# config.py

import os

BASE_DIR = os.getcwd()
ROUTES_PATH = os.path.join(BASE_DIR, "app/routes/")  # Путь к репозиторию с файлами
# Путь к json с роутерами/маршрутами
UTTERANCES_PATH = os.path.join(BASE_DIR, "app/routes/utterances.json")

# версия приложения
APP_VERSION = "0.5"
