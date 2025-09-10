#!/bin/bash

# Скрипт для извлечения данных из JSON файлов по субключу и полям
# Использование: ./extract_subkey_data.sh <json_file> <subkey> <field1,field2,field3...>

if [ $# -ne 3 ]; then
    echo "Использование: $0 <json_file> <subkey> <field1,field2,field3...>"
    echo "Пример: $0 additives.json cooked_sausages_tu name,application,dosage"
    exit 1
fi

JSON_FILE="app/routes/meat/$1"
SUBKEY="$2"
FIELDS="$3"

# Проверяем существование файла
if [ ! -f "$JSON_FILE" ]; then
    echo "Файл $JSON_FILE не найден!"
    exit 1
fi

echo "=== ДАННЫЕ ДЛЯ: $1 -> $SUBKEY ==="
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

echo "Найдено продуктов: $(echo "$PRODUCT_LIST" | wc -l)"
echo

# Для каждого поля показываем все уникальные значения
for FIELD in "${FIELD_ARRAY[@]}"; do
    echo "=== ПОЛЕ: $FIELD ==="
    
    case "$FIELD" in
        "name")
            echo "$PRODUCT_LIST" | jq -r 'select(has("name")) | .name' | sort | uniq
            ;;
        "application")
            if echo "$PRODUCT_LIST" | jq -e 'has("application")' >/dev/null 2>&1; then
                echo "$PRODUCT_LIST" | jq -r 'select(has("application")) | .application[]?' | sort | uniq
            else
                echo "[ПОЛЕ ОТСУТСТВУЕТ В ДАННЫХ]"
            fi
            ;;
        "composition")
            if echo "$PRODUCT_LIST" | jq -e 'has("composition")' >/dev/null 2>&1; then
                echo "$PRODUCT_LIST" | jq -r 'select(has("composition")) | .composition[]?' | sort | uniq
            else
                echo "[ПОЛЕ ОТСУТСТВУЕТ В ДАННЫХ]"
            fi
            ;;
        "advantages")
            if echo "$PRODUCT_LIST" | jq -e 'has("advantages")' >/dev/null 2>&1; then
                echo "$PRODUCT_LIST" | jq -r 'select(has("advantages")) | .advantages[]?' | sort | uniq
            else
                echo "[ПОЛЕ ОТСУТСТВУЕТ В ДАННЫХ]"
            fi
            ;;
        "dosage")
            if echo "$PRODUCT_LIST" | jq -e 'has("dosage")' >/dev/null 2>&1; then
                echo "$PRODUCT_LIST" | jq -r 'select(has("dosage")) | .dosage | "min: \(.min_g_per_kg)г, max: \(.max_g_per_kg)г"' | sort | uniq
            else
                echo "[ПОЛЕ ОТСУТСТВУЕТ В ДАННЫХ]"
            fi
            ;;
        "gost")
            if echo "$PRODUCT_LIST" | jq -e 'has("gost")' >/dev/null 2>&1; then
                echo "$PRODUCT_LIST" | jq -r 'select(has("gost")) | .gost' | sort | uniq
            else
                echo "[ПОЛЕ ОТСУТСТВУЕТ В ДАННЫХ]"
            fi
            ;;
        "is_halal")
            if echo "$PRODUCT_LIST" | jq -e 'has("is_halal")' >/dev/null 2>&1; then
                echo "$PRODUCT_LIST" | jq -r 'select(has("is_halal")) | .is_halal // "не указано"' | sort | uniq
            else
                echo "[ПОЛЕ ОТСУТСТВУЕТ В ДАННЫХ]"
            fi
            ;;
        "dosage_text")
            if echo "$PRODUCT_LIST" | jq -e 'has("dosage_text")' >/dev/null 2>&1; then
                echo "$PRODUCT_LIST" | jq -r 'select(has("dosage_text")) | .dosage_text' | sort | uniq
            else
                echo "[ПОЛЕ ОТСУТСТВУЕТ В ДАННЫХ]"
            fi
            ;;
        "description")
            if echo "$PRODUCT_LIST" | jq -e 'has("description")' >/dev/null 2>&1; then
                echo "$PRODUCT_LIST" | jq -r 'select(has("description")) | .description' | head -3
            else
                echo "[ПОЛЕ ОТСУТСТВУЕТ В ДАННЫХ]"
            fi
            ;;
        *)
            echo "Неизвестное поле: $FIELD"
            ;;
    esac
    echo
done

echo "=== ПРИМЕРЫ ПОЛНЫХ ЗАПИСЕЙ ==="
echo "$PRODUCT_LIST" | head -3 | jq .