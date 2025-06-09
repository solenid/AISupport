# test_get_info_from_vk.py
import pytest
from unittest.mock import patch, MagicMock
from GetInfoFromVK import getVKSession, getNumberOfFriends, getTotalComments, getTotalLikes

@patch('vk_api.VkApi')
def test_get_vk_session_success(mock_vk):
    mock_instance = MagicMock()
    mock_vk.return_value = mock_instance
    mock_instance.get_api.return_value = "api_instance"
    
    result = getVKSession("test_token")
    assert result == "api_instance"

@patch('vk_api.VkApi')
def test_get_number_of_friends(mock_vk):
    mock_api = MagicMock()
    mock_api.friends.get.return_value = {'count': 100}
    
    result = getNumberOfFriends(mock_api, "user123")
    assert result == 100

def test_get_total_comments():
    posts = [
        {'comments': {'count': 5}},
        {'comments': {'count': 10}},
        {'likes': {'count': 15}}
    ]
    result = getTotalComments(posts)
    assert result == 15

def test_get_total_likes():
    posts = [
        {'likes': {'count': 20}},
        {'likes': {'count': 30}},
        {'comments': {'count': 15}}
    ]
    result = getTotalLikes(posts)
    assert result == 50