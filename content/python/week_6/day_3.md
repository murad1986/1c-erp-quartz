---
type: lesson
course: "python"
week: 6
day: 3
title: "raise — бросаем исключения сами"
concepts: [raise, валидация входных данных, raise ValueError, правила defensive programming]
prerequisites: "[\"[week_6/day_2](/python/week_6/day_2/)\"]"
tags: [python, ошибки, raise, валидация, defensive-programming]
status: draft
---

# День 3: raise — бросаем исключения сами

До сих пор мы только ловили исключения, которые кидал Python. Но иногда нужно самим сигнализировать об ошибке — ещё до того, как произойдёт что-то плохое.

Представь функцию `level_up(char, levels)`. Если ей передать `-5` уровней — что должно случиться? Молча прибавить -5 к уровню? Это хуже, чем ошибка — это скрытый баг. Функция должна крикнуть: "Стоп, так нельзя!" Для этого существует `raise`.

---

## Часть 1: raise — синтаксис

`raise` бросает исключение прямо из твоего кода. Чаще всего используют `ValueError` — для "неверного значения аргумента".

```python
def level_up(char, levels):
    if levels <= 0:
        raise ValueError(f"Уровней должно быть > 0, получено: {levels}")
    char["level"] += levels
    return char

player = {"name": "Chosen Undead", "level": 10}

try:
    level_up(player, -5)
except ValueError as e:
    print(f"Ошибка: {e}")

# → Ошибка: Уровней должно быть > 0, получено: -5
# player["level"] остался 10 — ничего не сломалось
```

Обрати внимание: функция бросает исключение, а вызывающий код его ловит. Это разделение обязанностей — функция отвечает за то, что данные правильные, а вызывающий код — за то, что делать с ошибкой.

<!--illustration
file: day_3/raise_flow.png
alt: Поток raise — функция кидает ValueError, вызывающий код ловит через try/except
prompt:
Create a Dark RPG UI infographic showing the raise flow between a function and its caller.

Title: "raise — КАК РАБОТАЕТ" in cream (#e8e0d4).

Two-column layout connected by flowing arrows:

LEFT column — "Функция" (teal):
  Glass panel: "level_up(char, levels)"
  ↓ diamond: "levels <= 0?"
  YES branch (amber): raise ValueError(
      f"Уровней должно быть > 0, получено: {levels}"
  )
  - "Бросаем исключение" label
  - Fire/spark icon shooting upward (exception propagating)

CENTER: large glowing upward arrow labeled "исключение поднимается"

RIGHT column — "Вызывающий код" (indigo):
  Glass panel showing:
  try:
      level_up(player, -5)
  except ValueError as e:
      print(f"Ошибка: {e}")
  - "Ловим исключение" label
  - Shield/net icon catching the spark

Bottom output panel:
  → Ошибка: Уровней должно быть > 0, получено: -5
  → player["level"] остался 10 ✓

Key insight note: "Функция отвечает за данные. Вызывающий — за обработку ошибки."

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

## Часть 2: Валидация входных данных

Валидация — это проверка данных перед тем, как что-то с ними делать. Проверять нужно на "границах" системы: пользовательский ввод, данные из файлов, аргументы публичных функций.

```python
def create_character(name, char_class, level=1):
    if not name or not name.strip():
        raise ValueError("Имя персонажа не может быть пустым")
    if char_class not in ("воин", "маг", "вор"):
        raise ValueError(f"Неверный класс: {char_class}. Доступны: воин, маг, вор")
    if level < 1 or level > 100:
        raise ValueError(f"Уровень должен быть от 1 до 100, получено: {level}")
    return {"name": name.strip(), "class": char_class, "level": level}
```

Что происходит с неверными данными:

```python
try:
    hero = create_character("", "маг", 50)
except ValueError as e:
    print(f"Ошибка создания: {e}")
# → Ошибка создания: Имя персонажа не может быть пустым
```

Такой подход называется **defensive programming** — защитное программирование. Функция сама защищает себя от плохих данных.

<!--illustration
file: day_3/validation_pattern.png
alt: До и после — функция без валидации vs функция с raise: скрытый баг vs быстрое падение
prompt:
Create a Dark RPG UI infographic comparing functions without vs with input validation using raise.

Title: "ВАЛИДАЦИЯ: БЕЗ raise vs С raise" in cream (#e8e0d4).

TWO large panels side by side:

LEFT panel (dim, amber warning) — "Без валидации":
- Skull/broken icon at top
- Code:
  def level_up(char, levels):
      char["level"] += levels  # -5 пройдёт тихо!
      return char
- Problem: level_up(player, -5) → player["level"] = 5
- Hidden bug: no error shown, wrong state silently set
- Label: "Скрытый баг — уровень уменьшился"
- Dim cracked panel

RIGHT panel (teal, clean) — "С raise":
- Shield icon at top
- Code:
  def level_up(char, levels):
      if levels <= 0:
          raise ValueError(
              f"Уровней должно быть > 0, получено: {levels}"
          )
      char["level"] += levels
- Benefit: fails fast with clear message
- Label: "Падает сразу с понятным сообщением"
- "Defensive programming" badge

Bottom rule panel: "raise нужен когда продолжать работу с такими данными БЕССМЫСЛЕННО или ОПАСНО"

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

## Часть 3: raise без аргументов — перебросить исключение

Иногда нужно поймать исключение, сделать что-то дополнительное (например, вывести сообщение), а потом отправить его дальше — не гасить. Голый `raise` без аргументов перебрасывает текущее исключение.

```python
import json

def load_critical_config(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"КРИТИЧЕСКИЙ ФАЙЛ КОНФИГУРАЦИИ НЕ НАЙДЕН: {filename}")
        raise   # перебросить исходное FileNotFoundError дальше

# Вызывающий код получит FileNotFoundError
# и увидит наше сообщение в консоли
```

Это нужно когда функция не может справиться с ошибкой сама, но хочет оставить след — сообщение, запись в лог — перед тем как пустить ошибку дальше.

<!--illustration
file: day_3/bare_raise.png
alt: Голый raise — поймать, залогировать и перебросить то же исключение дальше
prompt:
Create a Dark RPG UI infographic showing bare raise (re-raise) pattern inside an except block.

Title: "Голый raise — ПРОБРОСИТЬ ДАЛЬШЕ" in cream (#e8e0d4).

A three-step vertical flow:

STEP 1 (teal): Exception occurs
- "FileNotFoundError кинуто" label
- Spark/fire icon

STEP 2 (indigo): except block catches it
  except FileNotFoundError:
      print(f"КРИТИЧЕСКИЙ ФАЙЛ НЕ НАЙДЕН: {filename}")
      raise   ← bare raise, no arguments
- "Ловим, логируем, отпускаем" label
- Net icon catching the spark, then releasing it upward

STEP 3 (amber): same exception propagates up
- Same FileNotFoundError continues to caller
- "То же исключение — выше по цепочке" label
- Calling code can still catch it

Right side annotation panel:
- "raise" with arguments = create NEW exception
- bare "raise" = re-throw CURRENT exception unchanged
- Use case: "Хочу залогировать, но не глотать"

Bottom code example:
def load_critical_config(filename):
    try:
        with open(filename) as f: return json.load(f)
    except FileNotFoundError:
        print(f"КРИТИЧЕСКИЙ ФАЙЛ НЕ НАЙДЕН: {filename}")
        raise   # пробрасываем дальше

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

## Часть 4: Когда НЕ нужен raise

`raise` — это сильный инструмент, но не нужно использовать его везде. Есть ситуации, где лучше вернуть `None` или значение по умолчанию.

**Не нужен raise:**

```python
# Плохо — raise там, где проще вернуть None
def find_item(inventory, item_name):
    for item in inventory:
        if item == item_name:
            return item
    raise ValueError(f"Предмет {item_name} не найден")  # лишнее

# Лучше — просто вернуть None, отсутствие предмета — не ошибка
def find_item(inventory, item_name):
    for item in inventory:
        if item == item_name:
            return item
    return None   # понятно и без исключения
```

**Нужен raise:**

```python
# Продолжать работу с отрицательным здоровьем — бессмысленно и опасно
def set_health(char, hp):
    if hp < 0:
        raise ValueError(f"HP не может быть отрицательным: {hp}")
    char["hp"] = hp
```

Правило: `raise` нужен когда продолжать работу с такими данными **бессмысленно или опасно**. Если ситуация нормальная (предмет просто не нашёлся) — верни `None`.

---

## Задания

### Задание 1: add_item

Напиши функцию `add_item(inventory, item, max_size=20)`:
- Добавляет предмет в список инвентаря
- Если инвентарь полон — бросает `ValueError` с понятным сообщением
- Если `item` пустая строка — тоже бросает `ValueError`

```python
def add_item(inventory, item, max_size=20):
    # твой код здесь
    pass

bag = ["меч", "щит"]
try:
    add_item(bag, "зелье")
    print(bag)    # → ['меч', 'щит', 'зелье']
    add_item(bag, "")
except ValueError as e:
    print(f"Ошибка: {e}")
```

### Задание 2: Дебаг-квест

В коде ниже `raise` используется неверно. Найди все проблемы и объясни почему это плохо:

```python
def validate_age(age):
    if age > 0:
        raise ValueError("Возраст положительный — продолжаем")
    if age < 0:
        print("Отрицательный возраст")
    if age > 150:
        raise ValueError("Слишком старый")
    return age
```

Подсказка: одна проблема с логикой raise, одна — с порядком проверок.

### Задание 3: set_player_stat

Напиши функцию `set_player_stat(player, stat, value)` с полной валидацией:
- `stat` должен быть одним из: `"hp"`, `"level"`, `"gold"`
- `"hp"` — от 1 до 1000
- `"level"` — от 1 до 100
- `"gold"` — от 0 и выше (не отрицательное)

```python
def set_player_stat(player, stat, value):
    # твой код здесь
    pass

hero = {"hp": 100, "level": 1, "gold": 0}
try:
    set_player_stat(hero, "level", 150)
except ValueError as e:
    print(f"Ошибка: {e}")
# → Ошибка: level должен быть от 1 до 100, получено: 150
```

### Задание 4 (мини-проект): Полная create_character

Напиши функцию `create_character(name, char_class, level)` с валидацией всех полей. Затем напиши код, который запрашивает у пользователя данные через `input()` и обрабатывает все возможные ошибки через `try/except`.

Требования:
- Имя: не пустое, не длиннее 30 символов
- Класс: только из списка `["воин", "маг", "вор", "лучник"]`
- Уровень: целое число от 1 до 100
- При любой ошибке — понятное сообщение, программа не падает

```python
def create_character(name, char_class, level):
    # твой код с raise
    pass

# Основной код с try/except для пользовательского ввода
```

---

<quiz>
**Вопрос 1:** Когда лучше использовать raise, а когда вернуть None?

- [ ] raise всегда лучше — он явно сигнализирует об ошибке
- [ ] None всегда лучше — не нужно усложнять код
- [x] raise — когда продолжать работу с такими данными опасно или бессмысленно; None — когда отсутствие результата нормальная ситуация
- [ ] Зависит от длины функции

**Объяснение:** Если предмет не нашёлся в инвентаре — это нормально, вернём `None`. Если функции передали отрицательное здоровье — это ошибка в логике программы, нужен `raise`. Главный вопрос: "это штатная ситуация или недопустимое состояние?"
</quiz>

<quiz>
**Вопрос 2:** Что делает raise без аргументов?

- [ ] Создаёт новое пустое исключение
- [ ] Вызывает ошибку синтаксиса
- [x] Перебрасывает текущее активное исключение дальше
- [ ] Останавливает программу без сообщения

**Объяснение:** Голый `raise` внутри блока `except` перебрасывает то исключение, которое сейчас обрабатывается. Это нужно когда хочешь что-то сделать (например, залогировать) перед тем как пустить ошибку дальше.
</quiz>

<quiz>
**Вопрос 3:** Чем отличается raise ValueError от raise Exception?

- [ ] Ничем, это синонимы
- [x] ValueError более конкретный — говорит что проблема в значении аргумента; Exception слишком общий
- [ ] Exception можно ловить, ValueError нельзя
- [ ] ValueError только для чисел

**Объяснение:** В Python есть иерархия исключений. `Exception` — общий родитель. `ValueError` — конкретный потомок, который говорит "аргумент имеет неверное значение". Использовать конкретный тип лучше: вызывающий код может поймать именно `ValueError` и знать что именно пошло не так.
</quiz>

---

<!--illustration
file: day_3/skill_tree.png
alt: Дерево навыков Дня 3 — raise, валидация, голый raise, defensive programming
prompt:
Create a Dark RPG UI skill tree infographic for Day 3 of Week 6 summary.

Title: "НАВЫКИ ДНЯ 3" in cream (#e8e0d4). Subtitle: "raise — бросаем исключения сами" in gray-blue (#8ea4b8).

A branching skill tree with 5 circular nodes connected by organic luminous threads:

Center node (largest, amber glow): throwing/launching icon — "raise"

Branching from center:
- Node 1 (teal): lightning bolt — "raise ValueError('...')"
- Node 2 (teal): shield — "Валидация входных данных"
- Node 3 (indigo): re-throw arrow — "Голый raise (перебросить)"
- Node 4 (indigo): scale icon — "Когда raise, когда None"

All nodes connected by soft glowing organic lines.

Bottom: a small checklist glass panel:
✓ raise ValueError("сообщение")
✓ if conditions → raise
✓ Defensive programming
✓ bare raise внутри except
✓ raise vs return None

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

← [День 6.2](/python/week_6/day_2/) | [День 6.4 →](/python/week_6/day_4/)
