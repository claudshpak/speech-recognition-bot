import logging

def setup_logger():
    logging.basicConfig(
        filename='bot.log',  # Имя файла для логов
        level=logging.INFO,  # Уровень логирования
        format='%(asctime)s - %(levelname)s - %(message)s'  # Формат логов
    )
    logging.info('Логирование настроено.')

