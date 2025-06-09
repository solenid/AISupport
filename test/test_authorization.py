# test_authorization.py
import pytest
from unittest.mock import patch, MagicMock
from Authorization import OAuthHandler, runServer, shutdownServer, exchangeCodeForToken

def test_oauth_handler_success():
    handler = OAuthHandler(MagicMock(), ('localhost', 80), MagicMock())
    handler.path = "/?code=test_code"
    handler.send_response = MagicMock()
    handler.send_header = MagicMock()
    handler.end_headers = MagicMock()
    handler.wfile = MagicMock()
    
    handler.do_GET()
    
    assert handler.send_response.called_with(200)
    assert b"Autorization complete" in handler.wfile.write.call_args[0][0]

def test_oauth_handler_failure():
    handler = OAuthHandler(MagicMock(), ('localhost', 80), MagicMock())
    handler.path = "/?error=access_denied"
    handler.send_response = MagicMock()
    handler.wfile = MagicMock()
    
    handler.do_GET()
    
    assert handler.send_response.called_with(400)
    assert b"Autorization ERROR" in handler.wfile.write.call_args[0][0]

@patch('threading.Thread')
def test_shutdown_server(mock_thread):
    mock_server = MagicMock()
    shutdownServer(mock_server)
    mock_server.shutdown.assert_called_once()

@patch('requests.get')
def test_exchange_code_for_token_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {'access_token': 'test_token'}
    mock_get.return_value = mock_response
    
    token = exchangeCodeForToken('test_code')
    assert token == 'test_token'

@patch('requests.get')
def test_exchange_code_for_token_failure(mock_get):
    mock_get.side_effect = Exception("HTTP error")
    token = exchangeCodeForToken('test_code')
    assert token is None