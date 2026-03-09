---
type: lesson
course: "python"
week: 6
day: 5
title: "Свои исключения"
concepts: [class MyError(Exception), иерархия исключений, raise MyError, когда нужны свои исключения]
prerequisites: "[\"[week_6/day_4](/python/week_6/day_4/)\"]"
tags: [python, ошибки, исключения, класс, иерархия]
status: draft
---

# День 5: Свои исключения

Встроенные исключения — `ValueError`, `FileNotFoundError`, `KeyError` — универсальные. Они описывают **тип** ошибки, но не **контекст**.

Представь: ты пишешь RPG-менеджер. Что-то пошло не так с персонажем. Ты видишь `ValueError: invalid literal for int()`. Это... где? В уровне? В хите? В идентификаторе предмета? Не ясно.

А теперь представь, что видишь `CharacterError: Уровень персонажа не может быть отрицательным`. Сразу понятно.

Вот зачем нужны **свои исключения** — они делают код говорящим.

> В Dark Souls у каждого типа смерти — своя анимация и надпись. "YOU DIED", "VICTORY ACHIEVED", "HEIR OF FIRE DESTROYED". Игра не просто говорит "что-то произошло" — она точно объясняет что именно.

---

## Часть 1: Простейший класс исключения

Сегодня первый раз видишь слово `class`. Не пугайся — в Week 7 разберём его полностью. Сейчас просто запомни шаблон: так создаётся "свой тип ошибки".

```python
# Создаём своё исключение — шаблон, полное объяснение в Week 7
class CharacterError(Exception):
    pass   # пока пустой — наследует всё от Exception
```

Всё. Это рабочее исключение. Его можно `raise`, его можно ловить в `except`.

```python
def load_character(name):
    if not name.strip():
        raise CharacterError("Имя персонажа не может быть пустым")
    return {"name": name, "level": 1}

try:
    load_character("")
except CharacterError as e:
    print(f"Ошибка персонажа: {e}")
    # → Ошибка персонажа: Имя персонажа не может быть пустым
```

`CharacterError` ведёт себя точно как `ValueError` или `FileNotFoundError` — потому что все они наследуют от `Exception`. Ты просто добавил новое имя в эту семью.

<!--illustration
file: day_5/custom_exception_anatomy.png
alt: Анатомия class CharacterError(Exception) — что означает каждая часть объявления
prompt:
Create a Dark RPG UI infographic showing the anatomy of a custom exception class definition.

Title: "АНАТОМИЯ СВОЕГО ИСКЛЮЧЕНИЯ" in cream (#e8e0d4).

Central large annotated code block:

class CharacterError(Exception):
    pass

Each part labeled with annotation arrows:

- "class" (teal keyword) → "Создаём новый тип"
- "CharacterError" (cream, bold) → "Имя нашего исключения"
- "(Exception)" (indigo) → "Наследуем от Exception — родителя всех ошибок"
- "pass" (amber) → "Пока пустой — наследует всё поведение"

Below: three usage panels in a row:

PANEL 1 — raise it:
raise CharacterError("Имя не может быть пустым")
"Бросаем как обычный ValueError"

PANEL 2 — catch it:
except CharacterError as e:
    print(f"Ошибка персонажа: {e}")
"Ловим по имени"

PANEL 3 — result:
→ Ошибка персонажа: Имя персонажа не может быть пустым
"Точное сообщение о контексте"

Bottom: comparison strip — "ValueError: invalid literal..." (generic, unclear) vs "CharacterError: Имя персонажа не может быть пустым" (specific, informative).

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

## Часть 2: Иерархия своих исключений

Можно создать **базовое** исключение для всей программы, и **специфические** — для разных ситуаций. Специфические наследуют от базового.

```python
# Базовое исключение для всей игры
class GameError(Exception):
    pass

# Специфические исключения — каждый для своей ситуации
class CharacterError(GameError):
    pass

class InventoryError(GameError):
    pass

class SaveError(GameError):
    pass
```

Теперь можно ловить **точечно** (только ошибки сейва) или **широко** (любая игровая ошибка):

```python
def load_save(filename):
    # ... если файл сломан:
    raise SaveError(f"Не удалось загрузить: {filename}")

# Ловим только ошибки сейва:
try:
    load_save("broken.json")
except SaveError as e:
    print(f"Проблема с сейвом: {e}")

# Ловим любую игровую ошибку:
try:
    load_save("broken.json")
except GameError as e:   # поймает SaveError, CharacterError, InventoryError
    print(f"Игровая ошибка: {e}")
```

Это работает потому что `SaveError` — это и `SaveError`, и `GameError` одновременно. Как `FileNotFoundError` — это и `FileNotFoundError`, и `OSError`, и `Exception`.

<!--illustration
file: day_5/exception_hierarchy.png
alt: Иерархия исключений — Exception → GameError → CharacterError / SaveError / InventoryError
prompt:
Create a Dark RPG UI infographic showing a custom exception hierarchy as a skill tree / family tree.

Title: "ИЕРАРХИЯ ИСКЛЮЧЕНИЙ — СЕМЕЙНОЕ ДЕРЕВО" in cream (#e8e0d4).

Top-down tree structure with glowing nodes and organic connecting lines:

ROOT (largest, cream glow): Exception — "Прародитель всех ошибок"

LEVEL 1 (teal, large): GameError(Exception) — "Все игровые ошибки"
  "Базовое исключение для RPG-программы"

LEVEL 2 — three children of GameError (medium nodes):
  - CharacterError(GameError) — teal — "Ошибки персонажа"
  - SaveError(GameError) — indigo — "Ошибки файловой системы"
  - InventoryError(GameError) — amber — "Ошибки инвентаря"

Catch-breadth labels on the right:
  "except SaveError" → catches ONLY SaveError (narrow, precise)
  "except GameError" → catches ALL three children (wide, broad)
  "except Exception" → catches everything (widest, dangerous)

Each node: dark glass circle, colored border, name + description.

Bottom illustration: "SaveError — это SaveError, GameError и Exception одновременно"
Visual: SaveError node surrounded by three concentric colored rings.

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

## Часть 3: Добавляем данные в исключение

Иногда хочется не только передать сообщение, но и **данные** — чтобы обработчик мог с ними работать.

```python
class LevelError(GameError):
    def __init__(self, level, max_level=100):
        self.level = level
        self.max_level = max_level
        # Формируем сообщение и передаём в родительский класс
        # Полное объяснение __init__ и super() — в Week 7
        super().__init__(
            f"Уровень {level} за пределами допустимого (1-{max_level})"
        )
```

Теперь из исключения можно достать **данные**, а не только строку:

```python
try:
    raise LevelError(150)
except LevelError as e:
    print(e)              # → Уровень 150 за пределами допустимого (1-100)
    print(e.level)        # → 150
    print(e.max_level)    # → 100
    # Можно сделать что-то умное с этими числами
```

Это мощный инструмент: обработчик получает не просто текст, а структурированные данные о том что пошло не так.

---

## Часть 4: Когда нужны свои исключения

**Нужны**, когда:
- Хочешь различать ошибки своей программы от системных — `except GameError` vs `except Exception`
- Нужно передать дополнительные данные с ошибкой (`e.level`, `e.item_name`)
- Строишь модуль для других — пользователь может ловить именно твои ошибки

**Не нужны**, когда:
- Просто оборачиваешь одно стандартное исключение в другое без пользы
- Программа маленькая и все ошибки и так понятны из контекста
- Ты только начал проект — не усложняй раньше времени

Хорошее правило: создавай свои исключения тогда, когда пользователь твоей функции должен **обрабатывать их по-разному**.

<!--illustration
file: day_5/custom_vs_generic.png
alt: Своё исключение vs универсальное — точечный except CharacterError vs слишком широкий except Exception
prompt:
Create a Dark RPG UI infographic comparing catching generic Exception vs specific custom exception.

Title: "СВОЁ ИСКЛЮЧЕНИЕ vs УНИВЕРСАЛЬНОЕ" in cream (#e8e0d4).

TWO large panels side by side:

LEFT panel (dim amber, warning) — "except Exception (слишком широко)":
- Warning/skull icon at top
- Code:
  try:
      load_character("Arthas")
  except Exception:
      print("Что-то пошло не так")
- Problems listed:
  ✗ Что именно пошло не так? Неизвестно.
  ✗ Скрывает баги в коде
  ✗ Нет информации для отладки
- Visual: fishnet catching everything — fish, boots, debris

RIGHT panel (teal, clean) — "except CharacterError (точечно)":
- Target/precision icon at top
- Code:
  try:
      load_character("Arthas")
  except CharacterError as e:
      print(f"Ошибка персонажа: {e}")
  except SaveError as e:
      print(f"Ошибка файла: {e}")
- Benefits listed:
  ✓ Ясно что пошло не так
  ✓ Разные реакции на разные ошибки
  ✓ Баги в коде не скрываются
- Visual: precise arrow hitting specific target

Bottom rule: "Создавай свои исключения когда пользователь функции должен ОБРАБАТЫВАТЬ ИХ ПО-РАЗНОМУ"

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

**Задание 1.** Создай иерархию для инвентаря:
- `InventoryError(GameError)` — базовая ошибка инвентаря
- `InventoryFullError(InventoryError)` — инвентарь полон, принимает `max_size` как атрибут
- `ItemNotFoundError(InventoryError)` — предмет не найден, принимает `item_name` как атрибут

Напиши функции `add_item(inventory, item)` и `remove_item(inventory, item_name)`, которые бросают нужные исключения. Проверь что `except InventoryError` ловит оба подтипа.

**Задание 2.** Напиши полную иерархию `GameError` для RPG-проекта из Week 4. Минимум 5 специфических исключений — подумай какие ситуации бывают в менеджере персонажей. Для каждого напиши одну функцию, которая его бросает.

**Задание 3 (дебаг-квест).** Найди проблемы в этой иерархии:

```python
class NetworkError(Exception):
    pass

class FileError(NetworkError):   # ← проблема 1
    pass

class ParseError(Exception):
    pass

class JsonError(ParseError):
    pass

class CsvError(JsonError):       # ← проблема 2
    pass

try:
    raise FileError("диск полон")
except ParseError:               # ← проблема 3
    print("Ошибка файла")
```

Что неправильно? Как должна выглядеть правильная иерархия?

**Задание 4 (мини-проект).** Возьми свой RPG-менеджер персонажей из Week 4 (или напиши базовую версию с нуля). Замени все голые `ValueError`, `KeyError`, `TypeError` на иерархию своих исключений: `GameError → CharacterError, ValidationError, SaveError`. Убедись что в `except` блоках ловятся правильные типы.

---

<quiz>
{
  "questions": [
    {
      "question": "Что означает запись class CharacterError(Exception): pass?",
      "options": [
        "Создаёт функцию CharacterError",
        "Создаёт новый тип исключения, который наследует всё от Exception",
        "Перехватывает исключение Exception",
        "Удаляет исключение Exception из программы"
      ],
      "correct": 1,
      "explanation": "class X(Y) создаёт новый класс X, который наследует поведение от Y. CharacterError(Exception) — это новый тип ошибки, который ведёт себя как Exception, но имеет своё имя."
    },
    {
      "question": "Есть иерархия: GameError → SaveError. Какой except поймает raise SaveError()?",
      "options": [
        "Только except SaveError",
        "Только except GameError",
        "Только except Exception",
        "Все три: except SaveError, except GameError, except Exception"
      ],
      "correct": 3,
      "explanation": "SaveError наследует от GameError, который наследует от Exception. Исключение ловится любым except из цепочки наследования — это и есть сила иерархии."
    },
    {
      "question": "Когда свои исключения НЕ нужны?",
      "options": [
        "Когда пишешь большую программу",
        "Когда пользователь функции должен обрабатывать ошибки по-разному",
        "Когда программа маленькая и ошибки и так понятны из контекста",
        "Когда используешь json.load()"
      ],
      "correct": 2,
      "explanation": "Свои исключения добавляют сложность. Если программа небольшая и стандартные ошибки уже дают достаточно информации — создавать иерархию не нужно. Усложняй только там, где это реально помогает."
    }
  ]
}
</quiz>

---

<!--illustration
file: day_5/skill_tree.png
alt: Дерево навыков Дня 5 — class MyError(Exception), иерархия, raise custom, когда использовать
prompt:
Create a Dark RPG UI skill tree infographic for Day 5 of Week 6 summary.

Title: "НАВЫКИ ДНЯ 5" in cream (#e8e0d4). Subtitle: "Свои исключения" in gray-blue (#8ea4b8).

A branching skill tree with 5 circular nodes connected by organic luminous threads:

Center node (largest, amber glow): crown/custom icon — "Свои исключения"

Branching from center:
- Node 1 (teal): code brackets — "class MyError(Exception): pass"
- Node 2 (indigo): tree diagram — "Иерархия GameError"
- Node 3 (amber): lightning bolt up — "raise CharacterError('...')"
- Node 4 (teal): target icon — "Точечный except"

All nodes connected by soft glowing organic lines.

Bottom: a small checklist glass panel:
✓ class MyError(Exception): pass
✓ Иерархия Exception → GameError → ...
✓ raise CustomError("сообщение")
✓ except MyError (точечно)
✓ Когда нужны / не нужны

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

← [День 4](/python/week_6/day_4/) | [День 6 →](/python/week_6/day_6/)
