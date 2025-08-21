# subsectors.py

# Список доступных отраслей для фронтенда
SUBSECTORS = [
    {"name": "Сельнозпродукция", "id": "00"},
    {"name": "HoReCa", "id": "01"},
    {"name": "Полуфабрикаты", "id": "02"},
    {"name": "Масложировая", "id": "03"},
    {"name": "Молочная", "id": "04"},
    {"name": "Мороженое", "id": "05"},
    # {"name": "Мукомольная", "id": "06"},
    {"name": "Мучные кондитерские изделия", "id": "07"},
    {"name": "Мясная", "id": "08"},
    {"name": "Напитки", "id": "09"},
    # {"name": "Овощная и фруктовая консервация", "id": "10"},
    # {"name": "Полуфабрикаты и кулинарные изделия", "id": "11"},
    # {"name": "Продукты быстрого приготовления", "id": "12"},
    # {"name": "Рыбная", "id": "13"}
]

# Маппинг ID отраслей к папкам с документами
SUBSECTOR_ROUTES = {
    "00": "selo",
    "01": "horeca",
    "02": "semi_finished",
    "03": "fat_and_oil",
    "04": "milk",
    "05": "ice_cream",
    # "06": "flour_milling_sector",
    "07": "bakery",
    "08": "meat",
    "09": "drinks",
    # "10": "fruit_vegetables_sector",
    # "11": "semi_finished_products_sector",
    # "12": "instant_products_sector",
    # "13": "fish_sector"
}