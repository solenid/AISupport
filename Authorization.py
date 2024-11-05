import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import requests
import threading
import time


clientID = '52523574'
clientSecret = 'LTM9lNJGlW3SxaZY4Z8W'
clientURI = 'http://localhost'
scope = 'groups'
authURL = (
    f"https://oauth.vk.com/authorize?client_id={clientID}"
    f"&display=page&redirect_uri={clientURI}"
    f"&scope={scope}&response_type=code&v=5.131"
)

authorizationCode = None
accessToken = None
server = None


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global authorizationCode, accessToken
        parsedUrl = urlparse.urlparse(self.path)
        queryParams = urlparse.parse_qs(parsedUrl.query)

        if 'code' in queryParams:
            authorizationCode = queryParams['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Autorization complete</h1></body></html>")
            threading.Thread(target=shutdownServer).start()
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Autorization ERROR</h1></body></html>")

def runServer():
    global server
    serverAddr = ('', 80)
    server = HTTPServer(serverAddr, OAuthHandler)
    print("Локальный сервер запущен на порту 80...")
    server.serve_forever()

def shutdownServer():
    time.sleep(1)
    server.shutdown()
    print("Сервер остановлен.")

def exchangeCodeForToken(code):
    tokenURL = "https://oauth.vk.com/access_token"
    params = {
        'client_id': clientID,
        'client_secret': clientSecret,
        'redirect_uri': clientURI,
        'code': code
    }
    try:
        response = requests.get(tokenURL, params=params)
        response.raise_for_status()
        data = response.json()
        if 'access_token' in data:
            return data['access_token']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"HTTP ошибка при обмене кода на токен: {e}")
        return None

def userAuthorization():
    startTime = time.time()
    global accessToken
    servThread = threading.Thread(target=runServer)
    servThread.daemon = True
    servThread.start()
    webbrowser.open(authURL)
    while authorizationCode is None:
        time.sleep(1)
        ourTime = time.time() - startTime
        print("Время авторизации")
        print(ourTime)
        if ourTime > 25:
            print("Долго выполняется басурман\n"
                  "Богатырей не хватает на них...")
    accessToken = exchangeCodeForToken(authorizationCode)
    if accessToken:
        return accessToken
    else:
        print("Не удалось получить токен доступа.")
