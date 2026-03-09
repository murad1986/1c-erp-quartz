---
type: lesson
course: "python"
week: 7
day: 5
title: "Магические методы — говорим с Python на его языке"
concepts: [__str__, __len__, __eq__, __repr__]
prerequisites: "[\"[week_7/day_4](/python/week_7/day_4/)\"]"
tags: [python, ооп, классы, магические методы, dunder методы]
status: draft
---

# Day 5: Магические методы — говорим с Python на его языке

> **Сегодня:** учимся объяснять Python, как работать с нашими объектами — сравнивать, считать, печатать
> **Время:** ~40 минут

---

## Часть 1 — Аналогия: Python уже умеет многое

Когда ты пишешь `3 + 5`, Python знает, что делать. Когда пишешь `len("hello")` — знает. Когда `print(42)` — тоже знает.

Но откуда Python знает, что делать с **твоим** объектом?

```python
class Item:
    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity

sword = Item("Bastard Sword", "редкий")

print(sword)      # <__main__.Item object at 0x10f3a2c50>  <-- непонятно
len(sword)        # TypeError: object of type 'Item' has no len()
sword == sword    # True (но по АДРЕСУ в памяти, не по содержимому!)
```

Python не знает, что значит «напечатать меч» или «длина меча». Но мы можем **объяснить ему это** через специальные методы.

Эти методы называются **магическими** (или **dunder-методами** — от «double underscore», двойное подчёркивание). Их имена всегда выглядят так: `__имя__`.

<!--illustration
file: day_5/dunder_map.png
alt: Карта автоматических вызовов магических методов Python — print→__str__, len→__len__, ==→__eq__, repr→__repr__
prompt:
Create a Dark RPG UI infographic showing a visual map of Python's automatic magic method calls.

Title: "МАГИЧЕСКИЕ МЕТОДЫ — КАК PYTHON ВЫЗЫВАЕТ ИХ" in cream (#e8e0d4).

Four translation arrows arranged in a 2x2 grid, each in its own glass panel:

Panel 1 (teal):
Left: print(sword) [user-written code]
→ translation arrow labeled "Python переводит в:"
Right: sword.__str__() [what Python actually calls]

Panel 2 (indigo):
Left: len(inventory)
→ arrow
Right: inventory.__len__()

Panel 3 (amber):
Left: sword == other_sword
→ arrow
Right: sword.__eq__(other_sword)

Panel 4 (teal-indigo):
Left: repr(sword)
→ arrow
Right: sword.__repr__()

Center: a glowing orb labeled "Python" connecting all four panels with organic light threads.

Bottom: caption "Ты пишешь обычный код — Python сам вызывает нужный метод" in cream.

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

## Часть 2 — `__str__`: что видит print()

Ты уже встречал `__str__` в Day 2. Сегодня разбираемся глубже.

`__str__` — это метод, который Python вызывает, когда ты делаешь `print(obj)` или `str(obj)`. Он должен возвращать строку, понятную **человеку**.

```python
class Item:
    def __init__(self, name, rarity, damage):
        self.name = name
        self.rarity = rarity
        self.damage = damage

    def __str__(self):
        rarity_colors = {
            "обычный": "⬜",
            "необычный": "🟩",
            "редкий": "🟦",
            "эпический": "🟪",
            "легендарный": "🟨"
        }
        icon = rarity_colors.get(self.rarity, "⬜")
        return f"{icon} {self.name} ({self.rarity}) — урон: {self.damage}"


sword = Item("Bastard Sword", "редкий", 45)
shield = Item("Tower Shield", "обычный", 0)
excalibur = Item("Excalibur", "легендарный", 120)

print(sword)      # 🟦 Bastard Sword (редкий) — урон: 45
print(shield)     # ⬜ Tower Shield (обычный) — урон: 0
print(excalibur)  # 🟨 Excalibur (легендарный) — урон: 120
```

Теперь `print` показывает человекочитаемое описание, а не адрес в памяти.

---

## Часть 3 — `__len__`: что возвращает len()

`len()` работает со списками, строками, словарями. Можно сделать так, чтобы она работала и с твоим классом.

Добавим класс `Inventory` — инвентарь героя:

```python
class Inventory:
    def __init__(self, owner):
        self.owner = owner
        self._items = []  # внутренний список (помним инкапсуляцию!)

    def add_item(self, item):
        self._items.append(item)
        print(f"  + {item.name} добавлен в инвентарь")

    def __len__(self):
        return len(self._items)

    def __str__(self):
        if not self._items:
            return f"Инвентарь {self.owner}: пусто"
        lines = [f"Инвентарь {self.owner} ({len(self)} предметов):"]
        for i, item in enumerate(self._items, 1):
            lines.append(f"  {i}. {item}")
        return "\n".join(lines)


class Item:
    def __init__(self, name, rarity, damage=0):
        self.name = name
        self.rarity = rarity
        self.damage = damage

    def __str__(self):
        return f"{self.name} ({self.rarity})"


inv = Inventory("Chosen Undead")
print(f"Предметов в инвентаре: {len(inv)}")  # 0

sword = Item("Bastard Sword", "редкий", 45)
ring = Item("Ring of Steel Protection", "необычный")
inv.add_item(sword)
inv.add_item(ring)

print(f"Предметов в инвентаре: {len(inv)}")  # 2
print(inv)
```

Вывод:
```
Предметов в инвентаре: 0
  + Bastard Sword добавлен в инвентарь
  + Ring of Steel Protection добавлен в инвентарь
Предметов в инвентаре: 2
Инвентарь Chosen Undead (2 предметов):
  1. Bastard Sword (редкий)
  2. Ring of Steel Protection (необычный)
```

`len(inv)` теперь возвращает количество предметов. Python вызывает `inv.__len__()` автоматически.

---

## Часть 4 — `__eq__`: когда два объекта равны?

По умолчанию `==` для объектов сравнивает **адреса в памяти** (то есть, это буквально один и тот же объект или нет):

```python
a = Item("Sword", "обычный", 10)
b = Item("Sword", "обычный", 10)

print(a == b)  # False! Разные объекты в памяти, хотя содержимое одинаковое
print(a == a)  # True  — это один и тот же объект
```

Это часто не то, чего мы хотим. Нам важно: «этот предмет называется так же?».

Добавляем `__eq__`:

```python
class Item:
    def __init__(self, name, rarity, damage=0):
        self.name = name
        self.rarity = rarity
        self.damage = damage

    def __eq__(self, other):
        # Сначала проверяем: other вообще тоже Item?
        if not isinstance(other, Item):
            return NotImplemented  # Python разберётся сам
        # Два предмета равны, если у них одинаковое имя
        return self.name == other.name

    def __str__(self):
        return f"{self.name} ({self.rarity})"


sword1 = Item("Bastard Sword", "редкий", 45)
sword2 = Item("Bastard Sword", "обычный", 30)  # то же имя, другая редкость
dagger = Item("Dagger", "обычный", 15)

print(sword1 == sword2)  # True  — оба называются "Bastard Sword"
print(sword1 == dagger)  # False — разные имена
print(sword1 == "Bastard Sword")  # False — строка не Item, возвращаем NotImplemented
```

Зачем `NotImplemented`? Если мы возвращаем `NotImplemented`, Python пробует вызвать `__eq__` у другого объекта. Если и там не получается — возвращает `False`. Это правильное поведение.

Практичный пример — проверка дубликатов в инвентаре:

```python
class Inventory:
    def __init__(self, owner):
        self.owner = owner
        self._items = []

    def add_item(self, item):
        # Проверяем дубликат через __eq__
        if item in self._items:
            print(f"  ! {item.name} уже есть в инвентаре")
        else:
            self._items.append(item)
            print(f"  + {item.name} добавлен")

    def __len__(self):
        return len(self._items)


inv = Inventory("Hero")
sword = Item("Bastard Sword", "редкий", 45)
sword_copy = Item("Bastard Sword", "необычный", 40)

inv.add_item(sword)        # + Bastard Sword добавлен
inv.add_item(sword_copy)   # ! Bastard Sword уже есть в инвентаре
```

`item in self._items` внутри вызывает `__eq__` для каждого элемента списка.

<!--illustration
file: day_5/eq_memory.png
alt: __eq__ — сравнение по значению vs сравнение адресов в памяти для двух объектов Item
prompt:
Create a Dark RPG UI infographic showing memory comparison vs __eq__ value comparison.

Title: "__eq__ — СРАВНИВАЕМ ЗНАЧЕНИЯ, НЕ АДРЕСА" in cream (#e8e0d4).

TOP section — Memory layout:
Two glass memory address panels:
- Address 0x1a2b: sword1 = Item("Bastard Sword", "редкий", 45) — teal border
- Address 0x3c4d: sword2 = Item("Bastard Sword", "обычный", 30) — teal border
Both at DIFFERENT memory addresses (shown clearly).

BOTTOM LEFT panel (dim, amber warning): "Без __eq__:"
    sword1 == sword2 → False
Caption: "Сравниваются АДРЕСА. Разные объекты → False"
Skull/X icon.

BOTTOM RIGHT panel (bright, green): "С __eq__:"
    def __eq__(self, other):
        return self.name == other.name
    sword1 == sword2 → True
Caption: "Сравниваются ИМЕНА. 'Bastard Sword' == 'Bastard Sword' → True"
Check mark icon.

Center: organic arrow labeled "определяем правило равенства"

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

## Часть 5 — `__repr__`: для разработчика, не для игрока

Есть ещё один похожий метод — `__repr__`. Разница такая:

| Метод | Для кого | Цель |
|-------|----------|------|
| `__str__` | Для пользователя | Красивый, понятный вывод |
| `__repr__` | Для разработчика | Точный, однозначный вывод для отладки |

`__repr__` вызывается:
- когда ты смотришь на объект в интерактивной консоли (без `print`)
- внутри списков и словарей при `print`
- через `repr(obj)`

Правило: если не знаешь, что писать в `__repr__`, пиши `f"ClassName(attr={self.attr!r})"`. Конструкция `!r` добавляет кавычки вокруг строк — чтобы было сразу ясно, что строка, а что число.

```python
class Item:
    def __init__(self, name, rarity, damage=0):
        self.name = name
        self.rarity = rarity
        self.damage = damage

    def __str__(self):
        return f"{self.name} ({self.rarity})"

    def __repr__(self):
        return f"Item(name={self.name!r}, rarity={self.rarity!r}, damage={self.damage!r})"

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self.name == other.name

    def __len__(self):
        # Для предмета len() — это "вес" или просто 1?
        # Пусть возвращает 1 (один слот в инвентаре)
        return 1


sword = Item("Bastard Sword", "редкий", 45)

print(sword)       # 🟦 Bastard Sword (редкий)   <-- __str__
print(repr(sword)) # Item(name='Bastard Sword', rarity='редкий', damage=45)  <-- __repr__

# В списке Python использует __repr__:
items = [sword, Item("Dagger", "обычный", 15)]
print(items)
# [Item(name='Bastard Sword', rarity='редкий', damage=45), Item(name='Dagger', rarity='обычный', damage=15)]
```

Это удобно при дебаггинге: видишь точные значения, а не `<Item object at 0x...>`.

<!--illustration
file: day_5/str_vs_repr.png
alt: __str__ vs __repr__ — красивый вывод для пользователя vs точный вывод для разработчика
prompt:
Create a Dark RPG UI infographic comparing __str__ and __repr__ outputs for the same object.

Title: "__str__ vs __repr__ — ДЛЯ КОГО?" in cream (#e8e0d4).

Two glass panels side by side:

LEFT panel (teal glow, labeled "__str__ — для пользователя"):
- Icon: player/person silhouette
- Caption: "Красивый, понятный"
- Output box: 🟦 Bastard Sword (редкий) — урон: 45
- Context: print(sword) → this output
- Label: "Читается как текст"

RIGHT panel (indigo glow, labeled "__repr__ — для разработчика"):
- Icon: developer/wrench silhouette
- Caption: "Точный, однозначный"
- Output box: Item(name='Bastard Sword', rarity='редкий', damage=45)
- Context: repr(sword) / в списке [sword] → this output
- Label: "Видны все значения для дебага"

Center divider with the sword Item object icon glowing amber.

Bottom: "Правило: __str__ — красота, __repr__ — точность" in cream monospace.

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

## Часть 6 — Всё вместе: класс Item с магическими методами

```python
class Item:
    def __init__(self, name, rarity, damage=0, weight=1):
        self.name = name
        self.rarity = rarity
        self.damage = damage
        self.weight = weight

    def __str__(self):
        return f"{self.name} ({self.rarity}, урон: {self.damage})"

    def __repr__(self):
        return (f"Item(name={self.name!r}, rarity={self.rarity!r}, "
                f"damage={self.damage!r}, weight={self.weight!r})")

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self.name == other.name

    def __len__(self):
        return self.weight  # "длина" предмета = его вес в слотах


class Inventory:
    def __init__(self, owner, capacity=10):
        self.owner = owner
        self._capacity = capacity
        self._items = []

    def add_item(self, item):
        if len(self) >= self._capacity:
            print(f"  ! Инвентарь полон ({self._capacity} слотов)")
            return False
        if item in self._items:
            print(f"  ! {item.name} уже есть")
            return False
        self._items.append(item)
        print(f"  + {item.name}")
        return True

    def __len__(self):
        return len(self._items)

    def __str__(self):
        if not self._items:
            return f"[{self.owner}] инвентарь пуст"
        lines = [f"[{self.owner}] инвентарь ({len(self)}/{self._capacity}):"]
        for item in self._items:
            lines.append(f"  • {item}")
        return "\n".join(lines)


# Тест:
sword = Item("Claymore", "редкий", 60, weight=2)
ring = Item("Havels Ring", "легендарный", 0, weight=1)
shield = Item("Dragon Crest Shield", "необычный", 0, weight=3)
shield_copy = Item("Dragon Crest Shield", "обычный", 0, weight=3)

print(sword)           # Claymore (редкий, урон: 60)
print(repr(ring))      # Item(name='Havels Ring', rarity='легендарный', damage=0, weight=1)
print(sword == ring)   # False
print(shield == shield_copy)  # True (одинаковое имя)

inv = Inventory("Chosen Undead", capacity=3)
inv.add_item(sword)
inv.add_item(ring)
inv.add_item(shield)
inv.add_item(shield_copy)  # ! уже есть
print(inv)
```

---

## Камень в рюкзак: `==` и `is`

```python
a = Item("Sword", "обычный", 10)
b = Item("Sword", "обычный", 10)

print(a == b)  # True  — мы определили __eq__ по имени
print(a is b)  # False — это два разных объекта в памяти

c = a
print(a is c)  # True  — c это та же ссылка, что и a
```

`==` — сравнивает **значения** (через `__eq__`)
`is` — сравнивает **адреса в памяти** (тот же ли это объект)

В 99% случаев тебе нужен `==`. `is` используют в основном для `is None`.

---

## Итог дня

| Метод | Когда вызывается | Что возвращает |
|-------|-----------------|----------------|
| `__str__` | `print(obj)`, `str(obj)` | Строка для пользователя |
| `__repr__` | `repr(obj)`, в консоли, в списках | Строка для разработчика |
| `__len__` | `len(obj)` | Целое число >= 0 |
| `__eq__` | `obj1 == obj2` | `True`/`False` или `NotImplemented` |

**Главная идея:** магические методы — это способ объяснить Python, как вести себя с твоими объектами. Ты пишешь правила, Python им следует.

---

> **Задание на подумать:** у тебя есть класс `Enemy` с атрибутами `name` и `hp`. Что должен возвращать `__str__`? Что `__repr__`? Когда два врага должны считаться «равными»?

---

## Задание 1 — `__str__` для персонажа (10 мин)

Добавь `__str__` к классу `Hero`. Вывод должен включать класс персонажа, имя и HP.

```python
hero = Hero("Странник", level=5, hp=80, char_class="Воин")
print(hero)      # → [Воин] Странник | Ур.5 | HP: 80
print(str(hero)) # → [Воин] Странник | Ур.5 | HP: 80
```

<details>
<summary>Решение</summary>

```python
class Hero:
    def __init__(self, name, level, hp, char_class):
        self.name = name
        self.level = level
        self.hp = hp
        self.char_class = char_class

    def __str__(self):
        return f"[{self.char_class}] {self.name} | Ур.{self.level} | HP: {self.hp}"

hero = Hero("Странник", level=5, hp=80, char_class="Воин")
print(hero)  # → [Воин] Странник | Ур.5 | HP: 80
```

</details>

---

## Задание 2 — `__len__` для инвентаря (10 мин)

Создай класс `Inventory` с методом `add()` и `__len__`. `len(inventory)` должен возвращать количество предметов.

```python
inv = Inventory()
inv.add("Меч")
inv.add("Щит")
inv.add("Зелье")
print(len(inv))                  # → 3
print(f"Предметов: {len(inv)}")  # → Предметов: 3
```

<details>
<summary>Решение</summary>

```python
class Inventory:
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def __len__(self):
        return len(self._items)

inv = Inventory()
inv.add("Меч")
inv.add("Щит")
inv.add("Зелье")
print(len(inv))  # → 3
```

</details>

---

## Задание 3 — `__eq__` для предметов (10 мин)

Два предмета `Item` считаются одинаковыми, если совпадают `name` и `rarity`. Реализуй `__eq__`.

```python
sword1 = Item("Длинный меч", "обычный")
sword2 = Item("Длинный меч", "обычный")
sword3 = Item("Длинный меч", "редкий")

print(sword1 == sword2)  # → True
print(sword1 == sword3)  # → False
print(sword1 is sword2)  # → False  (разные объекты в памяти!)
```

<details>
<summary>Решение</summary>

```python
class Item:
    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self.name == other.name and self.rarity == other.rarity

sword1 = Item("Длинный меч", "обычный")
sword2 = Item("Длинный меч", "обычный")
sword3 = Item("Длинный меч", "редкий")
print(sword1 == sword2)  # → True
print(sword1 == sword3)  # → False
print(sword1 is sword2)  # → False
```

</details>

---

## Задание 4 — Мини-проект: класс Item со всеми магическими методами (15 мин)

Собери все четыре метода в одном классе `Item`:
- `__str__` → `"[редкий] Меч бездны"`
- `__repr__` → `"Item(name='Меч бездны', rarity='редкий', damage=150)"`
- `__len__` → возвращает `damage`
- `__eq__` → равенство по `name`

```python
blade = Item("Меч бездны", "редкий", damage=150)
print(blade)           # → [редкий] Меч бездны
print(repr(blade))     # → Item(name='Меч бездны', rarity='редкий', damage=150)
print(len(blade))      # → 150
blade2 = Item("Меч бездны", "обычный", damage=50)
print(blade == blade2) # → True  (сравниваем по name)
```

<details>
<summary>Решение</summary>

```python
class Item:
    def __init__(self, name, rarity, damage):
        self.name = name
        self.rarity = rarity
        self.damage = damage

    def __str__(self):
        return f"[{self.rarity}] {self.name}"

    def __repr__(self):
        return (f"Item(name={self.name!r}, rarity={self.rarity!r}, "
                f"damage={self.damage!r})")

    def __len__(self):
        return self.damage

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self.name == other.name

blade = Item("Меч бездны", "редкий", damage=150)
print(blade)            # → [редкий] Меч бездны
print(repr(blade))      # → Item(name='Меч бездны', rarity='редкий', damage=150)
print(len(blade))       # → 150
blade2 = Item("Меч бездны", "обычный", damage=50)
print(blade == blade2)  # → True
```

</details>

---

<!--illustration
file: day_5/skill_tree.png
alt: Дерево навыков Дня 5 — __str__, __len__, __eq__, __repr__
prompt:
Create a Dark RPG UI skill tree infographic for Day 5 of Week 7.

Title: "НАВЫКИ ДНЯ 5" in cream (#e8e0d4). Subtitle: "Магические методы" in gray-blue (#8ea4b8).

A branching skill tree with 4 circular nodes:

Root node (largest, amber glow): double-underscore __ icon — "Dunder-методы"

Branching:
- Node 1 (teal): print icon — "__str__" — "красивый вывод для пользователя"
- Node 2 (indigo): ruler icon — "__len__" — "len(obj) → количество"
- Node 3 (green): equals icon — "__eq__" — "obj1 == obj2 по значению"
- Node 4 (amber): code/debug icon — "__repr__" — "точный вывод для разработчика"

Connected by soft organic luminous vines.

Bottom checklist:
✓ def __str__(self): return "..."
✓ def __len__(self): return int
✓ def __eq__(self, other): return bool
✓ def __repr__(self): return "ClassName(...)"

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

← [Day 4 — Инкапсуляция](/python/week_7/day_4/) | [Day 6 — Практика →](/python/week_7/day_6/)
