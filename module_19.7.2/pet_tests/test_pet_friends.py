from api import PetFriends
from  settings import  valid_email, valid_password
import os


pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert  status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Ушастик', animal_type='корги',
                                     age='2', pet_photo='images/corgi.jpg'):


    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_delete_pet():
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Ушастик", "корги", "2", "images/corgi.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Ушастик', animal_type='корги', age=4):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


#Тест №1
def test_add_new_pet_whithout_photo_valid_data(name='Рыжик', animal_type='кот',
                                     age='1'):
    #Проверяем возможность добавления питоца с корректными данными без фото

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''

#Тест №2
def test_add_photo_of_pet(pet_photo='images/red_cat.jpg'):
    #Проверяем возможность отправки фото питомца

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    #Проверяем, если список не пустой, то пробуем добавить фото
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] != ''

#Тест №3
def test_add_monster_with_valid_data(name='Чужой', animal_type='монстр',
                                     age='50', pet_photo='images/alien.jpg'):
    """Проверяем возможность отправки на сервер запроса по добавлению фантастического монстра"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#Тест №4
def test_add_photo_error_format_pet(pet_photo='images/pet.txt'):
    #Проверяем невозможность отправки фото питомца неверного формата

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    #Проверяем, если список не пустой, то пробуем добавить фото
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200

#Тест №5
def test_negative_age_pet(name='Жора', animal_type='обезьяна',
                                     age='-5', pet_photo='images/monkey.jpg'):
    """"Проверка сайта на добавление питомца с отрицательным возрастом"""


    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print("Баг - сайт позволяет добавить питомца с отрицательным возрастом!")


#Тест №6
def test_extra_agey_pet(name='Жора', animal_type='обезьяна',
                                     age='555', pet_photo='images/monkey.jpg'):
    """"Проверка сайта на добавление питомца с нетипичным для животного возрастом"""


    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print("Баг - сайт позволяет добавить питомца со сверхвеликим возрастом!")

#Тест №7
def test_get_api_key_for_invalid_email(email = "qwerty@email", password = valid_password):
    #Проверяем получение кода 403, при введении неверного логина

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    #Проверяем результат
    assert status == 403

#Тест №8
def test_get_api_key_for_invalid_password(email = valid_email, password = 'password'):
    #Проверяем получение кода 403, при введении неверного пароля

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    #Проверяем результат
    assert status == 403

#Тест №9
def test_invalid_simbols(name='?!@:;', animal_type='12354$$$^',
                                     age='qwert', pet_photo='images/monkey.jpg'):
    #Проверка сайта на заполнение карточки питомца недопустимыми символами


    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print("Баг - сайт позволяет заполнить карточку питомца недопустимыми символами!")

#Тест №10
def test_empty_filds(name='', animal_type='',
                                     age='', pet_photo='images/monkey.jpg'):
    #Проверка сайта на добавление питомца с пустой карточкой


    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print("Баг - сайт позволяет добавить питомца с пустой карточкой!")