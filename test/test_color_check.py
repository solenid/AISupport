# test_color_check.py
import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
import numpy as np
from ColorCheck import colorz, downloadImage, colorCheck

def test_colorz_with_image():
    img = Image.new('RGB', (100, 100), color='red')
    colors = colorz(img, n=3)
    assert len(colors) == 3
    assert colors[0][0] > colors[0][1] and colors[0][0] > colors[0][2]

@patch('requests.get')
@patch('Image.open')
def test_download_image_success(mock_open, mock_get):
    mock_response = MagicMock()
    mock_response.content = b'test_image_data'
    mock_get.return_value = mock_response
    
    mock_img = MagicMock()
    mock_open.return_value = mock_img
    
    result = downloadImage("http://test.url/image.jpg")
    assert result == mock_img

@patch('ColorCheck.downloadImage')
def test_color_check_success(mock_download):
    mock_img = MagicMock()
    mock_download.return_value = mock_img
    
    with patch('ColorCheck.colorz', return_value=[[255, 0, 0]]):
        result = colorCheck("http://test.url/image.jpg", 3)
        assert result == [[255, 0, 0]]

@patch('ColorCheck.downloadImage')
def test_color_check_failure(mock_download):
    mock_download.side_effect = Exception("Download failed")
    result = colorCheck("http://test.url/image.jpg", 3)
    assert result is None