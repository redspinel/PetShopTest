import logging
import os


class Logger:
    def __init__(self, log_file='test.log'):
        self.log_file = log_file  # Сохраняем имя файла как атрибут экземпляра
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Создаем директорию для логов, если она не существует
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Обработчик для записи логов в файл
        file_handler = logging.FileHandler(f'logs/{self.log_file}')
        file_handler.setLevel(logging.DEBUG)

        # Форматтер для логов
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def get_logs(self):
        with open(f'logs/{self.log_file}', 'r') as file:
            return file.read()

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)