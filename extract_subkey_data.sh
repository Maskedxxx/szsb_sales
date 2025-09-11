#!/bin/bash

# Универсальный скрипт для извлечения данных из JSON файлов по субключу и полям
# Использование: ./extract_subkey_data.sh <industry> <json_file> <subkey> <field1,field2,field3...>

if [ $# -ne 4 ]; then
    echo "Использование: $0 <industry> <json_file> <subkey> <field1,field2,field3...>"
    echo "Пример: $0 semi_finished chees.json cheeses name,properties"
    exit 1
fi

INDUSTRY="$1"
JSON_FILE="app/routes/$INDUSTRY/$2"
SUBKEY="$3"
FIELDS="$4"

# Проверяем существование файла
if [ ! -f "$JSON_FILE" ]; then
    echo "Файл $JSON_FILE не найден!"
    exit 1
fi

echo "=== ДАННЫЕ ДЛЯ: $2 -> $SUBKEY ==="
echo "=== ПОЛЯ: $FIELDS ==="
echo

# Преобразуем список полей в массив
IFS=',' read -ra FIELD_ARRAY <<< "$FIELDS"

# Извлекаем product_list для указанного субключа
PRODUCT_LIST=$(jq -r ".$SUBKEY.product_list[]" "$JSON_FILE" 2>/dev/null)

if [ -z "$PRODUCT_LIST" ]; then
    echo "Субключ '$SUBKEY' не найден или пустой в файле $JSON_FILE"
    exit 1
fi

# Подсчет количества продуктов
PRODUCT_COUNT=$(jq -r ".$SUBKEY.product_list | length" "$JSON_FILE" 2>/dev/null)
echo "Найдено продуктов: $PRODUCT_COUNT"
echo

# Для каждого поля показываем все уникальные значения
for FIELD in "${FIELD_ARRAY[@]}"; do
    echo "=== ПОЛЕ: $FIELD ==="
    
    # Универсальная логика для любого поля
    # В semi_finished данные хранятся как JSON-строки в product_list, нужно их парсить
    VALUES=$(jq -r ".$SUBKEY.product_list[] | fromjson | .\"$FIELD\" // empty" "$JSON_FILE" 2>/dev/null | sort -u | grep -v '^$')
    
    if [ -z "$VALUES" ]; then
        echo "[ПОЛЕ ОТСУТСТВУЕТ В ДАННЫХ]"
    else
        echo "$VALUES" | while IFS= read -r value; do
            echo "  - $value"
        done
    fi
    echo
done

echo "=== ПРИМЕРЫ ПОЛНЫХ ЗАПИСЕЙ ==="
jq -r ".$SUBKEY.product_list[0:3][] | fromjson" "$JSON_FILE" 2>/dev/null | jq .