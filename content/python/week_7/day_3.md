---
type: lesson
course: "python"
week: 7
day: 3
title: "Наследование — класс от класса"
concepts: [наследование, super().__init__(), переопределение метода, isinstance()]
prerequisites: "[\"[week_7/day_2](/python/week_7/day_2/)\"]"
tags: [python, ооп, наследование, super, isinstance, полиморфизм]
status: draft
---

# День 3: Наследование — класс от класса

> **Сегодня:** учимся строить иерархии классов. Warrior, Mage и Rogue — все герои, но у каждого своя специализация. Наследование позволяет не писать одно и то же трижды.
> **Время:** ~40 минут

---

## Часть 1 — Проблема: три одинаковых класса

Допустим, ты хочешь три класса: Warrior, Mage, Rogue. У всех есть `name`, `hp`, `damage`, методы `is_alive()`, `__str__`. Разница только в методе `attack()` и одном-двух уникальных атрибутах.

Без наследования придётся копировать всё три раза. Это кошмар: если захочешь добавить атрибут `level` — придётся менять три класса.

```
Warrior:   __init__, is_alive, __str__, attack ← сильный удар
Mage:      __init__, is_alive, __str__, attack ← заклинание
Rogue:     __init__, is_alive, __str__, attack ← удар в спину

Всё что выделено курсивом — одинаковое. Зачем писать трижды?
```

**Решение — наследование.** Создаём базовый класс `Hero` с общим кодом, а Warrior, Mage, Rogue **наследуют** от него и добавляют только своё.

---

## Часть 2 — Синтаксис наследования

В Dark Souls есть базовая система персонажей: все имеют здоровье, стамину, экипировку. Рыцарь, Маг, Пиромансер — специализации этой базы. Так же работает наследование в Python.

```python
class Hero:                          # базовый (родительский) класс
    def __init__(self, name, hp, damage):
        self.name   = name
        self.hp     = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return f"[{self.name}] HP:{self.hp} | Урон:{self.damage}"

class Warrior(Hero):                 # Warrior наследует от Hero
    pass                             # пока ничего не добавляем

w = Warrior("Artorias", 150, 30)
print(w)                             # → [Artorias] HP:150 | Урон:30
print(w.is_alive())                  # → True
```

Написав `class Warrior(Hero):`, мы получаем все атрибуты и методы `Hero` автоматически — бесплатно. `Warrior` уже умеет всё, что умеет `Hero`.

<!--illustration
file: day_3/inheritance_tree.png
alt: Дерево иерархии RPG-классов — Hero, Warrior, Mage, Rogue с унаследованными и уникальными атрибутами
prompt:
Create a Dark RPG UI infographic showing an RPG class hierarchy as an inheritance tree.

Title: "ИЕРАРХИЯ КЛАССОВ — НАСЛЕДОВАНИЕ" in cream (#e8e0d4).

A tree structure flowing top to bottom:

ROOT node (largest, teal glow): "Hero" — class Hero: with shared attributes listed beside it in dim grey panels:
- name, hp, damage (grey text — "унаследовано")
- is_alive(), __str__() (grey text — "унаследовано")

Three child nodes connected by glowing organic arrows:
- "Warrior" node (amber): own attributes in color: armor=20. Own method: attack() МОЩНЫЙ УДАР
- "Mage" node (indigo): own attributes in color: mana=200. Own method: attack() ОГНЕННЫЙ ШАР
- "Rogue" node (teal-green): own attributes in color: stealth=60. Own method: attack() УДАР ИЗ ТЕНИ

Each child node: dark glass panel. Shared attributes shown in muted grey, unique attributes in bright color.

Inheritance arrows: soft glowing organic vines flowing from Hero to each child. Label: "class Warrior(Hero):"

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

## Часть 3 — super().__init__(): правильный конструктор

Проблема появляется, когда подкласс хочет добавить **свои** атрибуты. Например, у Мага есть `mana`:

```python
class Mage(Hero):
    def __init__(self, name, hp, damage, mana):
        super().__init__(name, hp, damage)  # вызываем __init__ Hero
        self.mana = mana                    # добавляем свой атрибут

mage = Mage("Sellen", 70, 50, 200)
print(mage.name)     # → Sellen  (создан через Hero.__init__)
print(mage.hp)       # → 70
print(mage.mana)     # → 200     (только у Mage)
print(mage)          # → [Sellen] HP:70 | Урон:50
```

`super()` — это ссылка на родительский класс. `super().__init__(...)` — вызов его конструктора. Он создаёт атрибуты `name`, `hp`, `damage`, а потом мы добавляем `mana`.

**Подводный камень:** если забыть вызвать `super().__init__()`, атрибуты родителя не создадутся:

```python
class BrokenMage(Hero):
    def __init__(self, name, hp, damage, mana):
        self.mana = mana               # ЗАБЫЛИ super().__init__()!

b = BrokenMage("Broken", 70, 50, 200)
print(b.mana)    # → 200  (это есть)
print(b.name)    # → AttributeError: 'BrokenMage' has no attribute 'name'
```

<!--illustration
file: day_3/super_init.png
alt: Цепочка вызовов super().__init__() — Mage вызывает Hero, потом добавляет свои атрибуты
prompt:
Create a Dark RPG UI infographic showing the super().__init__() call chain.

Title: "super().__init__() — ЦЕПОЧКА ВЫЗОВОВ" in cream (#e8e0d4).

A two-stage vertical flow:

STAGE 1 (top, indigo panel): "Mage.__init__(self, name, hp, damage, mana)"
    super().__init__(name, hp, damage)  ← highlighted in amber
    self.mana = mana
Arrow labeled "сначала вызывает родителя" pointing down

STAGE 2 (bottom, teal panel): "Hero.__init__(self, name, hp, damage)"
    self.name   = name     ← creates name
    self.hp     = hp       ← creates hp
    self.damage = damage   ← creates damage
Arrow returning up labeled "создал name, hp, damage"

Then back in STAGE 1: self.mana = mana ← adds own attribute (amber glow)

Right side: a glass panel showing the final Mage object with all 4 attributes:
- name (from Hero)
- hp (from Hero)
- damage (from Hero)
- mana (own — highlighted amber)

Warning panel: "Забыл super().__init__() → AttributeError: 'name'" with skull icon

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

## Часть 4 — Переопределение метода и isinstance()

**Переопределение** — когда подкласс заменяет метод родителя своей версией. Warrior атакует иначе, чем обычный герой:

```python
class Hero:
    def __init__(self, name, hp, damage):
        self.name   = name
        self.hp     = hp
        self.damage = damage

    def attack(self, target):
        target.hp -= self.damage
        print(f"{self.name} атакует: -{self.damage} hp")

    def is_alive(self):
        return self.hp > 0

class Warrior(Hero):
    def attack(self, target):        # переопределяем метод
        bonus  = self.damage * 2     # двойной удар!
        target.hp -= bonus
        print(f"{self.name} МОЩНЫЙ УДАР: -{bonus} hp")

class Mage(Hero):
    def __init__(self, name, hp, damage, mana):
        super().__init__(name, hp, damage)
        self.mana = mana

    def attack(self, target):        # переопределяем метод
        if self.mana >= 20:
            self.mana  -= 20
            target.hp  -= self.damage
            print(f"{self.name} ОГНЕННЫЙ ШАР: -{self.damage} hp")
        else:
            print(f"{self.name}: нет маны!")
```

```python
goblin  = Hero("Гоблин", 50, 5)
warrior = Warrior("Warrior", 150, 30)
mage    = Mage("Mage", 70, 50, 40)

warrior.attack(goblin)   # → Warrior МОЩНЫЙ УДАР: -60 hp
mage.attack(goblin)      # → Mage ОГНЕННЫЙ ШАР: -50 hp (goblin.hp теперь -60)
```

**isinstance()** — проверяет, является ли объект экземпляром класса (или его подкласса):

```python
print(isinstance(warrior, Warrior))  # → True
print(isinstance(warrior, Hero))     # → True  (Warrior наследует Hero!)
print(isinstance(mage, Warrior))     # → False
print(isinstance(mage, Hero))        # → True
```

Это удобно, когда у тебя список разных персонажей и нужно обработать их по-разному.

<!--illustration
file: day_3/method_override.png
alt: Переопределение метода — Hero.attack() vs Warrior.attack() в арене сравнения
prompt:
Create a Dark RPG UI infographic showing method override as an arena comparison.

Title: "ПЕРЕОПРЕДЕЛЕНИЕ МЕТОДА" in cream (#e8e0d4).

Two glass arena panels side by side:

LEFT panel (dim, labeled "Hero.attack()"):
    def attack(self, target):
        target.hp -= self.damage
        print(f"{self.name} атакует: -{self.damage}")
Result box: "Гоблин получает 5 урона" (base damage)
Label: "базовый удар"

RIGHT panel (brighter amber glow, labeled "Warrior.attack() — переопределён"):
    def attack(self, target):
        bonus = self.damage * 2
        target.hp -= bonus
        print(f"{self.name} МОЩНЫЙ УДАР: -{bonus}")
Result box: "Гоблин получает 60 урона" (double damage — amber glow)
Label: "МОЩНЫЙ УДАР x2"

Arrow between panels: "override" label.

Bottom panel: "Python всегда выбирает метод САМОГО конкретного класса" — with organic arrow showing lookup: warrior.attack() → Warrior.attack (found!) → uses this version

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

## Задание 1 — Класс Rogue (6 мин)

Создай класс `Rogue`, наследующий от `Hero`. У Rogue есть дополнительный атрибут `stealth` (скрытность, число). Переопредели `attack()`: удар разбойника наносит урон плюс `stealth // 2` бонусного урона, а `stealth` уменьшается на 10 после удара.

<details>
<summary>Решение</summary>

```python
class Hero:
    def __init__(self, name, hp, damage):
        self.name   = name
        self.hp     = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return f"[{self.name}] HP:{self.hp} | Урон:{self.damage}"

class Rogue(Hero):
    def __init__(self, name, hp, damage, stealth):
        super().__init__(name, hp, damage)
        self.stealth = stealth

    def attack(self, target):
        bonus = self.stealth // 2
        total = self.damage + bonus
        target.hp   -= total
        self.stealth = max(0, self.stealth - 10)
        print(f"{self.name} удар из тени: -{total} (скрытность: {self.stealth})")

rogue  = Rogue("Lautrec", 90, 40, 60)
goblin = Hero("Гоблин", 100, 5)
rogue.attack(goblin)   # → Lautrec удар из тени: -70 (скрытность: 50)
rogue.attack(goblin)   # → Lautrec удар из тени: -65 (скрытность: 40)
```

</details>

---

## Задание 2 — isinstance() в деле (7 мин)

Создай список из 4 персонажей: двух Warrior, одного Mage, одного Hero. Напиши функцию `count_warriors(party)`, которая принимает список и возвращает количество персонажей типа `Warrior` (используй `isinstance`).

<details>
<summary>Решение</summary>

```python
class Hero:
    def __init__(self, name, hp, damage):
        self.name   = name
        self.hp     = hp
        self.damage = damage

class Warrior(Hero):
    pass

class Mage(Hero):
    pass

def count_warriors(party):
    count = 0
    for member in party:
        if isinstance(member, Warrior):
            count += 1
    return count

party = [
    Warrior("Sigurd",  150, 30),
    Mage("Miriel",     70,  50),
    Warrior("Bolverk", 140, 35),
    Hero("Villager",   60,  10),
]

print(count_warriors(party))   # → 2
```

</details>

---

## Задание 3 — Иерархия монстров (8 мин)

Создай базовый класс `Monster` (атрибуты: `name`, `hp`, `reward`; метод `take_damage(amount)` и `__str__`). Создай два подкласса:
- `Boss(Monster)` — у него `hp` удваивается при создании (он живучее), награда утраивается
- `Minion(Monster)` — у него есть атрибут `master_name`. Метод `__str__` добавляет `"(слуга [master_name])"`

<details>
<summary>Решение</summary>

```python
class Monster:
    def __init__(self, name, hp, reward):
        self.name   = name
        self.hp     = hp
        self.reward = reward

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            print(f"{self.name} повержен! Получено {self.reward} монет.")
        else:
            print(f"{self.name}: осталось {self.hp} hp")

    def __str__(self):
        return f"{self.name} | HP:{self.hp} | Награда:{self.reward}"

class Boss(Monster):
    def __init__(self, name, hp, reward):
        super().__init__(name, hp * 2, reward * 3)   # усиленный

class Minion(Monster):
    def __init__(self, name, hp, reward, master_name):
        super().__init__(name, hp, reward)
        self.master_name = master_name

    def __str__(self):
        base = super().__str__()
        return f"{base} (слуга {self.master_name})"

boss   = Boss("Gwyn", 100, 500)
minion = Minion("Рыцарь", 50, 30, "Gwyn")

print(boss)     # → Gwyn | HP:200 | Награда:1500
print(minion)   # → Рыцарь | HP:50 | Награда:30 (слуга Gwyn)
```

</details>

---

## Задание 4 — Мини-проект: отряд (12 мин)

Собери всё вместе. Используй классы `Hero`, `Warrior`, `Mage` из урока. Создай функцию `run_battle(party, monster)`:
- `party` — список героев
- `monster` — объект Monster
- Герои атакуют монстра по очереди, пока он жив
- Если герой мёртв (`is_alive()` → False) — он пропускает ход
- После победы выводит список выживших

Создай отряд из Warrior (150 hp, 30 урон), Mage с маной (70 hp, 50 урон, 60 маны) и обычного Hero (80 hp, 20 урон). Монстр: Boss("Ancient Dragon", 100, 5000).

<details>
<summary>Решение</summary>

```python
class Hero:
    def __init__(self, name, hp, damage):
        self.name   = name
        self.hp     = hp
        self.damage = damage

    def attack(self, target):
        target.hp -= self.damage
        print(f"  {self.name} атакует: -{self.damage}")

    def is_alive(self):
        return self.hp > 0

class Warrior(Hero):
    def attack(self, target):
        dmg = self.damage * 2
        target.hp -= dmg
        print(f"  {self.name} МОЩНЫЙ УДАР: -{dmg}")

class Mage(Hero):
    def __init__(self, name, hp, damage, mana):
        super().__init__(name, hp, damage)
        self.mana = mana

    def attack(self, target):
        if self.mana >= 20:
            self.mana -= 20
            target.hp -= self.damage
            print(f"  {self.name} ЗАКЛИНАНИЕ: -{self.damage}")
        else:
            print(f"  {self.name}: нет маны, пропускает ход")

class Monster:
    def __init__(self, name, hp, reward):
        self.name   = name
        self.hp     = hp
        self.reward = reward

    def is_alive(self):
        return self.hp > 0

class Boss(Monster):
    def __init__(self, name, hp, reward):
        super().__init__(name, hp * 2, reward * 3)

def run_battle(party, monster):
    print(f"БОЙ: отряд против {monster.name} (HP:{monster.hp})\n")
    while monster.is_alive():
        for hero in party:
            if not monster.is_alive():
                break
            if hero.is_alive():
                hero.attack(monster)
    survivors = [h.name for h in party if h.is_alive()]
    print(f"\n{monster.name} повержен!")
    print(f"Выжили: {', '.join(survivors) if survivors else 'никто'}")

party = [
    Warrior("Artorias", 150, 30),
    Mage("Sellen", 70, 50, 60),
    Hero("Сельянин", 80, 20),
]
boss = Boss("Ancient Dragon", 100, 5000)
run_battle(party, boss)
```

</details>

---

<quiz>
[
  {
    "question": "Ты пишешь class Warrior(Hero):. Что это означает?",
    "options": [
      "A. Warrior заменяет Hero",
      "B. Warrior получает все атрибуты и методы Hero",
      "C. Hero получает все методы Warrior",
      "D. Warrior не может иметь свои методы"
    ],
    "answer": "B",
    "explanation": "Warrior(Hero) означает наследование: Warrior автоматически получает всё из Hero. При этом Warrior может добавлять новые методы и атрибуты или переопределять существующие."
  },
  {
    "question": "Зачем в __init__ подкласса вызывать super().__init__()?",
    "options": [
      "A. Это обязательный синтаксис Python",
      "B. Чтобы создать атрибуты родительского класса",
      "C. Чтобы скопировать методы родителя",
      "D. Чтобы удалить атрибуты подкласса"
    ],
    "answer": "B",
    "explanation": "super().__init__() вызывает конструктор родителя и создаёт его атрибуты (например, self.name, self.hp). Без этого вызова атрибуты родителя не появятся в объекте подкласса."
  },
  {
    "question": "warrior = Warrior('A', 100, 20). isinstance(warrior, Hero) вернёт?",
    "options": [
      "A. False — warrior это Warrior, не Hero",
      "B. True — Warrior наследует от Hero",
      "C. Ошибку",
      "D. None"
    ],
    "answer": "B",
    "explanation": "isinstance проверяет не только точный тип, но и всю цепочку наследования. Раз Warrior наследует Hero, экземпляр Warrior является и экземпляром Hero тоже."
  },
  {
    "question": "Warrior переопределяет attack(). Что произойдёт при warrior.attack(target)?",
    "options": [
      "A. Вызовется Hero.attack(), так как Warrior наследует от Hero",
      "B. Ошибка: нельзя переопределять методы родителя",
      "C. Вызовется Warrior.attack() — версия подкласса",
      "D. Вызовутся обе версии по очереди"
    ],
    "answer": "C",
    "explanation": "При переопределении Python всегда использует метод из самого конкретного (дочернего) класса. Hero.attack() при этом не пропадает — к нему можно обратиться через super().attack() если нужно."
  }
]
</quiz>

---

<!--illustration
file: day_3/skill_tree.png
alt: Дерево навыков Дня 3 — наследование, super().__init__(), переопределение, isinstance()
prompt:
Create a Dark RPG UI skill tree infographic for Day 3 of Week 7.

Title: "НАВЫКИ ДНЯ 3" in cream (#e8e0d4). Subtitle: "Наследование" in gray-blue (#8ea4b8).

A branching skill tree with 4 circular nodes:

Root node (largest, teal glow): tree/branches icon — "Наследование"

Branching:
- Node 1 (teal): parentheses icon — "Синтаксис" — "class Warrior(Hero):"
- Node 2 (indigo): chain icon — "super().__init__()" — "вызов конструктора родителя"
- Node 3 (amber): arrows-swap icon — "Переопределение" — "Warrior.attack() → свой метод"
- Node 4 (green): magnifier icon — "isinstance()" — "isinstance(warrior, Hero) → True"

Connected by soft organic luminous vines.

Bottom checklist:
✓ class Child(Parent):
✓ super().__init__(...)
✓ переопределение attack()
✓ isinstance(obj, Class)

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

← [День 2 — Методы](/python/week_7/day_2/) | [День 4 →](/python/week_7/day_4/)
