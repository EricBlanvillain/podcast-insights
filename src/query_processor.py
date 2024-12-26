import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
from openai import OpenAI

logger = logging.getLogger(__name__)

class QueryProcessor:
    """
    Handles query processing, analysis, and response generation for transcripts.
    """
    
    def __init__(self, collection, openai_client: OpenAI):
        """
        Initialize QueryProcessor.
        
        Args:
            collection: Chroma collection instance
            openai_client: OpenAI client instance
        """
        self.collection = collection
        self.openai_client = openai_client

    def detect_query_type(self, query: str) -> Dict[str, Any]:
        """
        Analyze query to determine type and requirements.
        
        Args:
            query: User's query string
            
        Returns:
            Dictionary containing query analysis
        """
        try:
            analysis_prompt = f"""Analyze this transcript-related query and provide a structured classification:
            Query: {query}
            
            Generate a JSON response with:
            1. query_type: one of [factual, opinion, comparison, procedural, conceptual]
            2. topics: list of main topics and subtopics
            3. context_needs: specific types of information needed
            4. expected_sources: relevant content or creators
            5. time_relevance: [recent_only, any_time, historical]
            6. summary_format: suggested response structure
            7. complexity_level: [basic, intermediate, advanced]
            8. key_terms: important terms or concepts to focus on"""

            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing queries about content."},
                    {"role": "user", "content": analysis_prompt}
                ]
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error in query analysis: {e}")
            # Return default analysis if error occurs
            return {
                "query_type": "factual",
                "topics": [query.lower()],
                "context_needs": ["general information"],
                "expected_sources": ["any"],
                "time_relevance": "any_time",
                "summary_format": "general",
                "complexity_level": "intermediate",
                "key_terms": query.lower().split()
            }

    def calculate_temporal_relevance(self, metadata: Dict[str, Any], max_age_days: int = 365) -> float:
        """
        Calculate temporal relevance score based on content age.
        
        Args:
            metadata: Content metadata containing publication date
            max_age_days: Maximum age to consider for scoring
            
        Returns:
            Float between 0.5 and 1.0 representing temporal relevance
        """
        try:
            if not metadata.get('published_at'):
                return 0.5

            published_date = pd.to_datetime(metadata['published_at'])
            age_days = (pd.Timestamp.now() - published_date).days
            
            # More recent content gets higher score, with a minimum of 0.5
            return max(0.5, 1 - (min(age_days, max_age_days) / (max_age_days * 2)))
            
        except Exception as e:
            logger.warning(f"Error calculating temporal relevance: {e}")
            return 0.5

    def calculate_content_relevance(
        self,
        text: str,
        metadata: Dict[str, Any],
        query_analysis: Dict[str, Any]
    ) -> float:
        """
        Calculate content relevance score based on various factors.
        """
        try:
            # Ensure text is string
            if isinstance(text, dict):
                text = str(text.get('text', ''))
            elif not isinstance(text, str):
                text = str(text)

            # Base semantic similarity
            semantic_score = 0.5

            # Title matching
            title = metadata.get('title', '').lower()
            topics = [str(t).lower() for t in query_analysis.get('topics', [])]
            title_match = sum(t in title for t in topics) / max(len(topics), 1)

            # Key terms matching
            text_lower = text.lower()
            key_terms = [str(term).lower() for term in query_analysis.get('key_terms', [])]
            term_matches = sum(term in text_lower for term in key_terms)
            term_score = min(term_matches * 0.1, 0.8)

            # Source relevance
            source_match = any(
                str(source).lower() in metadata.get('channel', '').lower()
                for source in query_analysis.get('expected_sources', ['any'])
            )
            source_score = 0.2 if source_match else 0

            # Temporal relevance
            temporal_score = self.calculate_temporal_relevance(metadata)

            # Calculate weighted score based on query type
            weights = {
                'factual': (0.3, 0.2, 0.3, 0.1, 0.1),
                'opinion': (0.2, 0.2, 0.2, 0.3, 0.1),
                'comparison': (0.3, 0.2, 0.2, 0.2, 0.1),
                'procedural': (0.2, 0.3, 0.3, 0.1, 0.1),
                'conceptual': (0.3, 0.2, 0.2, 0.2, 0.1)
            }

            query_type = query_analysis.get('query_type', 'factual')
            w = weights.get(query_type, weights['factual'])

            final_score = (
                semantic_score * w[0] +
                title_match * w[1] +
                term_score * w[2] +
                source_score * w[3] +
                temporal_score * w[4]
            )

            return min(max(final_score, 0), 1)

        except Exception as e:
            logger.error(f"Error calculating content relevance: {e}")
            return 0.0

    def get_initial_results(
            self,
            query: str,
            max_results: int,
            query_analysis: Dict[str, Any]
        ) -> List[Dict[str, Any]]:
            """
            Retrieve and process initial search results.
            """
            try:
                # Generate query embedding
                embedding = self.openai_client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=query
                ).data[0].embedding

                # Query collection with more results for filtering
                results = self.collection.query(
                    query_embeddings=[embedding],
                    n_results=max_results * 2,
                    include=["documents", "metadatas", "distances"]
                )

                processed_results = []
                for doc, meta, dist in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                ):
                    # Ensure consistent metadata
                    safe_meta = meta if meta else {}
                    safe_meta['title'] = safe_meta.get('title', 'Unknown Title')
                    safe_meta['published_at'] = safe_meta.get('published_at', 'Unknown Date')
                    safe_meta['channel'] = safe_meta.get('channel', 'Unknown Channel')

                    # Calculate relevance score
                    relevance_score = self.calculate_content_relevance(
                        doc,
                        safe_meta,
                        query_analysis
                    )

                    processed_results.append({
                        'content': doc,
                        'metadata': safe_meta,
                        'distance': dist,
                        'relevance_score': relevance_score
                    })

                return processed_results

            except Exception as e:
                logger.error(f"Error retrieving initial results: {e}")
                raise

    def generate_response(
        self,
        query: str,
        results: List[Dict[str, Any]],
        query_analysis: Dict[str, Any]
    ) -> str:
        """
        Generate a detailed response based on query and results.
        """
        try:
            if not results:
                return "No relevant results found."

            # Build detailed results
            detailed_results = []
            for idx, result in enumerate(results, 1):
                content = result['content']
                if isinstance(content, dict):
                    content = str(content.get('text', ''))
                elif not isinstance(content, str):
                    content = str(content)

                # Metadata display
                title = result['metadata'].get('title', 'Unknown Title')
                channel = result['metadata'].get('channel', 'Unknown Channel')
                published_at = result['metadata'].get('published_at', 'Unknown Date')
                relevance_score = result.get('relevance_score', 0.0)

                # Add detailed formatting
                detailed_results.append(f"""
    **Source {idx}:**  
    **Title:** {title}  
    **Channel:** {channel}  
    **Date:** {published_at}  
    **Relevance:** {relevance_score:.2f}  

    **Content Preview:**  
    {content[:500]}... *(truncated)*  

    ---
    """)

            # Combine detailed results
            all_details = "\n".join(detailed_results)

            # Build the final analysis prompt
            prompt = f"""You are analyzing transcript results to answer a query.  

    ### Question:  
    {query}  

    ### Detailed Results:  
    {all_details}  

    Provide:  
    1. A direct, concise answer to the query.  
    2. Supporting evidence from the results.  
    3. Relevant context or caveats for the user.  
    """

            # Generate response from OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert in summarizing and analyzing content."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Return the final response
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    def process_query(
        self,
        query: str,
        max_results: int = 5,
        min_relevance: float = 0.0,
        channels: Optional[Dict[str, bool]] = None,
        response_style: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Process user query and return relevant results.
        """
        try:
            query_analysis = self.detect_query_type(query)
            results = self.get_initial_results(query, max_results, query_analysis)

            filtered_results = [
                r for r in results
                if r['relevance_score'] >= min_relevance
                and (not channels or channels.get(r['metadata'].get('channel', ''), True))
            ]

            filtered_results.sort(key=lambda x: x['relevance_score'], reverse=True)
            final_results = filtered_results[:max_results]

            query_analysis.update({
                'results_found': len(final_results),
                'avg_relevance': sum(r['relevance_score'] for r in final_results) / len(final_results) if final_results else 0,
                'response_style': response_style
            })

            return final_results, query_analysis

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise