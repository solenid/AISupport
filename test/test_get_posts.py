# test_get_posts.py
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from GetPosts import getPostsForLastYear

@patch('vk_api.exceptions.VkApiError')
def test_get_posts_for_last_year(mock_error):
    mock_vk = MagicMock()
    mock_vk.wall.get.return_value = {
        'count': 1,
        'items': [{
            'date': (datetime.now() - timedelta(days=100)).timestamp(),
            'comments': {'count': 5},
            'likes': {'count': 10}
        }]
    }
    
    result = getPostsForLastYear(mock_vk, "user123")
    assert len(result) == 1
    assert result[0]['likes']['count'] == 10

@patch('vk_api.exceptions.VkApiError')
def test_get_posts_error(mock_error):
    mock_vk = MagicMock()
    mock_vk.wall.get.side_effect = Exception("API error")
    
    result = getPostsForLastYear(mock_vk, "user123")
    assert result == []