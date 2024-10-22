import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import requests
import threading
import time

CLIENT_ID = '52523574'
CLIENT_SECRET = 'LTM9lNJGlW3SxaZY4Z8W'
REDIRECT_URI = 'http://localhost'
SCOPE = 'groups'
AUTH_URL = (
    f"https://oauth.vk.com/authorize?client_id={CLIENT_ID}"
    f"&display=page&redirect_uri={REDIRECT_URI}"
    f"&scope={SCOPE}&response_type=code&v=5.131"
)
authorization_code = None
access_token = None
server = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global authorization_code, access_token
        parsed_url = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_url.query)

        if 'code' in query_params:
            authorization_code = query_params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            print(f"Получен код авторизации: {authorization_code}")
            threading.Thread(target=shutdown_server).start()
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            print("Ошибка: Код авторизации не найден в запросу.")

def run_server():
    global server
    server_address = ('', 80)
    server = HTTPServer(server_address, OAuthHandler)
    print("Локальный сервер запущен на порту 80...")
    server.serve_forever()

def shutdown_server():
    time.sleep(1)
    server.shutdown()
    print("Сервер остановлен.")

def exchange_code_for_token(code):
    token_url = "https://oauth.vk.com/access_token"
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }
    print("Отправка параметров для обмена кода на токен:", params)  # Отладочный вывод
    try:
        response = requests.get(token_url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'access_token' in data:
            return data['access_token']
        else:
            print("Ошибка при обмене кода на токен:", data)
            return None
    except requests.exceptions.RequestException as e:
        print(f"HTTP ошибка при обмене кода на токен: {e}")
        return None
def main():
    global access_token
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    print("Открываем браузер для авторизации...")
    webbrowser.open(AUTH_URL)
    while authorization_code is None:
        time.sleep(1)
    access_token = exchange_code_for_token(authorization_code)
    if access_token:
        print("Токен доступа получен:", access_token)
    else:
        print("Не удалось получить токен доступа.")