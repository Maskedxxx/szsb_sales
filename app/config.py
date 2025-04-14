# config.py

import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
ROUTES_PATH = os.path.join(BASE_DIR, "routes/")
# Путь к json с роутерами/маршрутами
ROUTING_TABLE_PATH = os.path.join(BASE_DIR, "routes/routing_table.json")
