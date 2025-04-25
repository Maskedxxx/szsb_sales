# utils/logger.py

import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str = 'app') -> logging.Logger:
    """
    Настраивает и возвращает logger с ротацией файлов и выводом в консоль.
    """
    # Получаем логгер
    logger = logging.getLogger(name)
    
    # Проверяем, настроен ли он уже (важная защита от дублирования)
    if logger.hasHandlers():
        return logger  # Если уже настроен, просто возвращаем
    
    # Глобальная настройка для предотвращения распространения логов родительским логгерам
    logger.propagate = False
    
    logger.setLevel(logging.DEBUG)
    
    # Создаем форматтер с информацией о файле и строке
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    try:
        # Пытаемся создать директорию logs в текущей директории скрипта
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Путь к файлу лога
        log_path = os.path.join(log_dir, 'app.log')
        
        # Настраиваем файловый обработчик
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=1_048_576,  # 1 MB
            backupCount=1,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    except Exception as e:
        print(f"Не удалось настроить файловый логгер: {e}")
        print("Логи будут доступны только в консоли")

    # Настраиваем обработчик для консоли в любом случае
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# Создаем глобальный логгер
logger = setup_logger()