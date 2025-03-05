# config.py

import os

BASE_DIR = os.getcwd()
ROUTES_PATH = os.path.join(BASE_DIR, "app/routes/")  # Путь к репозиторию с файлами
# Путь к json с роутерами/маршрутами
ROUTING_TABLE_PATH = os.path.join(BASE_DIR, "app/routes/routing_table.json")
