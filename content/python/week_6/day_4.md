---
type: lesson
course: "[[python_basics/README]]"
week: 6
day: 4
title: "Паттерны надёжного кода"
concepts: [safe_load паттерн, логирование ошибок, try/except в цикле, цепочка вызовов]
prerequisites: "[\"[[week_6/day_3]]\"]"
tags: [python, ошибки, паттерны, logging, цикл]
status: draft
---

# День 4: Паттерны надёжного кода

Знать `try/except` — это одно. Знать **как** использовать в реальном коде — совсем другое.

Представь двух кузнецов. Первый умеет ковать меч — он берёт металл и бьёт по нему. Второй кузнец умеет это же, но ещё знает паттерны — как правильно складывать удары, в каком порядке, какой нагрев нужен. Их мечи выглядят одинаково снаружи, но меч второго не сломается в бою.

Сегодня три рабочих паттерна, которые используются в каждой серьёзной программе.

---

## Часть 1: Паттерн safe_load — оборачиваем опасные операции

Есть проблема: когда `open()` или `json.load()` бросает исключение, твой код прерывается в том месте, где произошла ошибка. Иногда удобнее получить ошибку как **значение** — строку с описанием — а не как исключение, которое всё роняет.

Паттерн **safe_load** — функция-обёртка, которая возвращает пару `(данные, ошибка)`. Если всё хорошо — `(данные, None)`. Если плохо — `(None, "что пошло не так")`.

```python
import json

def safe_load_json(filename):
    """Загружает JSON. Возвращает (данные, None) или (None, описание_ошибки)."""
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, f"Файл не найден: {filename}"
    except json.JSONDecodeError as e:
        return None, f"Файл повреждён: {e}"
```

Посмотри на использование — оно читается как обычный код:

```python
data, error = safe_load_json("save.json")

if error:
    print(f"Проблема: {error}")
    # → Проблема: Файл не найден: save.json
else:
    print(f"Загружено: {data['name']}")
    # → Загружено: Артас
```

Ключевая идея: вызывающий код **не знает** про try/except. Он просто проверяет `if error`. Вся "страшная" логика скрыта внутри функции.

> Это как в Minecraft: функция `loadChunk()` внутри движка сама разбирается с повреждёнными данными региона. Ты просто получаешь чанк или пустую заглушку — и не думаешь про детали.

<!--illustration
file: day_4/safe_load_pattern.png
alt: Паттерн safe_load — функция возвращает (data, None) при успехе и (None, error) при ошибке
prompt:
Create a Dark RPG UI infographic showing the safe_load (data, error) tuple return pattern.

Title: "ПАТТЕРН safe_load — (данные, ошибка)" in cream (#e8e0d4).

Central diagram showing function input/output:

FUNCTION BOX (teal glass panel): "safe_load_json(filename)"
  Inside: try/except logic shown as simplified icon flow

TWO output arrows diverging downward:

LEFT arrow (green) — "Успех":
  Glass panel: return json.load(f), None
  Output box: data = { name: "Артас", level: 15 }, error = None
  Check mark icon

RIGHT arrow (amber) — "Ошибка":
  Glass panel: return None, f"Файл не найден: {filename}"
  Output box: data = None, error = "Файл не найден: save.json"
  Warning icon

BOTTOM: Usage code panel:
  data, error = safe_load_json("save.json")
  if error:
      print(f"Проблема: {error}")   ← amber path
  else:
      print(f"Загружено: {data['name']}")   ← green path

Key insight panel: "Вызывающий код НЕ ЗНАЕТ про try/except — просто проверяет if error"

Minecraft anvil icon in corner — "как loadChunk() в движке"

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

## Часть 2: Логирование ошибок в файл

Обработать ошибку — хорошо. Но если программа работает без пользователя (например, ночной бэкап сейвов), как потом узнать что пошло не так?

Ответ: **лог-файл**. Пишем ошибки в файл, чтобы потом разобраться.

```python
import json

LOG_FILE = "errors.log"

def log_error(message):
    """Дописывает сообщение об ошибке в лог-файл."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[ОШИБКА] {message}\n")

def safe_save_json(data, filename):
    """Сохраняет данные в JSON. При ошибке — пишет в лог и пробрасывает."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log_error(f"Не удалось сохранить {filename}: {e}")
        raise   # ← пробрасываем исключение выше, не глотаем
```

Обрати внимание на `raise` в конце — без аргументов он пробрасывает **то же исключение** дальше. Мы записали ошибку в лог, но не "проглотили" её. Вызывающий код всё равно узнает что что-то пошло не так.

Файл `errors.log` после нескольких запусков будет выглядеть так:

```
[ОШИБКА] Не удалось сохранить arthas.json: [Errno 28] No space left on device
[ОШИБКА] Не удалось сохранить backup.json: [Errno 13] Permission denied
```

---

## Часть 3: try/except в цикле — continue при ошибке

Допустим, у тебя 50 файлов сейвов. Один повреждён. Должна ли программа упасть из-за одного файла?

Нет. При ошибке в одном элементе — **пропускаем его** с помощью `continue` и продолжаем обработку остальных.

```python
import json
import os

def load_all_characters(folder):
    """Загружает персонажей из папки, пропуская повреждённые файлы."""
    characters = []
    for filename in os.listdir(folder):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(folder, filename)
        try:
            with open(path, encoding="utf-8") as f:
                char = json.load(f)
            characters.append(char)
        except (json.JSONDecodeError, KeyError) as e:
            log_error(f"Пропущен {filename}: {e}")
            continue   # ← переходим к следующему файлу
    return characters
```

Без `try/except` один повреждённый файл роняет всю загрузку. С паттерном выше — получаем список всех **рабочих** персонажей, а повреждённые молча логируются.

> В Dark Souls это как загрузка мира: даже если один регион повреждён, остальные локации всё равно доступны. Игра не падает целиком из-за одной кривой пещеры.

<!--illustration
file: day_4/try_continue_loop.png
alt: try/except в цикле — пропускаем сломанные файлы с continue, обрабатываем рабочие
prompt:
Create a Dark RPG UI infographic showing try/except + continue pattern inside a for loop.

Title: "try/except В ЦИКЛЕ — ПРОПУСКАЕМ ПЛОХИЕ" in cream (#e8e0d4).

A visual loop diagram showing multiple iterations:

LOOP: for filename in ["char1.json", "BROKEN.json", "char3.json", "char4.json"]

Each iteration shown as a horizontal row:

Row 1 (teal, check): "char1.json" → try succeeds → characters.append(char) ✓
Row 2 (amber, skull): "BROKEN.json" → JSONDecodeError → except: log_error → continue → SKIPPED
Row 3 (teal, check): "char3.json" → try succeeds → characters.append(char) ✓
Row 4 (teal, check): "char4.json" → try succeeds → characters.append(char) ✓

Right side panel: final result
  characters = [char1_data, char3_data, char4_data]  ← 3 items
  errors.log: "Пропущен BROKEN.json: ..."

Contrast panel at bottom: LEFT — "Без try/except: один сломанный файл роняет всё". RIGHT — "С паттерном: обрабатываем всё что можем".

Dark Souls analogy: "Как загрузка мира — один регион повреждён, остальные доступны"

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

## Часть 4: Цепочка вызовов — где ловить исключения

Главное правило: **лови там, где можешь что-то сделать**.

Если функция не знает что делать с ошибкой — пусть исключение поднимается выше по цепочке вызовов. Не нужно ловить всё подряд.

```python
def validate_player(data):
    """Проверяет данные. Бросает ValueError если что-то не так."""
    if data.get("level", 0) < 1:
        raise ValueError("Уровень персонажа должен быть >= 1")
    return data

def process_player(filename):
    data, error = safe_load_json(filename)
    if error:
        return None   # не знаем что делать — возвращаем None
    return validate_player(data)   # ValueError пусть поднимается выше

def game_loop():
    player = process_player("save.json")
    if player is None:
        player = create_new_player()   # ← здесь знаем что делать
    print(f"Играем за: {player['name']}")
```

`process_player` не знает — создавать нового персонажа или нет. `game_loop` знает. Поэтому решение принимается на нужном уровне.

Плохой вариант — ловить всё в `process_player` и возвращать None для любой ошибки, включая `ValueError`. Тогда мы теряем информацию о том, что именно пошло не так.

<!--illustration
file: day_4/exception_chain.png
alt: Цепочка вызовов — где ловить исключения: слои архитектуры и подъём исключений наверх
prompt:
Create a Dark RPG UI infographic showing a layered architecture where exceptions propagate up the call chain.

Title: "ЦЕПОЧКА ВЫЗОВОВ — ГДЕ ЛОВИТЬ?" in cream (#e8e0d4).

Three-layer vertical architecture diagram with glass panels:

TOP LAYER (green, widest) — "game_loop()":
  - "Здесь знаем что делать с ошибками"
  - Catches: if player is None → create_new_player()
  - Decision maker icon (crown/orb)

MIDDLE LAYER (indigo) — "process_player(filename)":
  - "Не знаем — пусть поднимается выше"
  - Uses safe_load_json (returns None on error)
  - validate_player raises ValueError → not caught here
  - Question mark icon

BOTTOM LAYER (teal, narrowest) — "validate_player(data) / safe_load_json()":
  - "Бросают исключения / возвращают (data, error)"
  - Raises ValueError if level < 1
  - Detailed code icon

Arrows between layers: exception bubbles UP (amber sparks rising), decisions flow DOWN (teal arrows).

Rule panel at right: "Лови там, где можешь что-то СДЕЛАТЬ. Если не знаешь — пусть поднимается выше."

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

## Задания

**Задание 1.** Напиши функцию `batch_convert(files)`, которая принимает список имён JSON-файлов, загружает каждый через `safe_load_json`, добавляет в нём поле `"converted": True` и сохраняет обратно. Если файл не удалось загрузить — пропускает его, логирует ошибку в `errors.log` и продолжает. В конце выводит: `"Конвертировано: X, пропущено: Y"`.

**Задание 2.** Напиши функцию `retry_input(prompt, converter, attempts=3)`. Она выводит `prompt`, читает строку, применяет к ней `converter` (например `int` или `float`). Если `converter` бросает исключение — выводит `"Неверный ввод, осталось попыток: N"` и пробует снова. После `attempts` неудачных попыток возвращает `None`.

Пример использования:
```python
level = retry_input("Введи уровень: ", int)
# Если пользователь три раза ввёл мусор → level == None
```

**Задание 3 (дебаг-квест).** Найди проблему в этом коде:

```python
def load_game_config(filename):
    try:
        with open(filename) as f:
            config = json.load(f)
        return config
    except Exception:
        return {}   # возвращаем пустой конфиг при любой ошибке

def start_game():
    config = load_game_config("config.json")
    max_players = config["max_players"]   # KeyError если конфиг пустой
    # ... остальная логика
```

Что здесь неправильно? Как исправить?

**Задание 4 (мини-проект).** Напиши функцию `load_all_saves(folder)`, которая:
1. Обходит все `.json` файлы в папке
2. Загружает каждый через `safe_load_json`
3. Рабочие файлы собирает в список `loaded`
4. Повреждённые — логирует в `game_errors.log`
5. В конце возвращает словарь `{"loaded": [...], "failed": ["file1.json", ...]}`
6. После вызова выводит отчёт: сколько загружено, сколько пропущено, имена повреждённых файлов

---

<quiz>
{
  "questions": [
    {
      "question": "Функция возвращает пару (data, error). Что означает результат (None, 'Файл не найден')?",
      "options": [
        "Файл загружен успешно, data = None",
        "Произошла ошибка, data недоступна, error содержит описание",
        "Функция вернула два None",
        "Нужно вызвать функцию ещё раз"
      ],
      "correct": 1,
      "explanation": "В паттерне safe_load: если data == None и error != None — значит операция не удалась. error содержит строку с описанием проблемы."
    },
    {
      "question": "Зачем в safe_save_json после log_error() стоит голый raise без аргументов?",
      "options": [
        "Чтобы создать новое исключение с сообщением из лога",
        "Чтобы пробросить то же исключение дальше, не проглатывая его",
        "Чтобы остановить программу",
        "Чтобы записать ошибку второй раз"
      ],
      "correct": 1,
      "explanation": "Голый raise без аргументов пробрасывает текущее исключение дальше по цепочке вызовов. Мы записали информацию в лог, но не скрыли факт ошибки от вызывающего кода."
    },
    {
      "question": "В цикле по файлам один файл повреждён. Какой паттерн правильный?",
      "options": [
        "Остановить цикл и вернуть пустой список",
        "Обернуть весь цикл в try/except снаружи",
        "Внутри цикла: except → log_error → continue",
        "Игнорировать ошибку без логирования"
      ],
      "correct": 2,
      "explanation": "try/except внутри цикла + continue позволяет пропустить один проблемный элемент и продолжить обработку остальных. log_error гарантирует, что информация о проблеме не потеряется."
    }
  ]
}
</quiz>

---

<!--illustration
file: day_4/skill_tree.png
alt: Дерево навыков Дня 4 — паттерн safe_load, логирование, try/continue в цикле, цепочка вызовов
prompt:
Create a Dark RPG UI skill tree infographic for Day 4 of Week 6 summary.

Title: "НАВЫКИ ДНЯ 4" in cream (#e8e0d4). Subtitle: "Паттерны надёжного кода" in gray-blue (#8ea4b8).

A branching skill tree with 5 circular nodes connected by organic luminous threads:

Center node (largest, indigo glow): gears/pattern icon — "Паттерны"

Branching from center:
- Node 1 (teal): tuple icon — "safe_load (data, error)"
- Node 2 (amber): quill/scroll — "Логирование в файл"
- Node 3 (indigo): loop with skip arrow — "try/continue в цикле"
- Node 4 (teal): layers icon — "Цепочка исключений"

All nodes connected by soft glowing organic lines.

Bottom: a small checklist glass panel:
✓ Паттерн (data, error)
✓ log_error() в файл
✓ try/except + continue
✓ bare raise (не глотаем)
✓ Ловим там, где можем помочь

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

← [[week_6/day_3|День 3]] | [[week_6/day_5|День 5 →]]
