import pytest
from src.ui_components import UIComponents

def test_create_controls(mocker):
    ui = UIComponents()
    # Mock streamlit components
    mocker.patch('streamlit.text_input', return_value="test query")
    mocker.patch('streamlit.slider', return_value=5)
    mocker.patch('streamlit.checkbox', return_value=True)
    
    controls = ui.create_controls()
    assert isinstance(controls, dict)
    assert 'query' in controls
    assert 'max_sources' in controls

def test_display_results(mocker):
    ui = UIComponents()
    results = [{
        'content': 'Test content',
        'metadata': {
            'title': 'Test Title',
            'channel': 'Test Channel',
            'published_at': '2024-01-01'
        },
        'relevance_score': 0.8
    }]
    analysis = {'query_type': 'factual', 'topics': ['test']}
    
    # Mock streamlit components
    mocker.patch('streamlit.markdown')
    mocker.patch('streamlit.expander')
    
    ui.display_results(results, analysis)