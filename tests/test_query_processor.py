import pytest
from src.query_processor import QueryProcessor

def test_detect_query_type(mock_openai_client):
    processor = QueryProcessor(None, mock_openai_client)
    query = "What does Lex Fridman say about AI?"
    result = processor.detect_query_type(query)
    assert isinstance(result, dict)
    assert 'query_type' in result
    assert 'topics' in result

def test_calculate_temporal_relevance():
    processor = QueryProcessor(None, None)
    metadata = {'published_at': '2024-01-01'}
    score = processor.calculate_temporal_relevance(metadata)
    assert 0 <= score <= 1

def test_calculate_content_relevance():
    processor = QueryProcessor(None, None)
    text = "AI and consciousness discussion"
    metadata = {'title': 'AI Ethics'}
    query_analysis = {
        'query_type': 'factual',
        'topics': ['AI', 'ethics'],
        'key_terms': ['AI', 'consciousness']
    }
    score = processor.calculate_content_relevance(text, metadata, query_analysis)
    assert 0 <= score <= 1