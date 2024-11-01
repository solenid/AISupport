def getToken() -> str:
    with open('TOKEN.txt', 'r') as file:
        token = file.read()
    return token