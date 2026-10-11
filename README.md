# game-optimizer

мин тулза для винды: выбор игры -> убить фон -> макс питание -> приоритет -> откат.

## стэк
- python 3.11+
- psutil (работа с проц по доке)
- tkinter (встроен, гуи без зависим)
- powercfg (схемы питания винды)

## запуск
```bash
pip install -r requirements.txt
python app.py
```

## как польз
1. выбери игру: `cs2` / `dota2` / `valorant`
2. жми оптимизировать
3. запусти игру
4. после катки жми откатить

## профили
лежат в `profiles.json`, легко добавить свою игру:
```json
"fortnite": {"label": "Fortnite", "process": "FortniteClient-Win64-Shipping.exe", "kill": ["chrome.exe"], "priority": "high"}
```

## дисклеймер
не трогает реестр и драйвера, только фон и питание. запуск от обыч юзера, часть системных проц не убьются - так и надо.
