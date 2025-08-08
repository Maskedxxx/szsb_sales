# Backup старых хендлеров Tool Calling

## Содержимое

Эта папка содержит backup файлы старой архитектуры Tool Calling, которые были заменены новой универсальной архитектурой:

- `service.py.old` - старые хендлеры HoReCaHandler и MilkHandler  
- `data_filter.py.old` - старые функции фильтрации данных

## Дата создания backup
6 августа 2025

## Причина замены
Переход на новую универсальную архитектуру с UniversalIndustryHandler для упрощения добавления новых отраслей.

## Когда можно удалить
Эти файлы можно безопасно удалить через 1-2 месяца после успешного тестирования новой архитектуры в production.

## Восстановление (если потребуется)
```bash
# Восстановить старый HoReCa хендлер
cp .backup/service.py.old horeca/service.py
cp .backup/data_filter.py.old horeca/data_filter.py

# Восстановить старый Milk хендлер  
cp .backup/service.py.old milk/service.py
cp .backup/data_filter.py.old milk/data_filter.py

# Откатить ToolService
git checkout HEAD~5 service.py
```