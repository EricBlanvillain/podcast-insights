import pytest

@pytest.fixture
def sample_transcript_data():
    return {
        "title": "Understanding Consciousness",
        "channel": "Lex Fridman",
        "published_at": "2024-01-01",
        "text": "This is a sample transcript about consciousness and AI...",
        "metadata": {
            "duration": "02:15:30",
            "language": "en",
            "url": "https://youtube.com/example"
        }
    }

@pytest.fixture
def sample_query_result():
    return {
        'content': 'Sample content about AI and consciousness...',
        'metadata': {
            'title': 'AI and Consciousness',
            'channel': 'Lex Fridman',
            'published_at': '2024-01-01'
        },
        'distance': 0.5,
        'relevance_score': 0.8
    }