---
type: lesson
course: "python"
week: 4
day: 6
title: "Практика — менеджер персонажей RPG"
concepts: []
prerequisites: "[\"[week_4/day_5](/python/week_4/day_5/)\"]"
tags: [python, практика, файлы, json, os, проект]
status: draft
---

# Day 6: Практика — строим менеджер персонажей

> **Сегодня:** только практика. Никакого нового материала — только закрепление.
>
> **Время:** ~60 минут

---

Ты изучил за неделю: чтение/запись файлов, JSON, пути через `os.path`. Пришло время собрать всё в один проект.

Сегодня строим **менеджер персонажей RPG** — программу для хранения, загрузки и редактирования данных нескольких персонажей. Как профиль игрока в Steam, только свой.

---

## Задание 1 — Структура данных (10 мин)

Определи структуру JSON-файла для одного персонажа. Файл должен содержать:

- `name` — имя персонажа (строка)
- `class` — класс: `"воин"`, `"маг"`, `"вор"` (строка)
- `level` — уровень (int, от 1)
- `stats` — словарь: `hp`, `mp`, `strength`, `dexterity`
- `inventory` — список предметов (строки)
- `achievements` — множество выполненных ачивок (список в JSON)
- `playtime_hours` — время игры (float)

Создай папку `characters/` и вручную напиши JSON-файл для одного тестового персонажа. Проверь что можешь загрузить его в Python.

```python
import json
import os

with open(os.path.join("characters", "test.json"), encoding="utf-8") as f:
    char = json.load(f)
print(char["name"])
```

![JSON структура персонажа RPG: name, class, level, stats, inventory, achievements, playtime](day_6/day_6_character_json_structure.png)

---

## Задание 2 — Функции CRUD (20 мин)

Напиши четыре функции:

**`create_character(name, char_class)`** — создаёт нового персонажа со стартовыми значениями:
- level = 1
- stats: hp=100, mp=50, strength=10, dexterity=10
- inventory = []
- achievements = []
- playtime_hours = 0.0

Сохраняет в `characters/{name}.json`. Если имя уже занято — сообщает об ошибке.

**`load_character(name)`** — загружает персонажа из файла. Если не найден — `None`.

**`save_character(char)`** — сохраняет словарь персонажа в файл (имя файла = `char["name"]`).

**`list_characters()`** — возвращает список имён всех персонажей (все `.json` файлы из папки `characters/`).

<details>
<summary>Решение create_character и load_character</summary>

```python
import json
import os

CHARS_DIR = "characters"

def create_character(name, char_class):
    os.makedirs(CHARS_DIR, exist_ok=True)
    path = os.path.join(CHARS_DIR, f"{name}.json")

    if os.path.exists(path):
        print(f"Персонаж '{name}' уже существует")
        return None

    char = {
        "name": name,
        "class": char_class,
        "level": 1,
        "stats": {"hp": 100, "mp": 50, "strength": 10, "dexterity": 10},
        "inventory": [],
        "achievements": [],
        "playtime_hours": 0.0
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(char, f, ensure_ascii=False, indent=2)
    print(f"Создан: {name} ({char_class})")
    return char

def load_character(name):
    path = os.path.join(CHARS_DIR, f"{name}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)
```

</details>

![CRUD операции менеджера персонажей: create, load, update (level_up/add_item), delete](day_6/day_6_crud_flow.png)

---

## Задание 3 — Редактирование персонажа (15 мин)

Напиши функции изменения данных:

**`level_up(char)`** — повышает уровень на 1, увеличивает hp на 10, mp на 5. Сохраняет изменения.

**`add_item(char, item)`** — добавляет предмет в инвентарь. Если уже есть — не добавляет (проверь через `in`). Сохраняет.

**`unlock_achievement(char, achievement)`** — добавляет ачивку (если нет). `achievements` хранится как список, но работает как множество — без дублей. Сохраняет.

**`add_playtime(char, hours)`** — увеличивает время игры. Сохраняет.

<details>
<summary>Решение level_up</summary>

```python
def save_character(char):
    path = os.path.join(CHARS_DIR, f"{char['name']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(char, f, ensure_ascii=False, indent=2)

def level_up(char):
    char["level"] += 1
    char["stats"]["hp"] += 10
    char["stats"]["mp"] += 5
    save_character(char)
    print(f"{char['name']} достиг уровня {char['level']}!")
```

</details>

---

## Задание 4 — Главный цикл (15 мин)

Собери всё в интерактивную программу:

```
=== МЕНЕДЖЕР ПЕРСОНАЖЕЙ ===
Команды:
  список             — все персонажи
  создать            — создать нового
  загрузить <имя>    — выбрать персонажа
  (если персонаж выбран):
  статы              — все характеристики
  инвентарь          — предметы
  ачивки             — достижения
  прокачать          — повысить уровень
  добавить <предмет> — добавить предмет
  удалить            — удалить файл персонажа
  выход
```

Программа помнит **текущего выбранного персонажа** — переменная `current_char`.

**Примерный вывод `статы`:**
```
=== Artorias (воин) ===
Уровень: 52
HP: 620  MP: 105
Сила: 40  Ловкость: 30
Время игры: 47.5 ч
```

---

## Бонус — Экспорт в текст

Напиши функцию `export_to_txt(char)`, которая сохраняет карточку персонажа в `{name}_profile.txt` — красиво форматированный текстовый файл:

```
========================
КАРТОЧКА ПЕРСОНАЖА
========================
Имя:    Artorias
Класс:  воин
Уровень: 52

ХАРАКТЕРИСТИКИ
HP:       620
MP:       105
Сила:      40
Ловкость:  30

ИНВЕНТАРЬ (3 предмета):
  - Меч Бездны
  - Щит Рыцаря
  - Кольцо Хавела

ДОСТИЖЕНИЯ (5):
  - first_blood
  - boss_slayer
  ...
========================
```

---

## Чеклист выполнения

- [ ] Папка `characters/` создаётся автоматически при первом запуске
- [ ] `create_character` проверяет дубли
- [ ] `load_character` возвращает `None` если персонаж не найден
- [ ] Все пути через `os.path.join()`
- [ ] Сохранение с `ensure_ascii=False, indent=2`
- [ ] Главный цикл с командами `список`, `создать`, `загрузить`, `статы`
- [ ] **(Бонус)** Экспорт в `.txt`

---

← [Day 5 — Пути к файлам](/python/week_4/day_5/) | [Day 7 — Лонгрид →](/python/week_4/day_7/)
