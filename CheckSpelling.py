import requests
def checkSpelling(text):
    url = "https://speller.yandex.net/services/spellservice.json/checkText"
    params = {
        'text': text,
        'lang': 'ru'
    }
    try:
        response = requests.post(url, data=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка запроса: {req_err}")
    except ValueError:
        print("Ошибка декодирования JSON. Ответ сервера:")
        print(response.text)
    return []