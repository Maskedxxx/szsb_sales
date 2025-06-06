# app/data/context_hints.py

# Словарь подсказок для выбора роутеров (файлов) в разных подсекторах
ROUTER_HINTS = {
    # Мясная отрасль
    "08": """
    ВАЖНО ПРИ ВЫБОРЕ ФАЙЛОВ:
    """,
    
    # Мороженое
    "05": """
    ВАЖНО ПРИ ВЫБОРЕ ФАЙЛОВ:
    """,
    
    # Напитки
    "09": """
    ВАЖНО ПРИ ВЫБОРЕ ФАЙЛОВ:
    - If the question concerns "energy drinks" or "kvas," choose the "mixture_data" router.
    - If the question concerns "juice-containing bases,"  choose the "flavor_data" router.
    - If the question concerns "matcha tea," also choose the "flavor_data" router.
    - If the question concerns "bacterial cultures," choose the "various_data" router.
    """,
    
    # Мучные кондитерские изделия
    "07": """
    ВАЖНО ПРИ ВЫБОРЕ ФАЙЛОВ:
    - Select the router `sweetener_collection` only if the question explicitly mentions sweeteners; otherwise, choose another router based on semantics.
    - If the question concerns "сухих смесей для приготовления" (dry mixes for preparation) or generally asks about any kind of mixes, select the router key `dry_mix_collection`.
    """
}

# Словарь подсказок для выбора ключей в разных подсекторах
KEY_HINTS = {
    # Мясная отрасль
    "08": """
    ВАЖНО ПРИ ВЫБОРЕ КЛЮЧЕЙ:
    """,
    
    # Мороженое
    "05": """
    ВАЖНО ПРИ ВЫБОРЕ КЛЮЧЕЙ:
    """,
    
    # Напитки
    "09": {
        "flavor_data": """
        ВАЖНО ПРИ ВЫБОРЕ КЛЮЧЕЙ В ФАЙЛЕ flavor_data:
        - If the question concerns "for sidra, cider," select the key "alcohol_flavor".
        - If the question pertains to clarifiers for beverages, prioritize selecting the key "citrus_aroma". This key includes two positions that have a clarifying effect.
        - If the question concerns "berry fruit drinks" or "compotes" or морсы, морс!, or "strawberries," choose the "grape_flavor" key.
        - If the question is general about flavorings and lacks specific categorization (e.g., 'Flavorings for beverages' or 'suggest some flavorings for beverages'), then select the key `fruit_aroma`.
        - Select the `natural` key exclusively if the question contains keywords such as "natural," "naturalness," etc. If these keywords are not present, do not select this key.
        """,
        "sweeteners_data": """
        - If the question is general and concerns sweeteners and does not specify a particular category, OR if it asks 'Which combined sweetener contains a combination of two sweeteners cyclamate and saccharinate?', then select the key `sweeteners_no_aspartame`.
        """,
        "colorant_collection": """
        - Select the `natural` key exclusively if the question contains keywords such as "natural," "naturalness," etc. If these keywords are not present, do not select this key.
        """
    },
    
    # Мучные кондитерские изделия
    "07": {
        "delar_collection": """
        ВАЖНО ПРИ ВЫБОРЕ КЛЮЧЕЙ В ФАЙЛЕ delar_collection:
         - If the question concerns cherry (вишня), select the key `berries`, as it belongs to the berry category.
        """
    }
}

def get_router_hint(subsector_id: str) -> str:
    """
    Получает подсказку для выбора роутеров.
    
    Args:
        subsector_id (str): ID подсектора
        
    Returns:
        str: Подсказка для выбора роутеров
    """
    return ROUTER_HINTS.get(subsector_id, "")

def get_key_hint(subsector_id: str, route_name: str = None) -> str:
    """
    Получает подсказку для выбора ключей в зависимости от подсектора и выбранного роутера.
    
    Args:
        subsector_id (str): ID подсектора
        route_name (str, optional): Название выбранного роутера
        
    Returns:
        str: Подсказка для выбора ключей
    """
    # Проверяем типы параметров и преобразуем списки в строки если нужно
    if isinstance(route_name, list) and len(route_name) > 0:
        route_name = route_name[0]
    elif isinstance(route_name, list) and len(route_name) == 0:
        route_name = None
    
    # Пробуем найти специфичную подсказку для роутера
    if (subsector_id in KEY_HINTS and 
        route_name and route_name in KEY_HINTS[subsector_id]):
        return KEY_HINTS[subsector_id][route_name]