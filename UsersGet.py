from vk_api.exceptions import VkApiError
def GetBase(vk, USER_ID):
    result = []
    fields = 'status, bdate, universities, interests, schools'
    try:
        response = vk.users.get(user_ids=USER_ID, fields=fields)
        # Если ответ получен и Если ответ не пуст
        if (len(response) != 0):
            result.append(f"Имя: {response[0]['first_name']} {response[0]['last_name']}")
            #Дата рождения
            if ('bdate' in response[0]):
                result.append(f"Дата рождения: {response[0]['bdate']}")
            #Статус
            if (len(response[0]['status']) != 0):
                result.append(f"Статус: {response[0]['status']}")
            # Школы
            if ('schools' in response[0]):
                result.append(f"Школы:")
                for school in response[0]['schools']:
                    result.append(f"- {school['name']}")
            # Если указан университет
            if ('universities' in response[0]):
                if (len(response[0]['universities']) != 0):
                    result.append(f"Университет: {response[0]['universities'][0]['name']} \n")
                    if 'faculty_name' in response[0]['universities']:
                        if 'chair_name' in response[0]['universities']:
                            result.append(f"{response[0]['universities'][0]['faculty_name']} - {response[0]['universities'][0]['chair_name']}")
                        else:
                            result.append(f"{response[0]['universities'][0]['faculty_name']}")
        else:
            print(response)
    except VkApiError as e:
        print(f"Ошибка при информации профиля: {e}")
    return result
