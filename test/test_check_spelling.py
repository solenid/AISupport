# test_check_spelling.py
import pytest
from unittest.mock import patch
from CheckSpelling import checkSpelling

@patch('requests.post')
def test_check_spelling_success(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = [{'word': 'test', 's': ['suggestion']}]
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response
    
    result = checkSpelling("test text")
    assert isinstance(result, list)
    assert len(result) > 0

@patch('requests.post')
def test_check_spelling_http_error(mock_post):
    mock_post.side_effect = Exception("HTTP error")
    result = checkSpelling("test text")
    assert result == []

@patch('requests.post')
def test_check_spelling_value_error(mock_post):
    mock_response = MagicMock()
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_response.text = "raw response"
    mock_post.return_value = mock_response
    
    result = checkSpelling("test text")
    assert result == []