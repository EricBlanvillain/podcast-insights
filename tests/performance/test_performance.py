import pytest
import time
from src.query_processor import QueryProcessor

@pytest.mark.performance
def test_query_processing_time(mock_chroma_client, mock_openai_client):
    processor = QueryProcessor(mock_chroma_client, mock_openai_client)
    
    start_time = time.time()
    result = processor.process_query("What is AI?", max_results=5)
    end_time = time.time()
    
    processing_time = end_time - start_time
    assert processing_time < 2.0  # Should process in less than 2 seconds

@pytest.mark.performance
def test_content_relevance_calculation_time(mock_chroma_client, mock_openai_client):
    processor = QueryProcessor(mock_chroma_client, mock_openai_client)
    
    text = "Sample text" * 1000  # Large text
    metadata = {"title": "Test", "channel": "Test Channel"}
    query_analysis = {"query_type": "factual", "topics": ["test"]}
    
    start_time = time.time()
    score = processor.calculate_content_relevance(text, metadata, query_analysis)
    end_time = time.time()
    
    calculation_time = end_time - start_time
    assert calculation_time < 0.1  # Should calculate in less than 0.1 seconds