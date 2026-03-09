---
type: lesson
course: "[[python_basics/README]]"
week: 7
day: 2
title: "Методы — функции внутри класса"
concepts: [методы экземпляра, __str__, self.метод(), return из метода]
prerequisites: "[\"[[week_7/day_1]]\"]"
tags: [python, ооп, классы, методы, __str__, self]
status: draft
---

# День 2: Методы — функции внутри класса

> **Сегодня:** даём объектам умения. Персонаж без атаки, лечения и проверки жизни — не герой, а просто набор цифр. Исправляем это.
> **Время:** ~40 минут

---

## Часть 1 — Объект с характеристиками И умениями

Вчера мы создали героя с атрибутами `name`, `hp`, `damage`. Но атаковали так:

```python
mage.hp -= warrior.damage
```

Это работает, но в большой игре это будет везде: и в бою, и при ловушках, и при отравлении. Одна логика разбросана по сотням мест. Если захочешь добавить броню — придётся менять всё.

Решение: вложить умения прямо в объект. В Dark Souls у каждого персонажа есть свой набор атак. Так же и у наших объектов — **методы** это функции, которые принадлежат классу и работают с его данными.

```
Объект warrior:
  Атрибуты:  name="Warrior", hp=150, damage=30
  Методы:    attack(), heal(), is_alive()
```

---

## Часть 2 — Пишем методы: attack, heal, is_alive

Метод — это обычная функция внутри класса. Первый параметр всегда `self` (ссылка на объект, от которого вызывается метод).

```python
class Hero:
    def __init__(self, name, hp, damage):
        self.name   = name
        self.hp     = hp
        self.damage = damage

    def attack(self, target):
        target.hp -= self.damage        # уменьшаем hp цели
        print(f"{self.name} атакует {target.name} на {self.damage}!")
        # → Warrior атакует Mage на 30!

    def heal(self, amount):
        self.hp += amount
        print(f"{self.name} восстановил {amount} hp. Текущий hp: {self.hp}")
        # → Warrior восстановил 20 hp. Текущий hp: 170

    def is_alive(self):
        return self.hp > 0              # → True или False
```

Вызов метода:

```python
warrior = Hero("Warrior", 150, 30)
mage    = Hero("Mage", 70, 50)

warrior.attack(mage)       # → Warrior атакует Mage на 30!
print(mage.hp)             # → 40
warrior.heal(20)           # → Warrior восстановил 20 hp. Текущий hp: 170
print(warrior.is_alive())  # → True
```

**Подводный камень:** `hero.attack` — это объект метода (без вызова). `hero.attack(target)` — это вызов. Легко забыть скобки.

```python
print(warrior.is_alive)    # → <bound method Hero.is_alive of <...>>
print(warrior.is_alive())  # → True
```

<!--illustration
file: day_2/method_anatomy.png
alt: Анатомия метода экземпляра — self, target, self.damage
prompt:
Create a Dark RPG UI infographic showing the anatomy of an instance method.

Title: "АНАТОМИЯ МЕТОДА ЭКЗЕМПЛЯРА" in cream (#e8e0d4).

Central: a large glass-morphism code panel showing:
    def attack(self, target):
        target.hp -= self.damage
        print(f"{self.name} атакует {target.name} на {self.damage}!")

Labeled annotation arrows pointing to each part:
- "self" (teal glow) — labeled "атакующий — тот, от кого вызван метод"
- "target" (indigo glow) — labeled "цель — передаём явно"
- "self.damage" (amber) — labeled "доступ к атрибуту через self"
- "target.hp" (amber) — labeled "изменяем атрибут цели"

Below: call example panel:
    warrior.attack(mage)
Arrow: warrior → self, mage → target

Side note glass panel: "self — первый параметр ВСЕГДА, но при вызове НЕ передаётся"

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

## Часть 3 — __str__: как выглядит объект при print

Попробуй сейчас вывести объект:

```python
print(warrior)
# → <__main__.Hero object at 0x7f3a2c1b4d50>
```

Бесполезно. Исправим это через специальный метод `__str__`. Python вызывает его автоматически, когда ты делаешь `print(объект)` или `str(объект)`.

```python
class Hero:
    def __init__(self, name, hp, damage):
        self.name   = name
        self.hp     = hp
        self.damage = damage

    def __str__(self):
        return f"[{self.name}] HP: {self.hp} | Урон: {self.damage}"

warrior = Hero("Warrior", 150, 30)
mage    = Hero("Mage", 70, 50)

print(warrior)  # → [Warrior] HP: 150 | Урон: 30
print(mage)     # → [Mage] HP: 70 | Урон: 50
```

`__str__` должен **возвращать строку** (через `return`), а не выводить её через `print`. Python сам решит, что с ней делать.

<!--illustration
file: day_2/str_method.png
alt: Цепочка вызовов при print(hero) — как Python находит и вызывает __str__
prompt:
Create a Dark RPG UI infographic showing the call chain when print(hero) is executed.

Title: "КАК РАБОТАЕТ print(hero)" in cream (#e8e0d4).

A vertical flow diagram with glass panels connected by organic glowing arrows:

Step 1 (top): Code panel: print(warrior) — teal border
↓ arrow labeled "Python ищет..."
Step 2: Panel: __str__ defined? — decision diamond shape with soft amber glow
↓ arrow "Да — вызывает"
Step 3 (indigo): Code panel: def __str__(self): / return f"[{self.name}] HP:{self.hp}"
↓ arrow "возвращает строку"
Step 4 (green #7bc88f): Output panel: [Warrior] HP:150 | Урон:30 ← beautiful, human-readable

Side branch from Step 2: "Нет __str__?" → red-amber panel: <__main__.Hero object at 0x7f3a...> — useless

Bottom note: "__str__ должен ВОЗВРАЩАТЬ строку (return), не выводить через print"

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

## Часть 4 — Методы вызывают другие методы через self

Методы внутри класса могут обращаться к другим методам через `self.имя_метода()`. Добавим метод `try_attack`, который проверяет, жив ли персонаж перед атакой:

```python
class Hero:
    def __init__(self, name, hp, damage):
        self.name   = name
        self.hp     = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        if not self.is_alive():          # вызов другого метода
            print(f"{self.name} мёртв и не может атаковать!")
            return
        target.hp -= self.damage
        print(f"{self.name} → {target.name}: -{self.damage} hp")
        # → Warrior → Mage: -30 hp

    def __str__(self):
        status = "жив" if self.is_alive() else "мёртв"
        return f"[{self.name}] HP:{self.hp} ({status})"
```

```python
warrior = Hero("Warrior", 150, 30)
ghost   = Hero("Ghost", 0, 20)      # уже мёртв

ghost.attack(warrior)   # → Ghost мёртв и не может атаковать!
warrior.attack(ghost)   # → Warrior → Ghost: -30 hp
print(warrior)          # → [Warrior] HP:150 (жив)
print(ghost)            # → [Ghost] HP:-30 (мёртв)
```

<!--illustration
file: day_2/method_call_chain.png
alt: Методы вызывают другие методы через self — цепочка вызовов
prompt:
Create a Dark RPG UI infographic showing methods calling other methods through self.

Title: "МЕТОДЫ ВЫЗЫВАЮТ МЕТОДЫ ЧЕРЕЗ self" in cream (#e8e0d4).

Three connected glass panels arranged in a cascade/chain:

Panel 1 (teal, top): "attack(self, target)"
    if not self.is_alive(): return
    target.hp -= self.damage
→ arrow labeled "вызывает" glowing teal

Panel 2 (indigo, middle): "is_alive(self)"
    return self.hp > 0
→ returns True/False back to Panel 1

Panel 3 (amber, right): "__str__(self)"
    status = "жив" if self.is_alive() else "мёртв"
→ arrow labeled "вызывает" pointing to Panel 2

All three panels connected by soft organic luminous curves. Arrows show bidirectional calls.

Bottom: key insight panel — "self.метод() внутри класса = вызов метода ЭТОГО объекта"

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

## Задание 1 — Добавь методы к оружию (5 мин)

Возьми класс `Weapon` из вчерашнего урока (атрибуты: `name`, `damage`, `durability`). Добавь метод `use()`: он уменьшает `durability` на 10 и выводит сообщение `"[name] использован. Прочность: X"`. Если `durability` уже 0 — вывести `"[name] сломан!"` и не уменьшать.

<details>
<summary>Решение</summary>

```python
class Weapon:
    def __init__(self, name, damage, durability):
        self.name       = name
        self.damage     = damage
        self.durability = durability

    def use(self):
        if self.durability == 0:
            print(f"{self.name} сломан!")
            return
        self.durability -= 10
        print(f"{self.name} использован. Прочность: {self.durability}")

sword = Weapon("Greatsword", 45, 20)
sword.use()   # → Greatsword использован. Прочность: 10
sword.use()   # → Greatsword использован. Прочность: 0
sword.use()   # → Greatsword сломан!
```

</details>

---

## Задание 2 — __str__ для монстра (7 мин)

Создай класс `Monster` с атрибутами `name`, `hp`, `reward`. Добавь:
- Метод `__str__`, который возвращает строку вида: `"Дракон | HP: 500 | Награда: 1000 монет"`
- Метод `is_defeated()`, который возвращает `True`, если `hp <= 0`
- Метод `take_damage(amount)`, который уменьшает `hp` и выводит статус

<details>
<summary>Решение</summary>

```python
class Monster:
    def __init__(self, name, hp, reward):
        self.name   = name
        self.hp     = hp
        self.reward = reward

    def __str__(self):
        return f"{self.name} | HP: {self.hp} | Награда: {self.reward} монет"

    def is_defeated(self):
        return self.hp <= 0

    def take_damage(self, amount):
        self.hp -= amount
        if self.is_defeated():
            print(f"{self.name} повержен! Получено {self.reward} монет.")
        else:
            print(f"{self.name} получил {amount} урона. HP: {self.hp}")

dragon = Monster("Дракон", 100, 1000)
print(dragon)            # → Дракон | HP: 100 | Награда: 1000 монет
dragon.take_damage(60)   # → Дракон получил 60 урона. HP: 40
dragon.take_damage(50)   # → Дракон повержен! Получено 1000 монет.
```

</details>

---

## Задание 3 — Бой двух героев (8 мин)

Используй полную версию класса `Hero` из Части 4 (с `is_alive`, `attack`, `__str__`). Напиши функцию `battle(hero1, hero2)`, которая симулирует бой:
- Каждый ход hero1 атакует hero2, затем hero2 атакует hero1
- Бой продолжается, пока оба живы
- После боя выводит имя победителя

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

    def attack(self, target):
        target.hp -= self.damage
        print(f"  {self.name} → {target.name}: -{self.damage} (hp: {target.hp})")

    def __str__(self):
        return f"[{self.name}] HP:{self.hp}"

def battle(hero1, hero2):
    round_num = 1
    while hero1.is_alive() and hero2.is_alive():
        print(f"Раунд {round_num}:")
        hero1.attack(hero2)
        if hero2.is_alive():
            hero2.attack(hero1)
        round_num += 1
    winner = hero1 if hero1.is_alive() else hero2
    print(f"Победитель: {winner.name}!")

battle(Hero("Warrior", 80, 25), Hero("Mage", 60, 30))
```

</details>

---

## Задание 4 — Мини-проект: инвентарь с методами (12 мин)

Создай класс `Player` с атрибутами `name`, `hp`, `gold` (монеты). Добавь методы:
- `earn_gold(amount)` — увеличить gold, вывести `"[name] заработал X монет. Итого: Y"`
- `spend_gold(amount)` — уменьшить gold, если хватает. Если нет — вывести `"Недостаточно монет!"`
- `buy_potion(cost, heal)` — купить зелье за `cost` монет и восстановить `heal` hp (используй `spend_gold` внутри метода)
- `__str__` — информация об игроке

Протестируй: создай игрока, заработай 200 монет, купи зелье за 50 (восстанавливает 30 hp), попробуй купить что-то, на что не хватает денег.

<details>
<summary>Решение</summary>

```python
class Player:
    def __init__(self, name, hp, gold):
        self.name = name
        self.hp   = hp
        self.gold = gold

    def earn_gold(self, amount):
        self.gold += amount
        print(f"{self.name} заработал {amount} монет. Итого: {self.gold}")

    def spend_gold(self, amount):
        if self.gold < amount:
            print("Недостаточно монет!")
            return False
        self.gold -= amount
        return True

    def buy_potion(self, cost, heal):
        if self.spend_gold(cost):
            self.hp += heal
            print(f"{self.name} купил зелье (+{heal} hp). HP: {self.hp}")

    def __str__(self):
        return f"Игрок: {self.name} | HP: {self.hp} | Монеты: {self.gold}"

p = Player("Chosen Undead", 80, 50)
print(p)                  # → Игрок: Chosen Undead | HP: 80 | Монеты: 50
p.earn_gold(200)          # → Chosen Undead заработал 200 монет. Итого: 250
p.buy_potion(50, 30)      # → Chosen Undead купил зелье (+30 hp). HP: 110
p.buy_potion(300, 100)    # → Недостаточно монет!
print(p)                  # → Игрок: Chosen Undead | HP: 110 | Монеты: 200
```

</details>

---

<quiz>
[
  {
    "question": "Что делает __str__?",
    "options": [
      "A. Удаляет объект из памяти",
      "B. Вызывается при print(объект) и должен возвращать строку",
      "C. Выводит строку через print()",
      "D. Создаёт объект из строки"
    ],
    "answer": "B",
    "explanation": "__str__ — специальный метод, который Python вызывает автоматически при print(obj) или str(obj). Он должен возвращать строку через return, а не выводить её сам."
  },
  {
    "question": "В чём разница между hero.heal и hero.heal(20)?",
    "options": [
      "A. Никакой разницы",
      "B. hero.heal — это объект метода, hero.heal(20) — его вызов",
      "C. hero.heal выводит код метода, hero.heal(20) удаляет его",
      "D. hero.heal(20) — ошибка синтаксиса"
    ],
    "answer": "B",
    "explanation": "Без скобок — ты получаешь ссылку на метод как объект. Со скобками — вызываешь его. Это частая ошибка: написал hero.is_alive вместо hero.is_alive() и получил True вместо проверки (объект метода всегда truthy)."
  },
  {
    "question": "Метод внутри класса хочет вызвать другой метод того же класса. Как правильно?",
    "options": [
      "A. другой_метод()",
      "B. Hero.другой_метод()",
      "C. self.другой_метод()",
      "D. super().другой_метод()"
    ],
    "answer": "C",
    "explanation": "Через self. Это обращение к методу конкретного объекта. Без self Python будет искать функцию другой_метод в глобальном пространстве и не найдёт её."
  },
  {
    "question": "def attack(self, target): target.hp -= self.damage. Что здесь self, а что target?",
    "options": [
      "A. self — атакующий, target — цель",
      "B. self — цель, target — атакующий",
      "C. Оба одно и то же",
      "D. self — класс, target — объект"
    ],
    "answer": "A",
    "explanation": "self — это тот объект, от которого вызван метод (warrior.attack(mage) → self=warrior). target — аргумент, который мы передаём явно (mage). Поэтому target.hp уменьшается, а self.damage — урон атакующего."
  }
]
</quiz>

---

<!--illustration
file: day_2/skill_tree.png
alt: Дерево навыков Дня 2 — методы экземпляра, __str__, self.метод(), return
prompt:
Create a Dark RPG UI skill tree infographic for Day 2 of Week 7.

Title: "НАВЫКИ ДНЯ 2" in cream (#e8e0d4). Subtitle: "Методы класса" in gray-blue (#8ea4b8).

A branching skill tree with 4 circular nodes connected by organic luminous threads:

Root node (largest, teal glow): wrench/tool icon — "Методы"

Branching:
- Node 1 (teal): sword icon — "Методы экземпляра" — "def attack(self, target):"
- Node 2 (indigo): eye icon — "__str__" — "print(hero) → красиво"
- Node 3 (amber): chain-link icon — "self.метод()" — "методы вызывают методы"
- Node 4 (green): return arrow — "return из метода" — "is_alive() → True/False"

All nodes connected by soft glowing organic vine-like lines.

Bottom checklist glass panel:
✓ def метод(self, ...):
✓ self.атрибут внутри метода
✓ def __str__(self): return "..."
✓ self.другой_метод()

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

← [День 1 — class и __init__](day_1.md) | [День 3 — Наследование →](day_3.md)
