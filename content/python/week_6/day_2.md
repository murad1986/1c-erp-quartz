---
type: lesson
course: "python"
week: 6
day: 2
title: "except по типу, else и finally"
concepts: [except конкретного типа, несколько except, else блок, finally блок]
prerequisites: "[\"[week_6/day_1](/python/week_6/day_1/)\"]"
tags: [python, ошибки, except, else, finally]
status: draft
---

# День 2: except по типу, else и finally

Вчера мы ловили одно исключение. Но что если может случиться несколько разных проблем? Файл не найден — одно. Файл есть, но содержимое сломано — другое. Нет прав на чтение — третье. Каждое требует своей реакции.

Это как боссфайт с несколькими фазами: на каждую фазу — своя тактика. Один `except` на всё — это стоять и тыкать мечом в надежде на лучшее.

---

## Часть 1: Несколько except блоков

После одного `try` можно написать несколько `except` — для разных типов исключений. Python проверяет их по очереди и останавливается на первом подходящем.

```python
import json

def load_player(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("Файл сейва не найден — новая игра")
        return None
    except json.JSONDecodeError:
        print("Файл повреждён — невозможно загрузить")
        return None
    except PermissionError:
        print("Нет прав на чтение файла")
        return None
```

Каждый `except` — отдельная реакция на конкретную проблему. Читателю кода сразу понятно, что именно может пойти не так.

<!--illustration
file: day_2/multiple_except_flow.png
alt: Схема потока try/except/else/finally с несколькими ветками except
prompt:
Create a Dark RPG UI infographic showing the complete try/except/else/finally flow as a flowchart.

Title: "ПОЛНАЯ СХЕМА: try/except/else/finally" in cream (#e8e0d4).

Top-to-bottom flowchart with glass-morphism panels:

START: "try:" panel (teal) — "Основной код"
  ↓ diamond: "Исключение?"

YES branch (amber, goes right):
  → "FileNotFoundError?" → YES → except FileNotFoundError panel (indigo): "Новая игра"
  → "JSONDecodeError?" → YES → except json.JSONDecodeError panel (indigo): "Файл повреждён"
  → "Другое?" → YES → except Exception as e panel (dim): "Неожиданная ошибка"

NO branch (green, goes left):
  → "else:" panel (green #7bc88f): "Только если try успешен — показать данные"

BOTH branches converge at:
  → "finally:" panel (amber glow): "ВСЕГДА — запись лога, сообщение о завершении"
  → arrow down: "Программа продолжает"

Labels on the right margin: "1. try → 2. except ИЛИ else → 3. finally"

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

## Часть 2: except Exception as e — поймать всё

`Exception` — это "родитель" почти всех исключений. Поймать его значит поймать всё что угодно. Это иногда нужно — но опасно.

```python
try:
    data = load_player("save.json")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")
    # → Неожиданная ошибка: [Errno 2] No such file or directory: 'save.json'
```

Конструкция `as e` сохраняет объект исключения в переменную `e`. Через `e` можно получить текст ошибки.

**Правило:** ловить конкретное исключение всегда лучше, чем ловить всё подряд. `except Exception` — это крайний случай, когда ты действительно не знаешь, что может случиться, и хочешь хотя бы залогировать.

<!--illustration
file: day_2/except_as_e.png
alt: except Exception as e — доступ к тексту и типу исключения через str(e) и type(e).__name__
prompt:
Create a Dark RPG UI infographic showing how to access exception details with "except Exception as e".

Title: "except Exception as e — ДЕТАЛИ ОШИБКИ" in cream (#e8e0d4).

Central large code panel with annotated parts:

except Exception as e:
    print(f"Ошибка: {e}")
    print(type(e).__name__)

Three labeled annotation arrows pointing to code elements:
- "Exception" → label: "Тип для перехвата" (teal)
- "as e" → label: "Сохраняем объект исключения" (amber)
- "e" in print → label: "Текст ошибки" (indigo)
- "type(e).__name__" → label: "Имя класса ошибки" (indigo)

Below: two output glass panels side by side:

LEFT (str(e)):
- Input: FileNotFoundError raised
- Output: "[Errno 2] No such file or directory: 'save.json'"
- Label: "str(e) — текстовое описание"

RIGHT (type(e).__name__):
- Input: same exception
- Output: "FileNotFoundError"
- Label: "имя типа — для логов"

Bottom note: "Exception — родитель почти всех исключений. Лови конкретное там где можешь, Exception — крайний случай."

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

## Часть 3: else — код при успехе

Блок `else` выполняется, только если `try` прошёл без единого исключения. Это удобно: код "успешного пути" отделён от кода обработки ошибок.

```python
import json

try:
    with open("save.json", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Новая игра — файл не найден")
    data = None
else:
    print(f"Загружен сейв: {data['name']}, уровень {data['level']}")
    # Эта строка выполняется ТОЛЬКО если open и json.load сработали без ошибок

# → Загружен сейв: Artorias, уровень 52
```

Аналогия: `else` — это "если сундук открылся без проблем — бери лут". Не нужно писать это внутри `try`, потому что там только "опасный" код.

---

## Часть 4: finally — код в любом случае

`finally` выполняется **всегда** — и если всё прошло хорошо, и если случилась ошибка. Его используют для действий, которые нужны в любом исходе: закрыть файл, записать лог, сообщить о завершении операции.

```python
import json

def save_with_log(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Сохранено успешно")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
    finally:
        print("Попытка сохранения завершена")
        # Эта строка выполнится всегда — и при успехе, и при ошибке
```

Порядок выполнения всей конструкции:
1. `try` — основной код
2. `except` — если было исключение
3. `else` — если исключения не было
4. `finally` — всегда

<!--illustration
file: day_2/else_finally_analogy.png
alt: Игровая аналогия: else — бонус за уровень без смертей, finally — сохранение всегда
prompt:
Create a Dark RPG UI infographic showing else and finally through an RPG game level analogy.

Title: "else И finally — ИГРОВАЯ АНАЛОГИЯ" in cream (#e8e0d4).

Two large glass-morphism panels:

LEFT panel (green teal border) — labeled "else:"
- RPG trophy/bonus chest icon at top (glowing amber)
- Main text: "Если уровень пройден без смертей — получи бонус"
- Python connection: "Выполняется ТОЛЬКО если try прошёл без ошибок"
- Code example: else: print(f"Загружен сейв: {data['name']}")
- Visual: a victory banner, stars, bonus loot falling
- Subtitle: "Путь победителя"

RIGHT panel (amber border) — labeled "finally:"
- Progress save / bonfire icon at top (warm amber glow)
- Main text: "Конец уровня — всегда сохраняем прогресс"
- Python connection: "Выполняется ВСЕГДА — и при ошибке, и без неё"
- Code example: finally: print("Попытка сохранения завершена")
- Visual: a bonfire saving, regardless of player state
- Subtitle: "Гарантированный финал"

Between panels: vertical separator with icons: success path → LEFT, failure path → RIGHT, BOTH → merge at finally.

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

### Задание 1: safe_divide

Напиши функцию `safe_divide(a, b)`, которая делит `a` на `b`. Обработай:
- `ZeroDivisionError` — деление на ноль
- `TypeError` — если передали не числа (например, строку)

```python
def safe_divide(a, b):
    # твой код здесь
    pass

print(safe_divide(10, 2))    # → 5.0
print(safe_divide(10, 0))    # → None (и сообщение об ошибке)
print(safe_divide(10, "x"))  # → None (и сообщение об ошибке)
```

### Задание 2: Загрузчик конфига

Напиши функцию `load_config(filename)` с тремя `except` (для `FileNotFoundError`, `json.JSONDecodeError`, `KeyError`) и блоком `else`, который выводит успешно загруженные данные.

```python
import json

def load_config(filename):
    # Ожидаемый формат конфига: {"version": "1.0", "language": "ru"}
    # твой код здесь
    pass
```

### Задание 3: Дебаг-квест

Найди проблему в этом коде и объясни, почему `finally` здесь мешает:

```python
def read_number_from_file(filename):
    try:
        with open(filename) as f:
            number = int(f.read().strip())
        return number
    except ValueError:
        return None
    finally:
        return -1    # проблема здесь — почему?
```

Что вернёт функция, если файл содержит "42"? А если "abc"? А если файл не найден? Исправь код.

### Задание 4 (мини-проект): load_or_create

Напиши функцию `load_or_create(filename, defaults)`:
- Загружает JSON из файла
- Если файл не найден — создаёт его с данными из `defaults`
- Если файл повреждён — выводит предупреждение и использует `defaults`
- Использует `else` и `finally` осмысленно
- Всегда возвращает словарь

```python
import json

def load_or_create(filename, defaults):
    # твой код здесь
    pass

player = load_or_create("hero.json", {"name": "Безымянный", "level": 1})
print(player)
```

---

<quiz>
**Вопрос 1:** В каком порядке выполняются блоки try/except/else/finally?

- [ ] try → else → except → finally
- [x] try → except (если была ошибка) → else (если ошибки не было) → finally
- [ ] try → finally → except → else
- [ ] try → except → finally → else

**Объяснение:** Сначала выполняется `try`. Если возникло исключение — выполняется подходящий `except`, иначе выполняется `else`. В конце всегда выполняется `finally`, независимо от исхода.
</quiz>

<quiz>
**Вопрос 2:** Когда выполняется блок else?

- [ ] Всегда, как и finally
- [ ] Только если было поймано исключение
- [x] Только если в блоке try не возникло ни одного исключения
- [ ] Только если except не нашёл подходящего типа

**Объяснение:** `else` — это "путь успеха". Он выполняется когда `try` прошёл чисто, без исключений. Если было исключение (даже пойманное через `except`) — `else` не выполняется.
</quiz>

<quiz>
**Вопрос 3:** Когда выполняется блок finally?

- [ ] Только если было исключение
- [ ] Только если исключений не было
- [ ] Только если except поймал исключение
- [x] Всегда — и при ошибке, и без неё

**Объяснение:** `finally` выполняется в любом случае. Это гарантия: код внутри `finally` запустится всегда, даже если произошла ошибка которую никто не поймал. Поэтому туда пишут "уборку" — закрытие файлов, запись лога.
</quiz>

---

<!--illustration
file: day_2/skill_tree.png
alt: Дерево навыков Дня 2 — несколько except, else, finally, except as e
prompt:
Create a Dark RPG UI skill tree infographic for Day 2 of Week 6 summary.

Title: "НАВЫКИ ДНЯ 2" in cream (#e8e0d4). Subtitle: "except, else, finally" in gray-blue (#8ea4b8).

A branching skill tree with 5 circular nodes connected by organic luminous threads:

Center node (largest, teal glow): branching paths icon — "Множество except"

Branching from center:
- Node 1 (teal): three branches icon — "Несколько except"
- Node 2 (green #7bc88f): trophy icon — "else — путь успеха"
- Node 3 (amber): bonfire icon — "finally — всегда"
- Node 4 (indigo): magnifier on "e" — "except as e"

All nodes connected by soft glowing organic lines.

Bottom: a small checklist glass panel:
✓ except FileNotFoundError / JSONDecodeError
✓ except Exception as e
✓ str(e) и type(e).__name__
✓ else — только при успехе
✓ finally — всегда

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

← [День 6.1](/python/week_6/day_1/) | [День 6.3 →](/python/week_6/day_3/)
