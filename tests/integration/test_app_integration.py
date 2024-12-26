import pytest
from src.app import PodcastInsightsApp

@pytest.mark.integration
def test_app_initialization():
    app = PodcastInsightsApp()
    assert app.chroma_client is not None
    assert app.openai_client is not None
    assert app.ui is not None

@pytest.mark.integration
def test_transcript_loading(mock_chroma_client):
    app = PodcastInsightsApp()
    app.chroma_client = mock_chroma_client
    collection = app.load_transcripts()
    assert collection is not None

@pytest.mark.integration
def test_query_processing(mock_chroma_client, mock_openai_client):
    app = PodcastInsightsApp()
    app.chroma_client = mock_chroma_client
    app.openai_client = mock_openai_client
    
    query = "What is consciousness?"
    controls = {
        'max_sources': 5,
        'min_relevance': 0.3,
        'podcast_sources': {'Lex Fridman': True}
    }
    
    results = app.process_query(query, controls)
    assert results is not None