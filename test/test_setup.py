# test_setup.py
import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_vk_api():
    with patch('vk_api.VkApi') as mock:
        yield mock

@pytest.fixture
def mock_requests():
    with patch('requests.get') as mock:
        yield mock

@pytest.fixture
def mock_sqlite3():
    with patch('sqlite3.connect') as mock:
        yield mock