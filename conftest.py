import pytest
from pages.user_page import UserPage
from config.generator import generate_user_data
from utils.logger import Logger

@pytest.fixture(scope="module")
def logger():
    return Logger()

@pytest.fixture(scope="module")
def user_page():
    return UserPage()

@pytest.fixture(scope="module")
def user_data():
    data = generate_user_data()
    return data

@pytest.fixture(scope="module")
def created_user(user_page, user_data, logger):
    response = user_page.create_user(user_data.__dict__)
    assert response.status_code == 200, response.text
    user_data.id = response.json().get('message')  # Обновляем id пользователя
    logger.info(f"Созданный пользователь (в фикстуре created_user): {user_data.__dict__}")
    return user_data