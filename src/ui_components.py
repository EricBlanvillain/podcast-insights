import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class UIComponents:
    """Manages UI components and styling"""
    
    def setup_page(self):
        """Configure page settings and styling"""
        st.set_page_config(
            page_title="Podcast Insights",
            page_icon="🎙️",
            layout="wide",
            initial_sidebar_state="collapsed"  # Hide sidebar
        )
        self._load_custom_css()
    
    def _load_custom_css(self):
        """Load custom CSS styles"""
        st.markdown("""
            <style>
            /* Main Layout */
            .main-header {
                font-size: 2.5rem;
                color: #FF8C00;
                text-align: center;
                margin-bottom: 20px;
                font-weight: 600;
            }
            .subheader {
                color: #FF8C00;
                text-align: center;
                margin-bottom: 30px;
                font-size: 1.2rem;
            }

            /* Search Elements */
            .stTextInput > div > div > input {
                background-color: #F8F9FA;
                border: 2px solid #FF8C00;
                border-radius: 10px;
                padding: 12px 20px;
                font-size: 1.1rem;
                color: #000000;  /* Changed to black */
            }

            /* Buttons */
            .stButton > button {
                background-color: #FF8C00;
                color: white;
                border-radius: 8px;
                padding: 10px 25px;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                background-color: #FF7000;
                transform: translateY(-2px);
            }

            /* Results */
            .results-container {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 20px;
                margin-top: 30px;
            }

            /* Make sure placeholder text is also visible */
            .stTextInput > div > div > input::placeholder {
                color: #6B7280;
                opacity: 1;
            }
            </style>
        """, unsafe_allow_html=True)

    def render_header(self):
        """Display application header"""
        st.markdown(
            '<h1 class="main-header">🎙️ Podcast Insights</h1>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<h3 class="subheader">Explore insights from Lex Fridman, DOAC, Andrew Huberman and more...</h3>',
            unsafe_allow_html=True
        )

    def create_controls(self) -> Dict[str, Any]:
        """Create control elements in main content area"""
        # Query input box
        query = st.text_input(
            "",
            placeholder="Ask a question about any topic...",
            key="query_input",
            label_visibility="collapsed"
        )
        
        # Create two columns for basic settings
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            max_sources = st.slider(
                "Max Sources",
                1, 10, 5,
                help="Maximum number of sources to include"
            )
        
        with col2:
            min_relevance = st.slider(
                "Minimum Relevance",
                0.0, 1.0, 0.3,
                step=0.1,
                help="Minimum relevance score"
            )
            
        with col3:
            response_style = st.selectbox(
                "Response Style",
                ["Detailed", "Concise", "Academic"]
            )
        
        # Podcast Selection using columns
        st.markdown("#### Select Podcasts")
        podcast_cols = st.columns(3)
        podcast_sources = {}
        
        with podcast_cols[0]:
            podcast_sources["Lex Fridman"] = st.checkbox("Lex Fridman", value=True)
        with podcast_cols[1]:
            podcast_sources["Huberman Lab"] = st.checkbox("Andrew Huberman", value=True)
        with podcast_cols[2]:
            podcast_sources["Diary of a CEO"] = st.checkbox("DOAC", value=True)
        
        # Advanced settings in an expander
        with st.expander("Advanced Settings", expanded=False):
            adv_col1, adv_col2 = st.columns(2)
            
            with adv_col1:
                date_range = st.date_input(
                    "Date Range",
                    value=(
                        datetime.now().date() - timedelta(days=365),
                        datetime.now().date()
                    )
                )
            
            with adv_col2:
                show_metadata = st.toggle(
                    "Show Metadata",
                    value=False,
                    help="Display additional source information"
                )
        
        # Search button centered
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            search_clicked = st.button("Search", type="primary", use_container_width=True)
        
        return {
            'query': query,
            'search_clicked': search_clicked,
            'max_sources': max_sources,
            'min_relevance': min_relevance,
            'podcast_sources': podcast_sources,
            'date_range': date_range,
            'response_style': response_style,
            'show_metadata': show_metadata
        }

    def display_results(self, results: list, query_analysis: Dict, show_confidence: bool = False):
        """Display search results"""
        if not results:
            st.info("No results found.")
            return

        # Show query analysis if requested
        if show_confidence:
            with st.expander("Query Analysis", expanded=False):
                st.json(query_analysis)

        # Display results
        st.markdown("### Search Results")
        for idx, result in enumerate(results, 1):
            with st.expander(
                f"Source {idx}: {result['metadata'].get('title', 'Unknown Title')}",
                expanded=idx == 1
            ):
                # Metadata section
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Relevance", f"{result.get('relevance_score', 0.0):.2f}")
                with col2:
                    st.metric("Source", result['metadata'].get('channel', 'Unknown'))
                with col3:
                    st.metric("Date", result['metadata'].get('published_at', 'Unknown'))

                # Content section
                st.markdown("#### Excerpt")
                content = result.get('content', '')
                if isinstance(content, dict):
                    content = content.get('text', str(content))
                st.markdown(self._format_content(str(content)))
    
    def _format_content(self, content: str, max_length: int = 300) -> str:
        """Format content excerpt"""
        excerpt = content[:max_length]
        if len(content) > max_length:
            excerpt += "..."
        return excerpt.replace('\n', ' ').strip()