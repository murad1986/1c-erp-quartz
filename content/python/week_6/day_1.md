---
type: lesson
course: "[[python_basics/README]]"
week: 6
day: 1
title: "try/except — первый щит"
concepts: [try/except, ValueError, FileNotFoundError, обработка исключений]
prerequisites: "[\"[[week_5/day_7]]\"]"
tags: [python, ошибки, try, except, исключения]
status: draft
---

# День 1: try/except — первый щит

В Dark Souls программа не падает, когда ты умираешь — она обрабатывает смерть как событие: воспроизводит анимацию, показывает надпись YOU DIED, возвращает тебя к костру. Это не баг, это запланированный исход.

В обычной программе любая ошибка — неверный ввод пользователя, отсутствующий файл, несуществующий ключ в словаре — роняет программу полностью. `try/except` — это твой план Б. Это щит, который принимает удар вместо тебя.

---

## Часть 1: Что такое исключение

Когда Python встречает ситуацию, с которой не может справиться, он **кидает исключение** — специальный объект ошибки. Если никто его не поймает, программа падает и показывает **трейсбек** (traceback) — длинное сообщение об ошибке.

Вот как выглядит падение программы:

```python
# Пользователь вводит "abc" вместо числа
number = int(input("Введи число: "))
print(f"Твоё число: {number}")

# → ValueError: invalid literal for int() with base 10: 'abc'
# Вся программа остановилась. Строка с print не выполнилась.
```

Трейсбек говорит тебе:
- **Где** упало — имя файла и номер строки
- **Что** упало — тип исключения (`ValueError`)
- **Почему** упало — текст ошибки (`invalid literal for int()...`)

Это не страшно. Трейсбек — твой друг, он показывает точное место проблемы. Но пользователю такое показывать нельзя.

<!--illustration
file: day_1/exception_types.png
alt: Карта типов исключений — ValueError, FileNotFoundError, KeyError, TypeError с примерами
prompt:
Create a Dark RPG UI infographic showing a visual map of common Python exception types.

Title: "ТИПЫ ИСКЛЮЧЕНИЙ — КАРТА УГРОЗ" in cream (#e8e0d4). Subtitle: "у каждой ошибки — своё имя" in gray-blue.

Four glass-morphism cards arranged in a 2x2 grid, each representing an exception type:

TOP-LEFT (teal): ValueError — "Неверное значение"
- Icon: crossed number symbol
- Trigger: int("abc") — highlighted in amber
- Example: invalid literal for int() with base 10: 'abc'

TOP-RIGHT (indigo): FileNotFoundError — "Файл не найден"
- Icon: broken folder/scroll
- Trigger: open("save_slot_1.json")
- Example: No such file or directory: 'save_slot_1.json'

BOTTOM-LEFT (amber): KeyError — "Ключ не найден"
- Icon: missing key symbol
- Trigger: player["gold"] when "gold" not in dict
- Example: KeyError: 'gold'

BOTTOM-RIGHT (indigo, softer): TypeError — "Неверный тип"
- Icon: type mismatch symbol (str vs int)
- Trigger: "уровень" + 42
- Example: can only concatenate str (not "int") to str

Connecting lines between cards showing they are all children of Exception. Central background label: "Exception" as a dim parent node.

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

## Часть 2: Синтаксис try/except

`try` — это «попробуй выполнить». `except` — это «если что-то пошло не так — делай вот это».

```python
try:
    number = int(input("Введи число: "))
    print(f"Твоё число: {number}")
except ValueError:
    print("Это не число! Попробуй ещё раз.")

# Если ввести "abc":
# → Это не число! Попробуй ещё раз.
# Программа продолжает работу — не падает
```

Аналогия: `try` — это «попробуй открыть сундук». `except` — это «если сундук заперт — сделай вот это, не стой столбом».

Важно: `except ValueError` ловит **только** `ValueError`. Другие типы ошибок пройдут мимо и всё равно уронят программу. Это правильно — не нужно глушить все ошибки подряд.

<!--illustration
file: day_1/try_except_anatomy.png
alt: Анатомия try/except — блок-схема: try → исключение? → except → программа продолжает
prompt:
Create a Dark RPG UI infographic showing the anatomy of a try/except block as a flowchart.

Title at top: "АНАТОМИЯ try/except" in warm cream (#e8e0d4). Subtitle: "щит между кодом и катастрофой" in muted gray-blue (#8ea4b8).

Four connected glass-morphism panels flowing top to bottom, connected by organic glowing lines:

PANEL 1 (teal border): labeled "try:" — "Опасный код"
- Shield icon on left
- Code inside: number = int(input("Введи число: ")) in teal monospace
- Description: "Пробуем выполнить"

PANEL 2 (amber border, split): diamond decision shape labeled "Исключение?"
- LEFT branch (YES, amber): arrow labeled "ValueError кинуто" curves to Panel 3
- RIGHT branch (NO, green): arrow labeled "всё хорошо" curves to Panel 4

PANEL 3 (indigo border): labeled "except ValueError:" — "Обработчик"
- Caught icon (net/shield catching a spark)
- Code: print("Это не число!") in cream monospace
- Description: "Ловим — программа живёт"

PANEL 4 (green #7bc88f border): labeled "продолжение"
- Check mark icon
- Description: "Программа продолжает работу"
- Arrow flows down

Bottom contrast panel: LEFT side dim red — traceback crash (no try/except). RIGHT side teal — graceful handling (with try/except).

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

<!--illustration
file: day_1/no_crash_comparison.png
alt: До и после — программа падает без try/except vs обрабатывает ошибку с try/except
prompt:
Create a Dark RPG UI infographic comparing program crash vs graceful error handling.

Title: "БЕЗ ЗАЩИТЫ vs С ЗАЩИТОЙ" in cream (#e8e0d4).

TWO large panels side by side:

LEFT panel (dim, reddish tint, cracked frame) — labeled "Без try/except":
- Skull icon at top
- Code panel showing:
  number = int(input("Введи число: "))
  print(f"Твоё число: {number}")
- Red traceback output box:
  ValueError: invalid literal
  for int() with base 10: 'abc'
  Program stopped!
- "ПРОГРАММА УПАЛА" label in amber
- Crack/shatter effect on the panel edges

RIGHT panel (teal, clean) — labeled "С try/except":
- Shield icon at top
- Code panel showing:
  try:
    number = int(input("Введи число: "))
  except ValueError:
    print("Это не число!")
- Green output box:
  → Это не число! Попробуй ещё раз.
  (программа продолжает работу)
- "ПРОГРАММА ЖИВЁТ" label in green #7bc88f
- Check mark, clean glow

Large dark souls-style YOU DIED text in dim red on the left panel. CONTINUE? text in teal on the right.

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

## Часть 3: FileNotFoundError — файл не найден

Один из самых частых случаев — попытка открыть файл, которого нет. В игровом коде это классика: сейв-файл пропал, конфиг удалили.

```python
import json

def load_save(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден — начинаем новую игру")
        return None

result = load_save("save_slot_1.json")
# → Файл save_slot_1.json не найден — начинаем новую игру
# result = None
```

Функция не падает. Она возвращает `None` — сигнал «данных нет». Вызывающий код сам решит, что делать с `None`.

---

## Часть 4: KeyError — ключ не найден

Словарь есть, но ключа в нём нет — тоже исключение. Например, загрузил старый сейв, где ещё не было поля `"gold"`.

```python
player = {"name": "Artorias", "level": 52}

try:
    print(player["gold"])    # ключа "gold" нет в словаре
except KeyError:
    print("Нет такого поля в данных персонажа")
    player["gold"] = 0       # добавляем со значением по умолчанию

print(f"Золото: {player['gold']}")
# → Нет такого поля в данных персонажа
# → Золото: 0
```

Это называется **обратная совместимость** — старые данные работают с новым кодом.

---

## Задания

### Задание 1: safe_int_input

Напиши функцию `safe_int_input(prompt)`, которая выводит подсказку, принимает ввод пользователя и возвращает число. Если пользователь ввёл не число — возвращает `None`.

```python
def safe_int_input(prompt):
    # твой код здесь
    pass

result = safe_int_input("Введи уровень персонажа: ")
if result is None:
    print("Некорректный ввод")
else:
    print(f"Уровень: {result}")
```

### Задание 2: safe_load_json

Напиши функцию `safe_load_json(filename)`, которая открывает JSON-файл и возвращает данные. Если файл не найден — возвращает `None` и выводит сообщение.

```python
def safe_load_json(filename):
    # твой код здесь
    pass
```

### Задание 3: Дебаг-квест

Найди все места, где программа может упасть, и добавь обработку:

```python
def get_player_level(save_filename):
    with open(save_filename) as f:
        data = json.load(f)
    level = int(data["level"])
    return level
```

Подсказка: как минимум два разных исключения.

### Задание 4 (мини-проект): Ввод данных персонажа

Напиши программу, которая запрашивает у пользователя:
- Имя персонажа (строка)
- Уровень (число от 1 до 100)
- Класс (воин / маг / вор)

Программа не должна падать ни на каком вводе. При неверном вводе — выводи понятное сообщение. В конце выводи итоговые данные персонажа.

---

<quiz>
**Вопрос 1:** Что такое исключение в Python?

- [ ] Синтаксическая ошибка в коде
- [x] Объект ошибки, который Python создаёт когда что-то пошло не так во время выполнения
- [ ] Предупреждение, которое не останавливает программу
- [ ] Специальный тип переменной

**Объяснение:** Исключение — это объект, который Python "бросает" при проблеме во время выполнения. Синтаксические ошибки (пропущенные двоеточия, неверные отступы) — это другой вид ошибок, они возникают ещё до запуска программы.
</quiz>

<quiz>
**Вопрос 2:** Когда нужен try/except?

- [ ] Всегда — нужно оборачивать весь код
- [ ] Никогда — Python сам разбирается с ошибками
- [x] Когда операция может не сработать по внешним причинам: неверный ввод, отсутствующий файл
- [ ] Только при работе с числами

**Объяснение:** try/except нужен когда ты знаешь, что что-то может пойти не так, но это не ошибка в коде — а внешнее обстоятельство. Оборачивать весь код — плохая практика, это скроет настоящие баги.
</quiz>

<quiz>
**Вопрос 3:** Что значит, что исключение "поймано"?

- [ ] Программа всё равно падает, но красиво
- [ ] Python игнорирует ошибку и продолжает как ни в чём не бывало
- [x] Блок except выполнился вместо падения программы, и выполнение продолжается дальше
- [ ] Исключение записывается в лог-файл

**Объяснение:** Когда исключение поймано — это значит нашёлся подходящий `except` блок. Он выполнился, и программа продолжила работу со следующей строки после всей конструкции try/except. Это и есть смысл обработки ошибок.
</quiz>

---

<!--illustration
file: day_1/skill_tree.png
alt: Дерево навыков Дня 1 — try/except, типы исключений, безопасный ввод
prompt:
Create a Dark RPG UI skill tree infographic for Day 1 of Week 6 summary.

Title: "НАВЫКИ ДНЯ 1" in cream (#e8e0d4). Subtitle: "try/except — первый щит" in gray-blue (#8ea4b8).

A branching skill tree with 5 circular nodes connected by organic luminous threads:

Center node (largest, teal glow): shield icon — "try/except"

Branching from center:
- Node 1 (teal): exclamation icon — "Что такое исключение"
- Node 2 (teal): [ValueError] label — "Типы ошибок"
- Node 3 (indigo): folder with X — "FileNotFoundError"
- Node 4 (indigo): key with X — "KeyError"

All nodes connected by soft glowing organic lines. Each node has a small Russian label.

Bottom: a small checklist glass panel:
✓ try/except синтаксис
✓ ValueError (неверный ввод)
✓ FileNotFoundError (файл)
✓ KeyError (словарь)
✓ программа не падает

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

← [[week_5/day_7|День 5.7]] | [[week_6/day_2|День 6.2 →]]
