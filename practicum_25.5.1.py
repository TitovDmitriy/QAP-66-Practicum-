import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)

def test_show_my_pets():
    # подключаем драйвер Chrome
    pytest.driver = webdriver.Chrome('C:/chromedriver/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('jko2a9gvamez@mail.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('123456')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

    yield

    pytest.driver.quit()


def test_all_pets():
    # Задаем период неявного ожидания
    pytest.driver.implicitly_wait(10)
    pytest.driver.get('http://petfriends.skillfactory.ru/all_pets')
    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_my_pets():
    # Переходим к списку своих питомцев
    pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')
    # Ищем текст с количеством питомцев
    pets_text = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))

    assert 'Питомцев:' in pets_text.text

    # Получаем количество питомцев в статистике
    pets_amount = int(pets_text.text.split('\n')[1].split(':')[1])

    # Проверяем, что количество строк в таблице питомцев равно количеству питомцев в статистике
    rows = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr')))
    rows_amount = len(rows)

    assert pets_amount == rows_amount

    # Проверяем, что у половины питомцев есть фото
    rows = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr/th/img')))
    photo_amount = 0
    for row in rows:
        if row.get_attribute('src') != '':
            photo_amount += 1

    assert photo_amount >= pets_amount / 2

    # Проверяем, что у всех питомцев заданы имя, возраст и порода
    # Т.к. в таблице четыре колонки, то элементов /tbody/tr/td должно быть в 4 раза больше, чем количество питомцев,
    # и все эти элементы должны иметь какой-то текст
    elements = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr/td')))

    assert pets_amount * 4 == len(elements)

    data_filled = True
    for element in elements:
        text = element.text
        if text.isspace():
            data_filled = False
            break

    assert data_filled

    # Проверяем, что нет повторяющихся карточек питомцев
    data_list = []
    rows = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr')))
    for row in rows:
        cells = row.text.split()
        data = tuple([cells[0], cells[1], cells[2]])
        data_list.append(data)
    # Преобразуем список во множество, чтобы убрать повторяющиеся элементы
    data_set = set(data_list)

    assert len(data_list) == len(data_set)

    # Проверка на отсутствие одинаковых имён
    name_list = []
    rows = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr')) )
    for row in rows:
        cells = row.text.split()
        name_list.append(cells[0])
    # Снова преобразуем список во множество, чтобы убрать повторяющиеся элементы
    name_set = set(name_list)

    assert len(name_list) == len(name_set)