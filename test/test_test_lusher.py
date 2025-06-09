# test_test_lusher.py
import pytest
from unittest.mock import patch, MagicMock
from TestLusher import getPostsPhoto, startTestLusher

@patch('GetInfoFromVK.getVKSession')
def test_get_posts_photo(mock_session):
    mock_vk = MagicMock()
    mock_session.return_value = mock_vk
    mock_vk.wall.get.return_value = {
        'items': [{
            'attachments': [{
                'photo': {
                    'orig_photo': {'url': 'http://test.url/photo.jpg'},
                    'id': 'photo123'
                }
            }]
        }]
    }
    
    result = getPostsPhoto("user123")
    assert len(result[0]) == 1
    assert result[0][0] == 'http://test.url/photo.jpg'

@patch('TestLusher.getPostsPhoto')
@patch('TestLusher.colorCheck')
@patch('numpy.array')
def test_start_test_lusher(mock_array, mock_color, mock_posts):
    mock_posts.return_value = [['http://test.url/photo1.jpg', 'http://test.url/photo2.jpg'], []]
    mock_color.return_value = [[255, 0, 0]]
    
    result = startTestLusher("user123")
    assert "Самый часто используемый цвет" in result