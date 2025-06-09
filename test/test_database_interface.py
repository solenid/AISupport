# test_database_interface.py
import pytest
from unittest.mock import patch, MagicMock
from DataBaseInterface import initializeDB, addUser, getLast5Users, getUserById, deleteUserById

@patch('sqlite3.connect')
def test_initialize_db_success(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    initializeDB()
    mock_cursor.execute.assert_called()

@patch('DataBaseInterface.initializeDB')
@patch('sqlite3.connect')
def test_add_user_success(mock_connect, mock_init):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    addUser("Doe", "John", "1990-01-01", "3", "4", "2", "3", "1", "RECOMMEND", "http://vk.com/id1")
    mock_cursor.execute.assert_called()

@patch('sqlite3.connect')
def test_get_last_5_users(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, "Doe", "John", "1990-01-01", "3", "4", "2", "3", "1", "RECOMMEND", "http://vk.com/id1")]
    
    result = getLast5Users()
    assert len(result) == 1

@patch('sqlite3.connect')
def test_get_user_by_id(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, "Doe", "John", "1990-01-01", "3", "4", "2", "3", "1", "RECOMMEND", "http://vk.com/id1")
    
    result = getUserById(1)
    assert result[1] == "Doe"

@patch('sqlite3.connect')
def test_delete_user_by_id(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    deleteUserById(1)
    mock_cursor.execute.assert_called()