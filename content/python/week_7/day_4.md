---
type: lesson
course: "[[python_basics/README]]"
week: 7
day: 4
title: "Инкапсуляция — защищаем данные героя"
concepts: [инкапсуляция, _private конвенция, геттеры и сеттеры, валидация данных]
prerequisites: "[\"[[week_7/day_3]]\"]"
tags: [python, ооп, классы, инкапсуляция, геттеры, сеттеры]
status: draft
---

# Day 4: Инкапсуляция — защищаем данные героя

> **Сегодня:** учимся защищать внутренние данные объекта от случайного взлома снаружи
> **Время:** ~40 минут

---

## Часть 1 — Проблема: объект можно сломать снаружи

Представь: ты написал класс `Hero`. Всё работает. Но потом кто-то (или ты сам в 2 часа ночи) пишет вот такое:

```python
hero.hp = -999
```

И герой с отрицательным HP продолжает ходить по миру. В Dark Souls такого нет — когда HP падает до 0, персонаж умирает. Отрицательный HP — это баг.

Посмотрим на пример:

```python
class Hero:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def status(self):
        print(f"{self.name}: {self.hp} HP")

hero = Hero("Chosen Undead", 100)
hero.status()  # Chosen Undead: 100 HP

# Ничто не мешает нам сломать объект:
hero.hp = -999
hero.status()  # Chosen Undead: -999 HP  <-- баг!

# Или ещё хуже:
hero.hp = "много"
hero.status()  # упадёт с ошибкой где-то в другом месте
```

Python не запрещает менять атрибуты напрямую. Это свобода, но и опасность.

**Инкапсуляция** — это принцип ООП: прячем внутренние данные объекта и даём доступ к ним только через специальные методы. Объект сам контролирует, что в него попадает.

<!--illustration
file: day_4/broken_object.png
alt: До и после инкапсуляции — герой с отрицательным HP vs правильный клампинг до 0
prompt:
Create a Dark RPG UI infographic showing a broken object vs protected object as before/after.

Title: "ИНКАПСУЛЯЦИЯ: ДО И ПОСЛЕ" in cream (#e8e0d4).

LEFT panel ("Без инкапсуляции", cracked/broken aesthetic, dim red-amber tint):
- Code: hero.hp = -999
- Below: a character silhouette with health bar showing "-999 HP" in red, still walking
- Skull icons and crack effects
- Caption: "Персонаж с -999 HP продолжает жить. Баг!"
- hero.hp = "много" → ошибка в другом месте (dim amber warning)

RIGHT panel ("С инкапсуляцией", clean teal glow, green accent):
- Code: hero.set_hp(-999)
- Inside set_hp(): if value < 0: self._hp = 0
- Health bar showing "0 HP" — properly dead, clean
- Check mark icon
- Caption: "set_hp(-999) → _hp = 0. Правильная смерть!"

Large glowing arrow between panels labeled "Инкапсуляция"

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

## Часть 2 — Конвенция `_hp`: «не трогай снаружи»

В Python нет жёсткого запрета на доступ к атрибутам. Но есть **договорённость** между разработчиками:

> Если атрибут начинается с одного подчёркивания `_hp` — это сигнал: «этот атрибут внутренний, не меняй его напрямую снаружи».

Python не будет кричать и падать с ошибкой. Это просто **социальный контракт**. Как знак «не входить» на двери — физически войти можно, но ты знаешь, что не надо.

```python
class Hero:
    def __init__(self, name, hp):
        self.name = name
        self._hp = hp  # одно подчёркивание = "внутренний атрибут"

hero = Hero("Knight Artorias", 150)

# Технически можно, но так делать НЕ НАДО:
hero._hp = -999  # нарушаем конвенцию

# Правильно — через методы (см. ниже)
```

Когда ты видишь `_что_то` в чужом коде — это сигнал: «автор не хочет, чтобы ты это трогал напрямую».

---

## Часть 3 — Геттеры и сеттеры: контролируем доступ

Чтобы дать удобный и **безопасный** способ читать и менять `_hp`, пишем два метода:

- **геттер** (getter) — получить значение: `get_hp()`
- **сеттер** (setter) — установить значение: `set_hp(value)`

```python
class Hero:
    def __init__(self, name, hp):
        self.name = name
        self._hp = hp  # внутренний атрибут

    def get_hp(self):
        """Возвращает текущее HP героя."""
        return self._hp

    def set_hp(self, value):
        """Устанавливает HP героя."""
        self._hp = value

    def status(self):
        print(f"{self.name}: {self._hp} HP")


hero = Hero("Chosen Undead", 100)
print(hero.get_hp())  # 100

hero.set_hp(80)
print(hero.get_hp())  # 80
```

Пока что это просто обёртка. Настоящая сила — в следующем шаге.

<!--illustration
file: day_4/getter_setter.png
alt: Геттер и сеттер как охраняемые двери к приватному атрибуту _hp
prompt:
Create a Dark RPG UI infographic showing getter and setter as guarded doors to a private attribute.

Title: "ГЕТТЕР И СЕТТЕР — ДВЕРИ К _hp" in cream (#e8e0d4).

Central: a dark glass vault/chest icon labeled "_hp = 120" (private, indigo glow, lock icon).

LEFT door (teal, open, glass panel): "get_hp()"
    def get_hp(self):
        return self._hp
- Icon: open door, read-only symbol
- Label: "Только читать — всегда разрешено"
- Arrow: → returns 120

RIGHT door (amber, with guard/gate): "set_hp(value)"
    def set_hp(self, value):
        if value < 0: self._hp = 0
        else: self._hp = value
- Icon: guarded gate with validation checks
- Label: "Записать — только с проверкой"
- set_hp(80) → _hp = 80 ✓ (green)
- set_hp(-999) → _hp = 0 ✓ (green, clamped)

Bottom caption: "Объект сам контролирует свои данные" in cream.

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

## Часть 4 — Валидация в сеттере: HP не уходит в минус

Сеттер — это не просто `self._hp = value`. Это **место для проверки**. Добавляем логику:

```python
class Hero:
    def __init__(self, name, hp):
        self.name = name
        self._hp = 0     # сначала 0
        self.set_hp(hp)  # потом устанавливаем через сеттер — сразу с проверкой!

    def get_hp(self):
        return self._hp

    def set_hp(self, value):
        if not isinstance(value, int):
            raise TypeError(f"HP должно быть числом, получено: {type(value).__name__}")
        if value < 0:
            self._hp = 0  # не уходим в минус — просто 0 (смерть)
        else:
            self._hp = value

    def is_alive(self):
        return self._hp > 0

    def take_damage(self, damage):
        self.set_hp(self._hp - damage)  # используем сеттер, а не прямое присвоение

    def status(self):
        alive = "жив" if self.is_alive() else "мёртв"
        print(f"{self.name}: {self._hp} HP ({alive})")


# Тестируем:
hero = Hero("Chosen Undead", 100)
hero.status()          # Chosen Undead: 100 HP (жив)

hero.take_damage(30)
hero.status()          # Chosen Undead: 70 HP (жив)

hero.take_damage(200)  # урон больше HP
hero.status()          # Chosen Undead: 0 HP (мёртв)

# Попробуем сломать:
try:
    hero.set_hp("много")
except TypeError as e:
    print(f"Ошибка: {e}")  # Ошибка: HP должно быть числом, получено: str
```

Обрати внимание на хитрость в `__init__`: мы сначала ставим `self._hp = 0`, а потом вызываем `set_hp(hp)`. Так валидация работает с самого первого момента создания объекта.

<!--illustration
file: day_4/validation_flow.png
alt: Блок-схема валидации внутри set_hp() — проверки типа, нижней и верхней границы
prompt:
Create a Dark RPG UI infographic showing a flowchart inside set_hp() validation.

Title: "ВАЛИДАЦИЯ В set_hp(value)" in cream (#e8e0d4).

A vertical flowchart with glass diamond decision nodes and panel result boxes:

START: "set_hp(value)" called — teal orb at top

Decision 1 (diamond): "isinstance(value, int)?"
→ Нет: red-amber box "raise TypeError!" with skull icon
→ Да: continue

Decision 2 (diamond): "value < 0?"
→ Да: amber box "self._hp = 0" (clamp to death) with down-arrow
→ Нет: continue

Decision 3 (diamond): "value > self._max_hp?"
→ Да: indigo box "self._hp = self._max_hp" (clamp to max) with up-arrow
→ Нет: green box "self._hp = value" ✓ (valid range)

Each decision diamond has soft colored glow. Arrows are organic curves with directional glow.

Bottom: example call trace: set_hp(-50) → value < 0 → self._hp = 0 in amber monospace.

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

## Часть 5 — Полный пример: герой с защищёнными атрибутами

Добавим ещё `_max_hp` — максимальное HP, которое тоже нужно защищать:

```python
class Hero:
    def __init__(self, name, max_hp):
        self.name = name
        self._max_hp = 0
        self._hp = 0
        self.set_max_hp(max_hp)
        self.set_hp(max_hp)  # начинаем с полным HP

    # --- Геттеры ---
    def get_hp(self):
        return self._hp

    def get_max_hp(self):
        return self._max_hp

    # --- Сеттеры ---
    def set_max_hp(self, value):
        if value <= 0:
            raise ValueError("Максимальное HP должно быть больше 0")
        self._max_hp = value

    def set_hp(self, value):
        if value < 0:
            self._hp = 0
        elif value > self._max_hp:
            self._hp = self._max_hp  # не превышаем максимум
        else:
            self._hp = value

    # --- Методы ---
    def is_alive(self):
        return self._hp > 0

    def take_damage(self, damage):
        print(f"  {self.name} получает {damage} урона")
        self.set_hp(self._hp - damage)

    def heal(self, amount):
        old_hp = self._hp
        self.set_hp(self._hp + amount)
        healed = self._hp - old_hp
        print(f"  {self.name} восстанавливает {healed} HP")

    def status(self):
        bar_length = 20
        filled = int(bar_length * self._hp / self._max_hp)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"{self.name}: [{bar}] {self._hp}/{self._max_hp} HP")

    def __str__(self):
        return f"Hero({self.name}, {self._hp}/{self._max_hp} HP)"


# Игра:
hero = Hero("Knight Artorias", 200)
hero.status()

hero.take_damage(80)
hero.status()

hero.heal(200)  # лечимся сверх максимума — не страшно, сеттер ограничит
hero.status()

hero.take_damage(300)  # смертельный удар
hero.status()
print(f"Жив? {hero.is_alive()}")
```

Вывод:
```
Knight Artorias: [████████████████████] 200/200 HP
  Knight Artorias получает 80 урона
Knight Artorias: [████████████░░░░░░░░] 120/200 HP
  Knight Artorias восстанавливает 80 HP
Knight Artorias: [████████████████████] 200/200 HP
  Knight Artorias получает 300 урона
Knight Artorias: [░░░░░░░░░░░░░░░░░░░░] 0/200 HP
Жив? False
```

---

## Камень в рюкзак: двойное подчёркивание `__hp`

В Python есть ещё `__hp` (двойное подчёркивание). Это называется **name mangling** — Python буквально переименовывает атрибут в `_ClassName__hp`, чтобы его труднее было найти снаружи.

```python
class Example:
    def __init__(self):
        self.__secret = 42  # двойное подчёркивание

e = Example()
# e.__secret  <-- AttributeError: атрибут не найден!
# e._Example__secret  <-- работает, но это уже хак
```

В реальном коде `__` используется редко и в курсе мы его использовать не будем. Одного подчёркивания `_` вполне достаточно для обозначения «внутреннего» атрибута.

---

## Итог дня

| Концепция | Что это | Пример |
|-----------|---------|--------|
| `_атрибут` | Конвенция «не трогай снаружи» | `self._hp = 100` |
| Геттер | Метод для чтения атрибута | `def get_hp(self): return self._hp` |
| Сеттер | Метод для записи с проверкой | `def set_hp(self, value): ...` |
| Валидация | Проверка данных в сеттере | `if value < 0: self._hp = 0` |

**Главная идея:** объект сам отвечает за корректность своих данных. Не надо надеяться, что снаружи напишут правильно.

---

> **Задание на подумать:** у тебя есть класс `Weapon` с атрибутом `damage`. Какую валидацию стоит добавить в `set_damage()`? Что должно произойти, если передать отрицательный урон? А строку вместо числа?

---

---

## Задание 1 — Оружие с защищённым уроном (10 мин)

Создай класс `Weapon` с атрибутом `_damage`. Добавь `get_damage()` и `set_damage(value)`. В сеттере: урон должен быть от 1 до 999. Если нет — raise ValueError.

```python
# Что должно работать:
sword = Weapon("Меч", 50)
print(sword.get_damage())   # → 50
sword.set_damage(100)
print(sword.get_damage())   # → 100
sword.set_damage(-5)        # → ValueError: Урон должен быть от 1 до 999
```

<details>
<summary>Решение</summary>

```python
class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self._damage = 0
        self.set_damage(damage)

    def get_damage(self):
        return self._damage

    def set_damage(self, value):
        if not isinstance(value, int):
            raise TypeError("Урон должен быть числом")
        if value < 1 or value > 999:
            raise ValueError("Урон должен быть от 1 до 999")
        self._damage = value

sword = Weapon("Меч", 50)
print(sword.get_damage())   # → 50
sword.set_damage(100)
print(sword.get_damage())   # → 100
```

</details>

---

## Задание 2 — Монстр с защищённым HP (10 мин)

Возьми класс `Monster` из предыдущих уроков. Переведи `hp` в `_hp` с геттером и сеттером. Сеттер: HP не может быть отрицательным (клампируй до 0), не может превышать `_max_hp`.

```python
goblin = Monster("Гоблин", 80)
goblin.take_damage(30)
print(goblin.get_hp())      # → 50
goblin.take_damage(9999)
print(goblin.get_hp())      # → 0  (не -9949!)
print(goblin.is_alive())    # → False
```

<details>
<summary>Решение</summary>

```python
class Monster:
    def __init__(self, name, max_hp):
        self.name = name
        self._max_hp = max_hp
        self._hp = max_hp

    def get_hp(self):
        return self._hp

    def set_hp(self, value):
        self._hp = max(0, min(value, self._max_hp))

    def take_damage(self, damage):
        self.set_hp(self._hp - damage)

    def is_alive(self):
        return self._hp > 0

goblin = Monster("Гоблин", 80)
goblin.take_damage(30)
print(goblin.get_hp())    # → 50
goblin.take_damage(9999)
print(goblin.get_hp())    # → 0
print(goblin.is_alive())  # → False
```

</details>

---

## Задание 3 — Игрок с кошельком (15 мин)

Создай класс `Player` с защищённым атрибутом `_gold`. Добавь методы:
- `get_gold()` — возвращает текущее золото
- `earn_gold(amount)` — добавляет золото (amount > 0, иначе ValueError)
- `spend_gold(amount)` — тратит золото. Если не хватает — ValueError с сообщением «Недостаточно золота: нужно X, есть Y»

```python
hero = Player("Артём")
hero.earn_gold(100)
hero.spend_gold(40)
print(hero.get_gold())     # → 60
hero.spend_gold(9999)      # → ValueError: Недостаточно золота: нужно 9999, есть 60
```

<details>
<summary>Решение</summary>

```python
class Player:
    def __init__(self, name):
        self.name = name
        self._gold = 0

    def get_gold(self):
        return self._gold

    def earn_gold(self, amount):
        if amount <= 0:
            raise ValueError("Количество золота должно быть > 0")
        self._gold += amount

    def spend_gold(self, amount):
        if amount > self._gold:
            raise ValueError(
                f"Недостаточно золота: нужно {amount}, есть {self._gold}"
            )
        self._gold -= amount

hero = Player("Артём")
hero.earn_gold(100)
hero.spend_gold(40)
print(hero.get_gold())  # → 60
```

</details>

---

## Задание 4 — Мини-проект: полный класс Hero (15 мин)

Собери всё вместе. Класс `Hero` с инкапсуляцией:
- `_hp`, `_max_hp` с клампингом через сеттер
- `_level` (только чтение через геттер, без сеттера)
- `level_up()` — повышает уровень, увеличивает max_hp на 20, восстанавливает HP
- `hp_bar()` — возвращает строку `"███░░ 60/100"`
- `__str__` — красивый вывод

```python
hero = Hero("Странник", hp=100)
hero.take_damage(40)
print(hero.hp_bar())       # → ███░░░░░░░ 60/100
hero.level_up()
print(hero)                # → Странник | Ур.2 | HP: 120/120
```

<details>
<summary>Решение</summary>

```python
class Hero:
    def __init__(self, name, hp=100):
        self.name = name
        self._max_hp = hp
        self._hp = hp
        self._level = 1

    def get_hp(self):
        return self._hp

    def set_hp(self, value):
        self._hp = max(0, min(value, self._max_hp))

    def get_level(self):
        return self._level

    def take_damage(self, damage):
        self.set_hp(self._hp - damage)

    def level_up(self):
        self._level += 1
        self._max_hp += 20
        self._hp = self._max_hp

    def hp_bar(self):
        filled = round(self._hp / self._max_hp * 10)
        bar = "█" * filled + "░" * (10 - filled)
        return f"{bar} {self._hp}/{self._max_hp}"

    def __str__(self):
        return f"{self.name} | Ур.{self._level} | HP: {self._hp}/{self._max_hp}"

hero = Hero("Странник", hp=100)
hero.take_damage(40)
print(hero.hp_bar())  # → ██████░░░░ 60/100
hero.level_up()
print(hero)           # → Странник | Ур.2 | HP: 120/120
```

</details>

<!--illustration
file: day_4/skill_tree.png
alt: Дерево навыков Дня 4 — _private, геттер, сеттер, валидация
prompt:
Create a Dark RPG UI skill tree infographic for Day 4 of Week 7.

Title: "НАВЫКИ ДНЯ 4" in cream (#e8e0d4). Subtitle: "Инкапсуляция" in gray-blue (#8ea4b8).

A branching skill tree with 4 circular nodes:

Root node (largest, indigo glow): lock/shield icon — "Инкапсуляция"

Branching:
- Node 1 (indigo): underscore icon — "_private" — "_hp = конвенция «не трогай»"
- Node 2 (teal): eye/read icon — "get_hp()" — "геттер — только читать"
- Node 3 (amber): gate icon — "set_hp()" — "сеттер — записать с проверкой"
- Node 4 (green): shield/checkmark icon — "Валидация" — "if value < 0: self._hp = 0"

Connected by soft organic luminous vines.

Bottom checklist:
✓ self._hp (внутренний атрибут)
✓ def get_hp(self): return self._hp
✓ def set_hp(self, value): ...
✓ валидация: тип + диапазон

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

← [Day 3 — Наследование](day_3.md) | [Day 5 — Магические методы →](day_5.md)
