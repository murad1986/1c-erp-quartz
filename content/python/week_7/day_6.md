---
type: lesson
course: "python"
week: 7
day: 6
title: "Практика — система врагов RPG"
concepts: []
prerequisites: "[\"[week_7/day_5](/python/week_7/day_5/)\"]"
tags: [python, ооп, практика, классы, наследование, инкапсуляция]
status: draft
---

# Day 6: Практика — система врагов RPG

> **Сегодня:** собираем всё, что изучили за неделю, в полноценную боевую систему
> **Время:** ~60 минут

---

Сегодня не будет новых концепций. Только практика. Ты построишь систему врагов для RPG — с классами, наследованием, инкапсуляцией и магическими методами. К концу дня у тебя будет работающая мини-игра.

Задания идут по нарастающей — каждое опирается на предыдущее. Читай условие, пробуй написать сам, потом смотри решение.

---

## Задание 1 — Базовый класс Enemy

### Условие

Напиши класс `Enemy` — базу для всех врагов в игре.

Требования:
- Атрибуты: `name`, `_hp`, `_max_hp`, `damage`, `loot` (список строк)
- HP защищено через `_hp` (инкапсуляция). Метод `set_hp(value)` не даёт уйти ниже 0 или выше max_hp
- Метод `is_alive()` — возвращает `True` если `_hp > 0`
- Метод `take_damage(amount)` — уменьшает HP через сеттер
- Метод `attack()` — возвращает строку вида `"Zombie атакует на 15 урона"`
- Метод `drop_loot()` — возвращает список `loot` (пустой если враг жив)
- `__str__` — красивое описание врага
- `__repr__` — строка для отладки

Пример использования:
```python
zombie = Enemy("Zombie", hp=50, damage=15, loot=["Гнилая плоть"])
print(zombie)
print(zombie.attack())
zombie.take_damage(20)
print(zombie)
```

### Решение

```python
class Enemy:
    def __init__(self, name, hp, damage, loot=None):
        self.name = name
        self.damage = damage
        self.loot = loot if loot is not None else []
        self._max_hp = hp
        self._hp = 0
        self.set_hp(hp)

    def get_hp(self):
        return self._hp

    def set_hp(self, value):
        if value < 0:
            self._hp = 0
        elif value > self._max_hp:
            self._hp = self._max_hp
        else:
            self._hp = value

    def is_alive(self):
        return self._hp > 0

    def take_damage(self, amount):
        self.set_hp(self._hp - amount)

    def attack(self):
        return f"{self.name} атакует на {self.damage} урона"

    def drop_loot(self):
        if self.is_alive():
            return []  # живых не грабим
        return self.loot.copy()

    def __str__(self):
        hp_bar_len = 10
        filled = int(hp_bar_len * self._hp / self._max_hp) if self._max_hp > 0 else 0
        bar = "█" * filled + "░" * (hp_bar_len - filled)
        status = "жив" if self.is_alive() else "мёртв"
        return f"[{self.name}] [{bar}] {self._hp}/{self._max_hp} HP ({status})"

    def __repr__(self):
        return (f"Enemy(name={self.name!r}, hp={self._hp!r}, "
                f"damage={self.damage!r}, loot={self.loot!r})")


# Тест:
zombie = Enemy("Zombie", hp=50, damage=15, loot=["Гнилая плоть", "Кость"])
print(zombie)
print(zombie.attack())

zombie.take_damage(20)
print(zombie)

zombie.take_damage(40)  # смертельный удар
print(zombie)
print(f"Дроп: {zombie.drop_loot()}")
```

Ожидаемый вывод:
```
[Zombie] [██████████] 50/50 HP (жив)
Zombie атакует на 15 урона
[Zombie] [██████░░░░] 30/50 HP (жив)
[Zombie] [░░░░░░░░░░] 0/50 HP (мёртв)
Дроп: ['Гнилая плоть', 'Кость']
```

---

## Задание 2 — Подклассы Zombie и Skeleton

### Условие

Создай два подкласса на основе `Enemy`:

**Zombie:**
- HP: 60, damage: 12
- Лут: `["Гнилая плоть"]` (всегда)
- Дополнительный метод `groan()` — возвращает `"Зомби стонет: брррааайнс..."`

**Skeleton:**
- HP: 40, damage: 18
- Лут: `["Кость", "Кость"]`
- Скелеты уязвимы к дробящему оружию: метод `take_blunt_damage(amount)` наносит `amount * 1.5` урона (округлить до целого)
- `__str__` — добавить к стандартному описанию пометку `[СКЕЛЕТ]`

Пример:
```python
z = Zombie("Пещерный Зомби")
s = Skeleton("Лучник-Скелет")
print(z)
print(z.groan())
print(s)
s.take_blunt_damage(20)
print(s)
```

### Решение

```python
class Zombie(Enemy):
    def __init__(self, name):
        super().__init__(
            name=name,
            hp=60,
            damage=12,
            loot=["Гнилая плоть"]
        )

    def groan(self):
        return f"{self.name} стонет: брррааайнс..."


class Skeleton(Enemy):
    def __init__(self, name):
        super().__init__(
            name=name,
            hp=40,
            damage=18,
            loot=["Кость", "Кость"]
        )

    def take_blunt_damage(self, amount):
        boosted = int(amount * 1.5)
        print(f"  {self.name} получает {boosted} дробящего урона (x1.5)!")
        self.take_damage(boosted)

    def __str__(self):
        base = super().__str__()
        return f"[СКЕЛЕТ] {base}"


# Тест:
z = Zombie("Пещерный Зомби")
s = Skeleton("Лучник-Скелет")

print(z)
print(z.groan())
print()
print(s)
s.take_blunt_damage(20)
print(s)
print(isinstance(z, Enemy))   # True
print(isinstance(s, Zombie))  # False
```

<!--illustration
file: day_6/enemy_hierarchy.png
alt: Полная иерархия классов врагов — Enemy, Zombie, Skeleton, Boss с уникальными методами
prompt:
Create a Dark RPG UI infographic showing the complete enemy class hierarchy built in practice.

Title: "ИЕРАРХИЯ ВРАГОВ — СИСТЕМА RPG" in cream (#e8e0d4).

A tree structure:

ROOT (top, large teal panel): "Enemy"
- Attributes listed: name, _hp, _max_hp, damage, loot
- Methods: set_hp(), is_alive(), take_damage(), attack(), drop_loot(), __str__, __repr__

Three child nodes connected by organic glowing arrows:

LEFT (amber panel): "Zombie"
- Unique method (amber highlight): groan() — "брррааайнс..."
- HP: 60, damage: 12
- Icon: zombie silhouette

CENTER (indigo panel): "Skeleton"
- Unique method (indigo highlight): take_blunt_damage() — "x1.5 урон"
- __str__ override: "[СКЕЛЕТ] ..."
- HP: 40, damage: 18
- Icon: skeleton/bone silhouette

RIGHT (red-amber panel): "Boss"
- Unique methods (highlighted): update_phase(), attack() override
- phase attribute (phase 1 → phase 2 at 50% HP)
- HP: 300, damage: 35
- Icon: crown/boss silhouette

Each child node shows inherited methods in grey and unique methods in color.

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

## Задание 3 — Boss со специальной атакой

### Условие

Создай класс `Boss(Enemy)`:

- HP: 300, damage: 35
- Лут: список передаётся при создании (у каждого босса свой)
- Переопределяет метод `attack()`: с вероятностью 30% атака двойная
- Атрибут `phase` — начинается с 1, переходит в 2 когда HP < 50% от максимума
- Метод `update_phase()` — вызывается автоматически при получении урона, обновляет `phase`
- Когда фаза меняется с 1 на 2 — печатает сообщение
- В фазе 2 вероятность двойной атаки вырастает до 50%
- `__str__` — добавить информацию о фазе

Подсказка: для случайности используй `import random` и `random.random()` — возвращает число от 0.0 до 1.0.

```python
import random
# random.random() < 0.3  →  30% вероятность
```

### Решение

```python
import random


class Boss(Enemy):
    def __init__(self, name, loot=None):
        super().__init__(
            name=name,
            hp=300,
            damage=35,
            loot=loot if loot is not None else ["Душа Босса"]
        )
        self.phase = 1

    def update_phase(self):
        if self.phase == 1 and self._hp <= self._max_hp * 0.5:
            self.phase = 2
            print(f"\n  !! {self.name} ПЕРЕХОДИТ В ФАЗУ 2 !!")
            print(f"  Ярость усиливает его атаки...\n")

    def take_damage(self, amount):
        super().take_damage(amount)
        self.update_phase()

    def attack(self):
        double_chance = 0.5 if self.phase == 2 else 0.3
        if random.random() < double_chance:
            total = self.damage * 2
            return f"{self.name} наносит ДВОЙНОЙ УДАР! {total} урона!"
        return f"{self.name} атакует на {self.damage} урона"

    def __str__(self):
        base = super().__str__()
        return f"[БОСС | Фаза {self.phase}] {base}"


# Тест:
random.seed(42)  # фиксируем случайность для воспроизводимого теста

boss = Boss("Повелитель Тьмы", loot=["Клинок Хаоса", "Душа Повелителя"])
print(boss)

# Несколько атак
for _ in range(4):
    print(boss.attack())

# Наносим большой урон — смотрим переход в фазу 2
boss.take_damage(160)
print(boss)
print(boss.attack())
```

---

## Задание 4 — Полная боевая система

### Условие

Собери всё в мини-игру с функцией `battle(hero_hp, enemy)` и основным циклом.

Требования:
- Класс `Inventory` с `__len__`, `__str__`, `add_item(item_name)`
- Функция `battle(hero_hp, enemy)` — возвращает `(оставшееся_hp, добытый_лут)`
  - Пошаговый бой: враг и герой бьют по очереди
  - Герой бьёт на фиксированный урон 25
  - Используй `try/except` для защиты от некорректных входных данных
- Функция `generate_enemy()` — случайно создаёт Zombie, Skeleton или Boss (10% шанс босса)
- Основной цикл: 5 раундов, каждый раунд — новый враг, трофеи накапливаются в инвентарь

### Решение

```python
import random


# ---- Инвентарь ----

class Inventory:
    def __init__(self, owner):
        self.owner = owner
        self._items = []

    def add_item(self, item_name):
        self._items.append(item_name)

    def __len__(self):
        return len(self._items)

    def __str__(self):
        if not self._items:
            return f"Инвентарь [{self.owner}]: пусто"
        items_str = ", ".join(self._items)
        return f"Инвентарь [{self.owner}] ({len(self)} пред.): {items_str}"


# ---- Боевая функция ----

def battle(hero_hp, enemy):
    """
    Проводит бой между героем (hero_hp) и врагом.
    Возвращает (оставшееся_hp, список_лута).
    """
    if not isinstance(hero_hp, int) or hero_hp <= 0:
        raise ValueError(f"HP героя должно быть положительным числом, получено: {hero_hp!r}")
    if not isinstance(enemy, Enemy):
        raise TypeError(f"enemy должен быть экземпляром Enemy, получено: {type(enemy).__name__}")

    print(f"\n{'='*40}")
    print(f"  Бой начинается: Герой ({hero_hp} HP) vs {enemy.name}")
    print(f"{'='*40}")

    current_hero_hp = hero_hp
    hero_damage = 25
    round_num = 0

    while current_hero_hp > 0 and enemy.is_alive():
        round_num += 1
        print(f"\n  -- Раунд {round_num} --")

        # Герой атакует
        enemy.take_damage(hero_damage)
        print(f"  Герой: наносит {hero_damage} урона → {enemy}")

        if not enemy.is_alive():
            break

        # Враг атакует
        attack_msg = enemy.attack()
        print(f"  {attack_msg}")

        # Извлекаем урон из строки атаки
        # Ищем числа в строке атаки
        words = attack_msg.split()
        enemy_dmg = 0
        for word in reversed(words):
            clean = word.rstrip("!")
            if clean.isdigit():
                enemy_dmg = int(clean)
                break

        current_hero_hp -= enemy_dmg
        if current_hero_hp < 0:
            current_hero_hp = 0
        print(f"  Герой: {current_hero_hp} HP")

    # Итог боя
    print(f"\n  {'Герой победил!' if enemy.is_alive() is False else 'Герой погиб...'}")

    loot = enemy.drop_loot()
    if loot:
        print(f"  Добыто: {', '.join(loot)}")

    return current_hero_hp, loot


# ---- Генератор врагов ----

ZOMBIE_NAMES = ["Деревенский Мертвец", "Утопленник", "Пещерный Зомби", "Стражник Тьмы"]
SKELETON_NAMES = ["Костяной Лучник", "Скелет-Воин", "Древний Скелет", "Проклятый Страж"]
BOSS_NAMES = ["Повелитель Тьмы", "Король Мертвецов", "Нежить Предвечная"]


def generate_enemy():
    """Случайно генерирует врага. 10% шанс босса."""
    roll = random.random()
    if roll < 0.10:
        name = random.choice(BOSS_NAMES)
        return Boss(name, loot=["Легендарный Клинок", "Душа Босса", "Ключ от крепости"])
    elif roll < 0.55:
        name = random.choice(ZOMBIE_NAMES)
        return Zombie(name)
    else:
        name = random.choice(SKELETON_NAMES)
        return Skeleton(name)


# ---- Основной игровой цикл ----

def main():
    print("=" * 50)
    print("  DARK DUNGEONS — Система врагов v1.0")
    print("=" * 50)

    hero_hp = 150
    inventory = Inventory("Герой")
    wins = 0
    losses = 0

    for round_num in range(1, 6):
        print(f"\n\n[РАУНД {round_num}/5]  Герой: {hero_hp} HP")

        if hero_hp <= 0:
            print("Герой мёртв. Игра окончена.")
            break

        enemy = generate_enemy()

        try:
            hero_hp, loot = battle(hero_hp, enemy)
            if enemy.is_alive() is False:
                wins += 1
                for item in loot:
                    inventory.add_item(item)
            else:
                losses += 1
        except (ValueError, TypeError) as e:
            print(f"Ошибка боя: {e}")

    # Финальная статистика
    print(f"\n\n{'='*50}")
    print(f"  ИГРА ОКОНЧЕНА")
    print(f"  Победы: {wins} | Поражения: {losses}")
    print(f"  Оставшееся HP: {hero_hp}")
    print(f"  {inventory}")
    print(f"{'='*50}")


# Запускаем с фиксированным сидом для воспроизводимости
random.seed(7)
main()
```

<!--illustration
file: day_6/battle_loop.png
alt: Блок-схема боевой системы — generate_enemy, battle loop, drop_loot, Inventory
prompt:
Create a Dark RPG UI infographic showing the battle system flowchart.

Title: "БОЕВОЙ ЦИКЛ — АРХИТЕКТУРА" in cream (#e8e0d4).

A flowchart flowing left to right and down:

START: "generate_enemy()" — teal orb
→ random roll: 10% Boss / 45% Zombie / 45% Skeleton (shown as probability split)

→ "battle(hero_hp, enemy)" — main fight function (large indigo panel)
    Inside panel: "while hero_hp > 0 and enemy.is_alive():"
    → hero deals 25 damage → enemy.take_damage(25)
    → enemy.attack() → hero takes damage

→ Decision diamond: "enemy.is_alive()?"
   → False: "drop_loot()" → amber loot items floating out
   → items flow into: "Inventory.add_item()" — teal panel with items accumulating

→ "Следующий раунд?" decision
   → Да: back to generate_enemy()
   → Нет / hero_hp <= 0: "Итог игры" — final green panel

Bottom: "5 раундов → побед: X | поражений: Y | инвентарь: N предметов"

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

## Финальная структура классов

К концу задания у тебя должна получиться такая иерархия:

```
Enemy
├── Zombie
│   └── метод: groan()
├── Skeleton
│   └── метод: take_blunt_damage()
└── Boss
    └── методы: update_phase(), attack() (переопределён)

Inventory
└── методы: add_item(), __len__(), __str__()

Функции:
├── battle(hero_hp, enemy) → (hp, loot)
└── generate_enemy() → Enemy
```

---

## Бонус: добавь сам

Если справился и хочешь большего — попробуй расширить систему:

1. **Лечение:** после каждого выигранного боя герой восстанавливает 20 HP (но не больше 150)
2. **Lich(Boss):** новый подкласс босса, который при переходе во фазу 2 призывает двух скелетов
3. **Редкий дроп:** скелет с 20% шансом роняет `"Редкая Кость"` вместо обычной
4. **Статистика урона:** `battle()` возвращает ещё и суммарный урон, нанесённый врагом

---

← [Day 5 — Магические методы](/python/week_7/day_5/) | [Day 7 — Лонгрид →](/python/week_7/day_7/)
