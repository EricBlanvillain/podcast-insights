import streamlit as st
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from chromadb import PersistentClient
import logging
import hashlib
from typing import Dict, Any, Tuple, List
from ui_components import UIComponents
from query_processor import QueryProcessor
import concurrent.futures

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PodcastInsightsApp:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize clients
        self.chroma_client = PersistentClient(path="./chroma_db")
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Initialize components
        self.ui = UIComponents()
        self.query_processor = None

    @staticmethod
    def generate_hash(file_path):
        """Generate a hash for a file to check if it's already processed."""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def load_transcripts(self):
        """Load transcripts into ChromaDB with caching."""
        try:
            collection = self.chroma_client.get_or_create_collection("youtube_transcripts")
            if collection.count() > 0:
                st.info("Transcripts already loaded in ChromaDB. Skipping loading.")
                return collection
            
            # Base path setup
            base_path = os.path.join(os.getcwd(), "youtube_transcripts")
            logger.info(f"Loading transcripts from: {base_path}")
            if not os.path.exists(base_path):
                st.error(f"Directory {base_path} does not exist. Please check the path.")
                return collection

            documents, metadatas, ids = [], [], []
            cache = {}

            def process_file(file_path, channel, filename):
                file_hash = self.generate_hash(file_path)
                if cache.get(file_hash):
                    logger.info(f"File {filename} already processed. Skipping.")
                    return None
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        transcript_data = json.load(f)
                    text = transcript_data.get('text', '')
                    metadata = {
                        'channel': channel,
                        'filename': filename,
                        'title': filename.split('.json')[0],
                        'date': filename.split('_')[0]
                    }
                    cache[file_hash] = True
                    return text, metadata, f"{channel}_{filename}"
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
                    return None

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for channel in os.listdir(base_path):
                    channel_path = os.path.join(base_path, channel)
                    if not os.path.exists(channel_path):
                        continue
                    for filename in os.listdir(channel_path):
                        if filename.endswith('.json'):
                            file_path = os.path.join(channel_path, filename)
                            futures.append(executor.submit(process_file, file_path, channel, filename))
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    text, metadata, doc_id = result
                    documents.append(text)
                    metadatas.append(metadata)
                    ids.append(doc_id)
            
            # Add documents to ChromaDB in batches
            if documents:
                BATCH_SIZE = 100
                for i in range(0, len(documents), BATCH_SIZE):
                    collection.add(
                        documents=documents[i:i + BATCH_SIZE],
                        metadatas=metadatas[i:i + BATCH_SIZE],
                        ids=ids[i:i + BATCH_SIZE]
                    )
                st.success(f"Successfully loaded {len(documents)} transcripts into ChromaDB")
            
            return collection
        except Exception as e:
            logger.error(f"Error loading transcripts: {e}")
            st.error(f"Error loading transcripts: {str(e)}")
            raise

    def setup(self):
        """Setup application state."""
        self.ui.setup_page()
        self.ui.render_header()
        
        try:
            # Load transcripts if needed
            collection = self.chroma_client.get_collection("youtube_transcripts")
            if collection.count() == 0:
                st.warning("Loading transcripts into ChromaDB...")
                collection = self.load_transcripts()
            
            self.query_processor = QueryProcessor(collection, self.openai_client)
            return True
        except Exception as e:
            st.error(f"Error initializing application: {str(e)}")
            logger.error(f"Setup error: {e}")
            return False

    def process_query(self, query: str, controls: Dict[str, Any]) -> Tuple[list, Dict[str, Any], str]:
        """Process user query with improved results handling."""
        try:
            logger.info(f"Processing query: {query}")
            logger.info(f"Controls: {controls}")
            
            results, analysis = self.query_processor.process_query(
                query=query,
                max_results=controls['max_sources'],
                min_relevance=controls['min_relevance'],
                channels=controls['podcast_sources'],
                response_style=controls['response_style']
            )
            
            if not results:
                logger.warning("No relevant results found for the query.")
                return [], {}, "No relevant results found. Try lowering the relevance threshold or rephrasing your query."

            response = self.query_processor.generate_response(
                query=query, 
                results=results,
                query_analysis=analysis
            )
            
            return results, analysis, response
        except Exception as e:
            logger.error(f"Query processing error: {e}")
            st.error(f"Query processing error: {str(e)}")
            raise

    def run(self):
        """Run the application."""
        if not self.setup():
            return

        try:
            # Get user input
            controls = self.ui.create_controls()
            
            # Process query if provided and search clicked
            if controls['query'] and controls['search_clicked']:
                with st.spinner('Analyzing...'):
                    try:
                        results, analysis, response = self.process_query(
                            query=controls['query'],
                            controls={k: v for k, v in controls.items() if k not in ['query', 'search_clicked']}
                        )
                        
                        # Display results
                        st.markdown(f"### Your Question\n{controls['query']}")
                        st.markdown("### Answer")
                        st.markdown(response)
                        
                        if controls.get('show_metadata', False):
                            st.markdown("### Detailed Results")
                            self.ui.display_results(
                                results,
                                analysis,
                                show_confidence=True
                            )
                    except Exception as e:
                        st.error(f"Error processing query: {str(e)}")
                        logger.error(f"Query processing error: {e}", exc_info=True)
        except Exception as e:
            st.error("An unexpected error occurred. Please try again later.")
            logger.error(f"Runtime error: {e}", exc_info=True)

if __name__ == "__main__":
    app = PodcastInsightsApp()
    app.run()