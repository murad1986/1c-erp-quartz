---
type: lesson
course: "[[python_basics/README]]"
week: 7
day: 1
title: "class и __init__ — создаём объекты"
concepts: [class, __init__, self, атрибуты экземпляра]
prerequisites: []
tags: [python, ооп, классы, объекты, self, init]
status: draft
---

# День 1: class и __init__ — создаём объекты

> **Сегодня:** учимся создавать собственные типы данных — классы. Каждый объект класса — это независимый персонаж со своими характеристиками.
> **Время:** ~40 минут

---

## Часть 1 — Проблема: персонаж в словаре

Помнишь, как на прошлой неделе мы работали с исключениями? Там ты видел `class MyError(Exception):` — первое знакомство с классами. Сегодня разберём их по-настоящему.

Представь, что ты пишешь RPG-игру. Тебе нужно хранить данные о герое. Самый очевидный способ:

```python
hero = {"name": "Artorias", "hp": 100, "damage": 25}

print(hero["name"])   # → Artorias
print(hero["hp"])     # → 100
```

Кажется, работает. Но теперь создай трёх героев:

```python
hero1 = {"name": "Artorias", "hp": 100, "damage": 25}
hero2 = {"name": "Solaire",  "hp": 80,  "damage": 20}
hero3 = {"name": "Siegward", "hp": 120, "damage": 15}

# Хочешь атаковать? Пишешь вручную:
hero2["hp"] -= hero1["damage"]
print(hero2["hp"])   # → 55
```

Это неудобно. Если добавишь новое поле (например, `"mana"`), придётся менять каждый словарь. А если кто-то опечатается и напишет `"HP"` вместо `"hp"` — всё сломается без единой ошибки.

**Решение: класс.** Класс — это чертёж. Словарь — это случайный набор данных, класс — это *гарантированная структура*.

<!--illustration
file: day_1/dict_vs_class.png
alt: Сравнение хранения героя в словаре и в классе — до и после
prompt:
Create a Dark RPG UI infographic comparing dict-based and class-based hero storage as a before/after arena.

Title: "СЛОВАРЬ VS КЛАСС" in cream (#e8e0d4).

LEFT panel (labeled "Словарь — неудобно", dimmer, slightly reddish tint):
- Code: hero = {"name": "Artorias", "hp": 100, "damage": 25}
- Below: hero2["hp"] -= hero["damage"]  — manual, error-prone
- Warning icon: если опечатаешься: "HP" vs "hp" — ошибка без предупреждения!
- Multiple dict snippets showing copy-paste repetition for hero1, hero2, hero3

RIGHT panel (labeled "Класс — структура", brighter, teal tint):
- Code: class Hero: / def __init__(self, name, hp, damage): / ...
- Below: hero1 = Hero("Artorias", 100, 25)  — clean creation
- Check mark: гарантированные поля, нет опечаток
- hero1.hp and hero2.hp shown as separate independent values

Large arrow between panels glowing teal. Label on arrow: "Класс = гарантированная структура"

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

## Часть 2 — Что такое класс: аналогия

В Dark Souls у каждого персонажа есть имя, здоровье, урон. Персонажей сотни, но все сделаны по одному чертежу. Сам персонаж — это **объект** (экземпляр), чертёж — это **класс**.

```
Класс Hero          Объект hero1       Объект hero2
────────────        ───────────────    ───────────────
• имя               name = "Artorias"  name = "Solaire"
• hp                hp   = 100         hp   = 80
• урон              damage = 25        damage = 20
```

Объекты независимы. Изменение `hero1.hp` никак не влияет на `hero2.hp`.

<!--illustration
file: day_1/class_blueprint.png
alt: Класс как чертёж и объекты как готовые персонажи — аналогия
prompt:
Create a Dark RPG UI infographic showing class as a blueprint and objects as characters built from it.

Title: "КЛАСС — ЧЕРТЁЖ, ОБЪЕКТ — ПЕРСОНАЖ" in cream (#e8e0d4).

LEFT side: A glass-morphism panel labeled "class Hero" styled as a blueprint schematic with faint blueprint grid lines. Inside: annotated fields with blueprint-style labels:
- "name" — blank line
- "hp" — blank line
- "damage" — blank line
Blueprint has aged, slightly weathered look with thin teal (#4db8c7) lines.

RIGHT side: Two separate glass panels representing created instances:
- Panel "hero1": name="Artorias", hp=100, damage=25. Character silhouette — a warrior.
- Panel "hero2": name="Solaire", hp=80, damage=20. Character silhouette — a knight with sun symbol.

Two glowing organic arrows from the blueprint to each panel:
- Arrow 1: labeled "hero1 = Hero(...)" in amber monospace
- Arrow 2: labeled "hero2 = Hero(...)" in amber monospace

Bottom: caption panel "Объекты независимы — изменение hero1 не меняет hero2" in cream.

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

## Часть 3 — Пишем первый класс

Ключевое слово `class`, затем имя (с большой буквы — договорённость), двоеточие, тело с отступом.

`__init__` — это специальный метод, который вызывается **автоматически** при создании объекта. Его ещё называют конструктором.

```python
class Hero:
    def __init__(self, name, hp, damage):
        self.name   = name    # атрибут экземпляра
        self.hp     = hp
        self.damage = damage

hero1 = Hero("Artorias", 100, 25)   # вызов __init__
hero2 = Hero("Solaire", 80, 20)

print(hero1.name)    # → Artorias
print(hero2.hp)      # → 80
print(hero1.damage)  # → 25
```

Что здесь происходит:
- `Hero("Artorias", 100, 25)` — Python создаёт новый объект и передаёт его как `self` в `__init__`
- `self.name = name` — записываем значение в атрибут *этого конкретного* объекта
- Получаем объект, у которого есть `.name`, `.hp`, `.damage`

<!--illustration
file: day_1/init_anatomy.png
alt: Анатомия метода __init__ с подписями каждой части
prompt:
Create a Dark RPG UI infographic showing the anatomy of the __init__ method with labeled parts.

Title: "АНАТОМИЯ __init__" in cream (#e8e0d4).

Central: a large code block in a glass-morphism panel:
    def __init__(self, name, hp, damage):
        self.name   = name
        self.hp     = hp
        self.damage = damage

Each part labeled with glowing annotation arrows:
- "self" (teal glow) — labeled "ссылка на ЭТОТ объект"
- "name, hp, damage" (amber glow) — labeled "параметры — приходят извне"
- "self.name" (indigo glow) — labeled "атрибут экземпляра — хранится В объекте"
- "= name" (amber) — labeled "записываем значение"

Below the code: a call example:
    hero1 = Hero("Artorias", 100, 25)
With arrows showing which argument maps to which parameter.

Bottom glass panel: "Python вызывает __init__ автоматически при Hero(...)" in cream.

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

## Часть 4 — self: что это и почему нужен

`self` — это ссылка на сам объект. Когда ты пишешь `hero1.name`, Python под капотом делает примерно `Hero.name(hero1)`. Поэтому `self` должен быть первым параметром в `__init__` и в любом другом методе класса.

**Важно:** `self` — это обычный параметр. Ты *мог бы* назвать его `this` или `me`, и Python не возразит. Но все пишут `self` — это договорённость всего Python-сообщества.

```python
class Hero:
    def __init__(self, name, hp, damage):
        self.name   = name
        self.hp     = hp
        self.damage = damage

warrior = Hero("Warrior", 150, 30)
mage    = Hero("Mage", 70, 50)
rogue   = Hero("Rogue", 90, 40)

# Каждый объект хранит свои данные:
print(warrior.hp)   # → 150
print(mage.hp)      # → 70
print(rogue.hp)     # → 90

# Меняем hp только у warrior:
warrior.hp -= 50
print(warrior.hp)   # → 100
print(mage.hp)      # → 70  (не изменилось!)
```

**Подводный камень:** `self` — первый параметр в определении, но при вызове ты его **не передаёшь**.

```python
# Правильно:
hero = Hero("Artorias", 100, 25)   # передаём name, hp, damage

# Ошибка:
# hero = Hero(hero, "Artorias", 100, 25)  — self НЕ передаётся вручную!
```

---

## Задание 1 — Первый класс (5 мин)

Создай класс `Weapon` с тремя атрибутами: `name` (название оружия), `damage` (урон), `durability` (прочность, число от 0 до 100).

Создай два объекта: меч (`"Greatsword"`, урон 45, прочность 80) и лук (`"Longbow"`, урон 30, прочность 60). Выведи оба объекта на экран через `print`.

<details>
<summary>Решение</summary>

```python
class Weapon:
    def __init__(self, name, damage, durability):
        self.name       = name
        self.damage     = damage
        self.durability = durability

sword = Weapon("Greatsword", 45, 80)
bow   = Weapon("Longbow", 30, 60)

print(sword.name, sword.damage, sword.durability)
# → Greatsword 45 80
print(bow.name, bow.damage, bow.durability)
# → Longbow 30 60
```

</details>

---

## Задание 2 — Три героя (7 мин)

Используя класс `Hero` из урока, создай трёх персонажей: Warrior (hp=150, damage=30), Mage (hp=70, damage=50), Rogue (hp=90, damage=40).

Затем:
1. Воин атакует мага: уменьши `hp` мага на урон воина
2. Маг атакует разбойника: уменьши `hp` разбойника на урон мага
3. Выведи итоговый `hp` всех трёх героев

<details>
<summary>Решение</summary>

```python
class Hero:
    def __init__(self, name, hp, damage):
        self.name   = name
        self.hp     = hp
        self.damage = damage

warrior = Hero("Warrior", 150, 30)
mage    = Hero("Mage", 70, 50)
rogue   = Hero("Rogue", 90, 40)

mage.hp   -= warrior.damage   # воин атакует мага
rogue.hp  -= mage.damage      # маг атакует разбойника

print(warrior.name, warrior.hp)  # → Warrior 150
print(mage.name,    mage.hp)     # → Mage 40
print(rogue.name,   rogue.hp)    # → Rogue 40
```

</details>

---

## Задание 3 — Класс Monster (8 мин)

Создай класс `Monster` с атрибутами `name`, `hp`, `reward` (сколько монет дают за убийство). Создай трёх монстров:
- Zombie: hp=30, reward=5
- Skeleton: hp=50, reward=10
- Dragon: hp=500, reward=1000

Выведи информацию о каждом в формате: `"Дракон: 500 hp, награда: 1000 монет"`

<details>
<summary>Решение</summary>

```python
class Monster:
    def __init__(self, name, hp, reward):
        self.name   = name
        self.hp     = hp
        self.reward = reward

zombie   = Monster("Зомби",   30,  5)
skeleton = Monster("Скелет",  50,  10)
dragon   = Monster("Дракон",  500, 1000)

monsters = [zombie, skeleton, dragon]
for m in monsters:
    print(f"{m.name}: {m.hp} hp, награда: {m.reward} монет")
# → Зомби: 30 hp, награда: 5 монет
# → Скелет: 50 hp, награда: 10 монет
# → Дракон: 500 hp, награда: 1000 монет
```

</details>

---

## Задание 4 — Мини-проект: инвентарь (10 мин)

Создай класс `Item` с атрибутами `name`, `item_type` (тип: `"weapon"`, `"armor"`, `"potion"`), `value` (стоимость в монетах).

Создай список из 5 предметов — смешай типы. Напиши код, который:
1. Выводит все предметы с их типом и стоимостью
2. Считает и выводит общую стоимость всего инвентаря
3. Выводит только предметы типа `"potion"`

<details>
<summary>Решение</summary>

```python
class Item:
    def __init__(self, name, item_type, value):
        self.name      = name
        self.item_type = item_type
        self.value     = value

inventory = [
    Item("Эстус",        "potion", 0),
    Item("Меч рыцаря",   "weapon", 500),
    Item("Зелье силы",   "potion", 150),
    Item("Кольчуга",     "armor",  300),
    Item("Огненный шар", "weapon", 250),
]

total = 0
for item in inventory:
    print(f"{item.name} [{item.item_type}] — {item.value} монет")
    total += item.value
# → Эстус [potion] — 0 монет  ... и т.д.

print(f"Итого: {total} монет")  # → Итого: 1200 монет

print("Зелья:")
for item in inventory:
    if item.item_type == "potion":
        print(" -", item.name)
# → Зелья:
# →  - Эстус
# →  - Зелье силы
```

</details>

---

<quiz>
[
  {
    "question": "Что такое __init__?",
    "options": [
      "A. Метод, который удаляет объект",
      "B. Метод, который вызывается автоматически при создании объекта",
      "C. Метод, который выводит объект на экран",
      "D. Обычная функция внутри класса"
    ],
    "answer": "B",
    "explanation": "__init__ — конструктор. Python вызывает его сам каждый раз, когда ты пишешь MyClass(...). В нём обычно задают начальные атрибуты объекта."
  },
  {
    "question": "Ты пишешь: hero = Hero('Link', 100, 20). Сколько аргументов передаётся в __init__?",
    "options": [
      "A. 2 (name и hp)",
      "B. 3 (name, hp, damage)",
      "C. 4 (self, name, hp, damage)",
      "D. Зависит от компьютера"
    ],
    "answer": "B",
    "explanation": "При вызове передаются 3 аргумента: 'Link', 100, 20. self Python подставляет сам — ты его не передаёшь явно. Внутри __init__ параметров 4 (включая self), но при вызове — 3."
  },
  {
    "question": "hero1 = Hero('A', 100, 20); hero2 = Hero('B', 80, 15); hero1.hp = 50. Чему равен hero2.hp?",
    "options": [
      "A. 50",
      "B. 80",
      "C. 100",
      "D. 0"
    ],
    "answer": "B",
    "explanation": "Каждый объект хранит свои атрибуты независимо. Изменение hero1.hp никак не затрагивает hero2.hp — это разные объекты в памяти."
  },
  {
    "question": "Что выведет: class A:\n    def __init__(self, x):\n        self.x = x\na = A(7)\nprint(a.x)?",
    "options": [
      "A. self.x",
      "B. x",
      "C. 7",
      "D. Ошибка"
    ],
    "answer": "C",
    "explanation": "При создании a = A(7) Python вызывает __init__(self, 7), записывает self.x = 7. Потом a.x обращается к атрибуту x объекта a — это 7."
  }
]
</quiz>

---

<!--illustration
file: day_1/skill_tree.png
alt: Дерево навыков Дня 1 — class, __init__, self, атрибуты экземпляра
prompt:
Create a Dark RPG UI skill tree infographic for Day 1 of Week 7.

Title: "НАВЫКИ ДНЯ 1" in cream (#e8e0d4). Subtitle: "class и __init__" in gray-blue (#8ea4b8).

A branching skill tree with 4 circular nodes connected by organic luminous threads flowing downward:

Root node (largest, teal glow): icon of blueprint schematic — "class"

Branching from root:
- Node 1 (teal): gear icon — "__init__" — "конструктор объекта"
- Node 2 (indigo): arrow-to-self icon — "self" — "ссылка на объект"
- Node 3 (amber): database slots icon — "атрибуты экземпляра" — "self.name = name"

All nodes connected by soft glowing organic vine-like lines. Each node: dark glass circle, thin colored border.

Bottom: a small checklist glass panel:
✓ class Hero:
✓ def __init__(self, ...):
✓ self.name = name
✓ hero1 = Hero(...)

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

← [Week 6 — Практика](../week_6/day_6.md) | [День 2 — Методы →](day_2.md)
