---
type: practice
course: "[[python_basics/README]]"
week: 6
day: 6
title: "Практика — надёжная система сейвов"
concepts: []
prerequisites: "[\"[[week_6/day_5]]\"]"
tags: [python, ошибки, практика, проект, rpg]
status: draft
---

# День 6: Практика — надёжная система сейвов

За эту неделю ты изучил:
- `try/except/else/finally` и конкретные типы исключений
- `raise` и пробрасывание исключений
- Паттерны надёжного кода: safe_load, логирование, continue в цикле
- Свои исключения и иерархии

Сегодня применяем всё это вместе. Берём менеджер персонажей RPG из Week 4 и делаем его по-настоящему надёжным — таким, который не падает ни при каком вводе пользователя и ни при каком состоянии файловой системы.

Работай последовательно: каждое задание строится на предыдущем.

---

## Задание 1 — Иерархия исключений для RPG (10 мин)

Определи иерархию исключений для всего проекта. Положи этот блок в начало файла — остальные задания будут его использовать.

```python
# Базовое исключение — все игровые ошибки наследуют от него
class GameError(Exception):
    pass

# Ошибки персонажа: не удалось загрузить, создать, найти
class CharacterError(GameError):
    pass

# Ошибки файловой системы: не удалось читать/писать сейв
class SaveError(GameError):
    pass

# Ошибки валидации: неверные входные данные
class ValidationError(GameError):
    pass
```

**Проверь себя:** напиши код, который бросает `ValidationError` и ловит его через `except GameError`. Убедись что поймалось.

<!--illustration
file: day_6/save_system_architecture.png
alt: Архитектура системы сейвов RPG — иерархия ошибок, валидация, загрузка/сохранение, главный цикл
prompt:
Create a Dark RPG UI infographic showing the architecture of the RPG save system project being built.

Title: "АРХИТЕКТУРА СИСТЕМЫ СЕЙВОВ" in cream (#e8e0d4).

Left-to-right data flow with four layered glass-morphism panels connected by organic luminous threads:

LAYER 1 (amber) — "Иерархия ошибок":
  GameError
  ├── CharacterError
  ├── SaveError
  └── ValidationError
  Label: "Свои исключения — основа"

LAYER 2 (teal) — "Валидация (create_character)":
  - Проверка имени
  - Проверка класса
  - Проверка уровня
  Throws: ValidationError
  Label: "Данные правильные?"

LAYER 3 (indigo) — "Загрузка/сохранение":
  - safe_load_character()
  - safe_save_character()
  - log_error() → game_errors.log
  Throws: CharacterError, SaveError
  Label: "Работа с файлами"

LAYER 4 (green #7bc88f) — "game_loop()":
  - Команды: new, load, save, info
  - Ловит: ValidationError, CharacterError, SaveError
  - Никогда не падает
  Label: "Главный цикл — ловит всё"

Arrows between layers showing exception propagation (amber sparks) and success paths (teal).

Bottom: "Неделя 6 в одном проекте — 5 концепций вместе"

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette is MUTED and atmospheric, like cave crystals and bioluminescent fungi:
  - Teal #4db8c7 for primary elements (soft crystal light, NOT bright cyan)
  - Indigo #8b6cc1 for secondary elements (like glowing fungi)
  - Amber #d4854a for accents and highlights (like distant torchlight)
  - Cream #e8e0d4 for text (warm parchment white)
  - Green #7bc88f only for positive/success states
- ALL glows are SOFT and DIFFUSED: blur radius 10-15px, opacity 20-35%. Like bioluminescence in a dark cave. NEVER sharp neon edges. NEVER bright cyan #00ffff or bright purple #ff00ff.
- RPG ornamental frame: thin border 1px rgba(77,184,199,0.12), weathered stone corner ornaments (aged, slightly eroded, NOT polished).
- Nodes/orbs: dark glass rgba(10,14,26,0.85) with thin colored border. Icons inside as white silhouettes at 50% opacity.
- Connecting lines: organic curves (like roots/vines/light threads), NOT straight mechanical wires. 1-1.5px, soft glow.
- Glass-morphism panels for info cards: semi-transparent dark with subtle blur and soft shadow.
- Floating spore particles (1-3px dots) scattered across image — like Hollow Knight spores.
- Monospace font for all code text. Code colored: teal for keywords, amber for values, indigo for strings.
- Slight grain/noise texture on background surfaces.
- Russian (Cyrillic) text for all titles, labels, annotations.
- Three tiny color swatches (6x6px) at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight's City of Tears — contemplative, beautiful, mysterious. NOT aggressive, NOT cyberpunk.
-->

---

## Задание 2 — Валидация при создании персонажа (15 мин)

Напиши функцию `create_character(name, char_class, level=1)`. Она должна:

1. Проверить что `name` — непустая строка (без пробелов по краям)
2. Проверить что `char_class` — один из допустимых: `["воин", "маг", "лучник", "вор"]`
3. Проверить что `level` — целое число от 1 до 100
4. При нарушении любого условия — бросать `ValidationError` с понятным сообщением
5. При успехе — возвращать словарь персонажа

Пример структуры:

```python
VALID_CLASSES = ["воин", "маг", "лучник", "вор"]

def create_character(name, char_class, level=1):
    # Проверка имени
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Имя не может быть пустым")

    # Проверка класса
    if char_class not in VALID_CLASSES:
        raise ValidationError(
            f"Неверный класс '{char_class}'. Допустимые: {VALID_CLASSES}"
        )

    # Проверка уровня — добавь самостоятельно

    return {
        "name": name.strip(),
        "class": char_class,
        "level": level,
        "hp": level * 10,
        "inventory": []
    }
```

**Проверь:** вызови функцию с `name=""`, с `char_class="некромант"`, с `level=200`. Убедись что каждый раз бросается `ValidationError` с понятным сообщением.

---

## Задание 3 — Надёжный load и save (15 мин)

Напиши две функции с полноценной обработкой ошибок и логированием.

**safe_load_character(name)** — загружает персонажа из файла `characters/{name}.json`:
- Если файл не найден — бросает `CharacterError`
- Если JSON повреждён — бросает `SaveError` и логирует в `game_errors.log`
- Если данные есть но структура неверная (нет ключа `"level"`) — бросает `CharacterError`
- При успехе — возвращает словарь персонажа

**safe_save_character(char)** — сохраняет персонажа в `characters/{name}.json`:
- Если папка `characters/` не существует — создаёт её через `os.makedirs`
- Если не удалось записать файл — бросает `SaveError` и логирует ошибку
- При успехе — возвращает `True`

```python
import json
import os

SAVE_FOLDER = "characters"
LOG_FILE = "game_errors.log"

def log_error(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[ОШИБКА] {message}\n")

def safe_load_character(name):
    path = os.path.join(SAVE_FOLDER, f"{name}.json")
    try:
        with open(path, encoding="utf-8") as f:
            char = json.load(f)
    except FileNotFoundError:
        raise CharacterError(f"Персонаж '{name}' не найден")
    except json.JSONDecodeError as e:
        log_error(f"Повреждённый файл {path}: {e}")
        raise SaveError(f"Файл сейва повреждён: {path}")

    # Проверяем структуру — добавь проверку ключей самостоятельно

    return char
```

---

## Задание 4 — Главный цикл с обработкой всех ошибок (20 мин)

Напиши интерактивный цикл команд. При любой ошибке — выводи информативное сообщение, программа не падает.

Поддерживаемые команды:
- `new <имя> <класс>` — создать нового персонажа
- `load <имя>` — загрузить персонажа из файла
- `save` — сохранить текущего персонажа
- `info` — показать данные текущего персонажа
- `quit` — выйти

```python
def game_loop():
    current_char = None

    print("Менеджер персонажей RPG")
    print("Команды: new, load, save, info, quit")

    while True:
        command = input("\n> ").strip().split()
        if not command:
            continue

        action = command[0].lower()

        if action == "quit":
            print("До свидания!")
            break

        elif action == "new":
            if len(command) < 3:
                print("Использование: new <имя> <класс>")
                continue
            try:
                current_char = create_character(command[1], command[2])
                print(f"Создан персонаж: {current_char['name']}")
            except ValidationError as e:
                print(f"Ошибка создания: {e}")

        elif action == "load":
            # Реализуй самостоятельно
            pass

        elif action == "save":
            # Реализуй самостоятельно
            pass

        elif action == "info":
            if current_char is None:
                print("Нет активного персонажа. Создай или загрузи.")
            else:
                print(f"Имя: {current_char['name']}")
                print(f"Класс: {current_char['class']}")
                print(f"Уровень: {current_char['level']}")
        else:
            print(f"Неизвестная команда: {action}")
```

**Требования:**
- Команды `load` и `save` — реализуй полностью
- При `CharacterError` и `SaveError` — выводи понятное сообщение, не падай
- Команда `save` без активного персонажа — выводит подсказку, не падает
- Добавь команду `levelup` — повышает уровень на 1, максимум 100, иначе `ValidationError`

<!--illustration
file: day_6/error_recovery_flow.png
alt: Поток восстановления ошибок в главном цикле — нормальный путь, обработанная ошибка, критический выход
prompt:
Create a Dark RPG UI infographic showing the game loop error recovery flowchart.

Title: "ГЛАВНЫЙ ЦИКЛ — ПОТОКИ ОШИБОК" in cream (#e8e0d4).

A flowchart with three distinct paths:

ENTRY: "game_loop() — ввод команды" (teal orb at top)

NORMAL PATH (green, left column):
  command → action → try: execute → success → print result → loop again
  - Icons: clean arrows, check marks
  - Label: "Штатный путь"

ERROR PATH (amber, center column):
  try: execute → ValidationError / CharacterError / SaveError → except → print message → loop again
  - Icons: warning shield, message bubble
  - Label: "Обработанная ошибка — продолжаем"

UNRECOVERABLE PATH (dim red-amber, right column):
  unexpected crash → falls through → program exits
  - Icons: skull, break
  - Label: "Непредвиденная ошибка — выходим"
  - Note: "Не глотай — дай увидеть"

All three paths loop back (green and amber) or exit (red-amber).

Bottom: scan_saves() mini-diagram showing ✓ Артас | ✓ Гермиона | ✗ broken_save.json

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette is MUTED and atmospheric, like cave crystals and bioluminescent fungi:
  - Teal #4db8c7 for primary elements (soft crystal light, NOT bright cyan)
  - Indigo #8b6cc1 for secondary elements (like glowing fungi)
  - Amber #d4854a for accents and highlights (like distant torchlight)
  - Cream #e8e0d4 for text (warm parchment white)
  - Green #7bc88f only for positive/success states
- ALL glows are SOFT and DIFFUSED: blur radius 10-15px, opacity 20-35%. Like bioluminescence in a dark cave. NEVER sharp neon edges. NEVER bright cyan #00ffff or bright purple #ff00ff.
- RPG ornamental frame: thin border 1px rgba(77,184,199,0.12), weathered stone corner ornaments (aged, slightly eroded, NOT polished).
- Nodes/orbs: dark glass rgba(10,14,26,0.85) with thin colored border. Icons inside as white silhouettes at 50% opacity.
- Connecting lines: organic curves (like roots/vines/light threads), NOT straight mechanical wires. 1-1.5px, soft glow.
- Glass-morphism panels for info cards: semi-transparent dark with subtle blur and soft shadow.
- Floating spore particles (1-3px dots) scattered across image — like Hollow Knight spores.
- Monospace font for all code text. Code colored: teal for keywords, amber for values, indigo for strings.
- Slight grain/noise texture on background surfaces.
- Russian (Cyrillic) text for all titles, labels, annotations.
- Three tiny color swatches (6x6px) at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight's City of Tears — contemplative, beautiful, mysterious. NOT aggressive, NOT cyberpunk.
-->

---

## Бонус — Отчёт о сейвах

Напиши функцию `scan_saves()`, которая:
1. Проверяет существование папки `characters/`
2. Обходит все `.json` файлы
3. Пытается загрузить каждый через `safe_load_character`
4. Успешно загруженные — добавляет в список с именем и уровнем
5. Повреждённые — записывает имя файла в список проблемных
6. Выводит итоговый отчёт

Ожидаемый вывод:

```
Сканирование папки characters/...
  ✓ Артас — уровень 15
  ✓ Гермиона — уровень 8
  ✗ broken_save.json — SaveError: Файл сейва повреждён
  ✗ empty.json — CharacterError: Отсутствует ключ 'level'

Итог: загружено 2, повреждено 2
```

---

← [[week_6/day_5|День 5]] | [[week_6/day_7|День 7 →]]
