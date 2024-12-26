import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_openai_client():
    client = Mock()
    completion = Mock()
    completion.choices = [Mock(message=Mock(content='{"query_type": "factual", "topics": ["AI"], "context_needs": ["general"], "expected_sources": ["any"], "time_relevance": "any_time", "summary_format": "general", "complexity_level": "intermediate", "key_terms": ["AI"]}'))]
    client.chat.completions.create.return_value = completion
    return client

@pytest.fixture
def mock_chroma_client():
    client = Mock()
    collection = Mock()
    collection.query.return_value = {
        'documents': [['Sample document']],
        'metadatas': [[{'title': 'Test', 'channel': 'Test Channel'}]],
        'distances': [[0.5]]
    }
    client.get_or_create_collection.return_value = collection
    return client