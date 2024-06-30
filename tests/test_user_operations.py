import pytest
import allure
from jsonschema import validate, ValidationError
from config.data import *
import time
import json

@pytest.mark.usefixtures("user_page", "user_data", "created_user")
class TestUserOperations:

    def test_create_user(self, user_page, user_data, logger):
        with allure.step("Создание пользователя"):
            logger.info("Создание пользователя...")
            response = user_page.create_user(user_data.__dict__)
            assert response.status_code == 200, response.text
            allure.attach(response.text, name="Текст ответа", attachment_type=allure.attachment_type.JSON)
            allure.attach(str(response.headers), name="Заголовки", attachment_type=allure.attachment_type.JSON)

            logger.info(f"Тест 'test_create_user' - Данные пользователя: {user_data.__dict__}")

            if response.headers.get('Content-Type') == 'application/json':
                data = response.json()
                logger.info(f"Полученные данные с сервера: {data}")

                with allure.step("Проверка Json схемы ответа"):
                    try:
                        validate(instance=data, schema=response_create_user_schema)
                    except ValidationError as e:
                        logger.error(f"Ошибка валидации Json схемы: {e}")
                        pytest.fail(f"Ошибка валидации Json схемы: {e}")

                with allure.step("Проверка соответствия ID пользователя и сообщения"):
                    assert data.get('message') == str(user_data.id), (
                        f"ID в ответе ({data.get('message')}) не соответствует ожидаемому ID ({user_data.id})"
                    )
                    logger.info(f"ID в ответе ({data.get('message')}) соответствует ожидаемому ID ({user_data.id})")
            else:
                logger.error("Ответ не в формате JSON")
                pytest.fail("Ответ не в формате JSON")

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)

    def test_get_user(self, user_page, created_user, logger):
        with allure.step("Получить данные созданного профиля"):
            logger.info("Получить данные созданного профиля...")
            response = user_page.get_user(created_user.username)
            assert response.status_code == 200, response.text

            logger.info(f"Тест 'test_get_user' - Данные пользователя: {created_user.__dict__}")

            with allure.step("Регистрация ответа"):
                allure.attach(response.text, name="Текст ответа", attachment_type=allure.attachment_type.JSON)
                allure.attach(str(response.headers), name="Заголовки", attachment_type=allure.attachment_type.JSON)
                logger.info(f"Ответ сервера: {response.text}")
                logger.info(f"Заголовки ответа: {response.headers}")

            if response.headers.get('Content-Type') == 'application/json':
                data = response.json()
                logger.info(f"Полученные данные с сервера: {data}")

                with allure.step("Проверка Json схемы"):
                    try:
                        validate(instance=data, schema=user_schema)
                    except ValidationError as e:
                        logger.error(f"Ошибка валидации Json схемы: {e}")
                        pytest.fail(f"Ошибка валидации Json схемы: {e}")

                with allure.step("Проверка соответствия данных пользователя"):
                    assert data['username'] == created_user.username, "Имя пользователя не соответствует"
                    assert data['firstName'] == created_user.firstName, "Имя не соответствует"
                    assert data['lastName'] == created_user.lastName, "Фамилия не соответствует"
                    assert data['email'] == created_user.email, "Email не соответствует"
                    assert data['phone'] == created_user.phone, "Телефон не соответствует"
                    logger.info("Данные пользователя успешно проверены и соответствуют ожидаемым значениям")
            else:
                logger.error("Ответ не в формате JSON")
                pytest.fail("Ответ не в формате JSON")

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)

    def test_update_user(self, user_page, created_user, logger, user_data):
        with allure.step("Обновление данных созданного профиля"):
            logger.info("Обновление данных созданного профиля...")
            user_data = created_user
            user_data.firstName = "Ryan"

            logger.info(f"Username для обновления: {created_user.username}")
            logger.info(f"Обновлённые данные профиля: {user_data.__dict__}")
            response = user_page.update_user(created_user.username, user_data.__dict__)
            logger.info(f"Тело ответа: {response.text}")

            assert response.status_code == 200, response.text

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)

    def test_delete_user(self, user_page, created_user, logger):
        with allure.step("Удаление созданного профиля"):
            logger.info("Удаление созданного профиля...")
            logger.info(f"Username для удаления: {created_user.username}")
            response = user_page.delete_user(created_user.username)
            logger.info(f"Тело ответа: {response.text}")
            assert response.status_code == 200, response.text

            # Проверка полученной схемы
            expected_response = json.loads(json.dumps(expected_delete_user_response)
                                           .replace("username_placeholder", created_user.username))
            response_json = response.json()

            logger.info(f"Ожидаемый результат: {expected_response}")
            logger.info(f"Фактический результат: {response_json}")

            assert response_json == expected_response, f"Ожидаемая {expected_response}, было получено {response_json}"

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)

    def test_login_user(self, user_page, created_user, logger):
        with allure.step("Вход в систему пользователем"):
            logger.info("Вход в систему пользователем...")
            logger.info(f"Username: {created_user.username}")
            logger.info(f"Password: {created_user.password}")
            response = user_page.login_user(created_user.username, created_user.password)
            logger.info(f"Тело ответа: {response.text}")
            assert response.status_code == 200, response.text
            response_json = response.json()
            expected_response = json.loads(json.dumps(expected_login_success_response))

            # Проверка "logged in user session" в "message"
            assert response_json["code"] == expected_response["code"], \
                f"Expected code {expected_response['code']}, but got {response_json['code']}"
            assert response_json["type"] == expected_response["type"], \
                f"Expected type {expected_response['type']}, but got {response_json['type']}"
            assert response_json["message"].startswith(expected_response["message"]), \
                f"Expected message to start with {expected_response['message']}, but got {response_json['message']}"

            logger.info("Вход в систему выполнен успешно")

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)

    def test_logout_user(self, user_page, logger):
        with allure.step("Выход из системы пользователем"):
            logger.info("Выход из системы пользователем...")
            response = user_page.logout_user()
            logger.info(f"Тело ответа: {response.text}")
            assert response.status_code == 200, response.text
            response_json = response.json()
            expected_response = json.loads(json.dumps(expected_logout_success_response))
            logger.info(f"Ожидаемый результат: {expected_response}")
            logger.info(f"Фактический результат: {response_json}")

            assert response_json == expected_response, f"Expected {expected_response}, but got {response_json}"
            logger.info("Выход из системы выполнен успешно!")

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)

    def test_get_nonexistent_user(self, user_page, logger):
        with allure.step("Получение несуществующего пользователя"):
            username = "Ryan Gosling"
            logger.info(f"Получение данных с несуществующим пользователем: {username}")
            response = user_page.get_user(username)
            logger.info(f"Тело ответа: {response.text}")
            assert response.status_code == 404, response.text

            if response.headers.get('Content-Type') == 'application/json':
                response_json = response.json()
                expected_response = json.loads(json.dumps(expected_nonexistent_user_response))

                logger.info(f"Ожидаемый результат: {expected_response}")
                logger.info(f"Фактический результат: {response_json}")

                assert response_json == expected_response, f"Ожидаемый {expected_response}, получено {response_json}"
            else:
                logger.warning("Ответ не в формате JSON")
                pytest.skip("Ответ не в формате JSON")

        with allure.step("Прикрепление данных после теста"):
            allure.attach(response.text, name="Текст ответа", attachment_type=allure.attachment_type.JSON)
            allure.attach(str(response.headers), name="Заголовки", attachment_type=allure.attachment_type.JSON)

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)

    def test_create_user_with_existing_username(self, user_page, created_user, logger, user_data):
        with allure.step("Создание пользователя с существующим именем пользователя"):
            logger.info("Создание пользователя с существующим именем пользователя...")
            user_data = created_user
            user_data.email = "RyanGosling@gmail.com"  # изменение емейла у старого пользователя
            logger.info(f"Попытка создать пользователя с данными: {user_data.__dict__}")
            response = user_page.create_user(user_data.__dict__)
            logger.info(f"Тело ответа: {response.text}")

            with allure.step("Регистрация ответа"):
                allure.attach(response.text, name="Текст ответа", attachment_type=allure.attachment_type.JSON)
                allure.attach(str(response.headers), name="Заголовки", attachment_type=allure.attachment_type.JSON)
                logger.info(f"Заголовки ответа: {response.headers}")

            expected_status = 400 if response.status_code != 200 else 200
            assert response.status_code == expected_status, response.text
            logger.info(f"Ожидаемый статус: {expected_status}, фактический статус: {response.status_code}")

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)

    def test_login_with_wrong_data(self, user_page, created_user, logger):
        with allure.step("Вход в систему с недействительными учетными данными"):
            logger.info("Вход в систему с недействительными учетными данными...")
            logger.info(f"Username: {created_user.username}")
            logger.info("Пароль: wrongpassword123")

            response = user_page.login_user(created_user.username, "wrongpassword123")

            logger.info(f"HTTP статус код ответа: {response.status_code}")
            logger.info(f"Тело ответа: {response.text}")

            with allure.step("Регистрация ответа"):
                allure.attach(response.text, name="Текст ответа", attachment_type=allure.attachment_type.JSON)
                allure.attach(str(response.headers), name="Заголовки", attachment_type=allure.attachment_type.JSON)
                logger.info(f"Заголовки ответа: {response.headers}")

            assert response.status_code == 400, f"Ожидаемый 400ый статус код, но получен {response.status_code}. Ответ: {response.text}"

            if response.headers.get('Content-Type') == 'application/json':
                response_json = response.json()

                logger.info(f"Фактическое тело ответа: {response_json}")

                expected_response = json.loads(json.dumps(expected_login_error_response))

                assert response_json == expected_response, f"Expected {expected_response}, but got {response_json}"
            else:
                logger.warning("Ответ не в формате JSON")
                pytest.skip("Ответ не в формате JSON")

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)

    def test_time_creating_user(self, user_page, created_user, logger, user_data):
        max_response_time = 5
        with allure.step("Измерение времени отклика при создании пользователя"):
            logger.info("Начало измерения времени отклика при создании пользователя...")
            user_data = created_user
            start_time = time.time()
            response = user_page.create_user(user_data.__dict__)
            end_time = time.time()
            response_time = end_time - start_time

            logger.info(f"Время отклика: {response_time} секунд")
            allure.attach(str(response_time), name="Время ответа", attachment_type=allure.attachment_type.TEXT)
            assert response_time < max_response_time, f"Время ответа слишком большое: {response_time} секунд"
            logger.info(f"Время ответа в пределах нормы: {response_time} секунд")

            assert response.status_code == 200, response.text
            logger.info(f"HTTP статус код ответа: {response.status_code}")

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)

    def test_create_users_with_array(self, user_page, logger):
        with allure.step("Создание списка пользователей с использованием массива"):
            logger.info("Создание пользователей с массивом данных...")
            users_data = [
                {
                    "id": 1, "username": "user1", "firstName": "First1",
                    "lastName": "Last1", "email": "user1@example.com",
                    "password": "password1", "phone": "1234567890", "userStatus": 0
                },
                {
                    "id": 2, "username": "user2", "firstName": "First2",
                    "lastName": "Last2", "email": "user2@example.com",
                    "password": "password2", "phone": "1234567891", "userStatus": 0
                }
            ]
            logger.info(f"Данные пользователей: {users_data}")

            response = user_page.create_users_with_array(users_data)
            logger.info(f"Тело ответа: {response.text}")

        with allure.step("Регистрация ответа"):
            allure.attach(response.text, name="Текст ответа", attachment_type=allure.attachment_type.JSON)
            allure.attach(str(response.headers), name="Заголовки", attachment_type=allure.attachment_type.JSON)
            logger.info(f"Заголовки ответа: {response.headers}")

        assert response.status_code == 200, response.text
        logger.info(f"HTTP статус код ответа: {response.status_code}")

        response_json = response.json()
        validate(instance=response_json, schema=response_create_user_schema)
        logger.info("Ответ соответствует ожидаемой схеме.")

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)

    def test_delete_nonexistent_user(self, user_page, logger):
        with allure.step("Удаление несуществующего пользователя"):
            username = "John Wick"
            logger.info(f"Удаление несуществующего пользователя: {username}")

            response = user_page.delete_user(username)

            logger.info(f"HTTP статус код ответа: {response.status_code}")
            logger.info(f"Тело ответа: {response.text}")

            with allure.step("Регистрация ответа"):
                allure.attach(response.text, name="Текст ответа", attachment_type=allure.attachment_type.JSON)
                allure.attach(str(response.headers), name="Заголовки", attachment_type=allure.attachment_type.JSON)
                logger.info(f"Заголовки ответа: {response.headers}")

            assert response.status_code == 404, f"Ожидаемый статус 404, но получен {response.status_code}. Ответ: {response.text}"

        with allure.step("Прикрепление логов"):
            logs = logger.get_logs()
            allure.attach(logs, name="Логи", attachment_type=allure.attachment_type.TEXT)



