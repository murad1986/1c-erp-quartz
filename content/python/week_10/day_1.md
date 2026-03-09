---
type: lesson
course: "[[python_basics/README]]"
week: 10
day: 1
title: "День 1 — import random: квест становится живым"
concepts: [import random, random.choice, random.randint, случайные события в игре]
prerequisites: "[\"[[week_9/day_7]]\"]"
tags: [python, текстовый-квест, random, проект]
status: draft
---

# День 1 — import random: квест становится живым

← [Week 9 — Финал](../week_9/day_7.md) | [День 2 — Модули →](day_2.md)

---

> **Сегодня:** добавляем случайность — теперь каждое прохождение квеста будет разным
> **Время:** ~40 минут

---

Твой квест пока предсказуем: зашёл в комнату — увидел одно и то же. Именно поэтому в Dark Souls враги появляются снова после костра, а в Minecraft каждый мир уникален. Случайность — это то, что делает игры живыми.

Сегодня добавим `import random` — один из самых полезных модулей Python. После этого: случайный лут, случайные комментарии врагов, случайные события при переходе между комнатами. Каждое прохождение — новый опыт.

---

## Концепция 1 — Что такое import

До сих пор весь твой код умещался в одном файле. Но Python поставляется с огромной стандартной библиотекой — готовых модулей на все случаи жизни. `import` — это способ подключить любой из них.

```python
import random   # подключаем модуль random

# Теперь все функции random доступны через random.название_функции
print(random.randint(1, 6))   # → случайное число от 1 до 6 (как кубик)
```

Модуль — это просто файл с кодом. `random.py` написан командой Python и содержит десятки функций для работы со случайными числами. Ты подключаешь его одной строкой и получаешь весь этот арсенал.

Три самые важные функции:

```python
import random

# Случайное целое число в диапазоне (включительно)
damage = random.randint(5, 15)        # → 7, или 11, или 5, или 15...

# Случайный элемент из списка
directions = ["север", "юг", "запад"]
chosen = random.choice(directions)    # → "юг" или "север" или "запад"

# Случайное число от 0.0 до 1.0 (для вероятностей)
roll = random.random()                # → 0.742..., 0.123..., 0.999...
if roll < 0.3:                        # 30% шанс
    print("Критический удар!")
```

---

## Концепция 2 — Случайный урон в бою

Сейчас урон фиксированный: игрок всегда бьёт на 10, враг — на 5. Добавим разброс, как в настоящих RPG:

```python
import random

def battle(player, enemy):
    print(f"\nНачался бой с {enemy.name}!")

    while enemy.is_alive() and player.hp > 0:
        # Урон игрока: базовый ± 20%
        player_damage = random.randint(
            int(player.damage * 0.8),
            int(player.damage * 1.2)
        )
        enemy.take_damage(player_damage)
        print(f"Ты атакуешь на {player_damage} урона. HP {enemy.name}: {enemy.hp}")

        if not enemy.is_alive():
            break

        # Урон врага: тоже с разбросом
        enemy_damage = random.randint(
            int(enemy.damage * 0.8),
            int(enemy.damage * 1.2)
        )
        player.hp -= enemy_damage
        print(f"{enemy.name} бьёт тебя на {enemy_damage} урона. Твой HP: {player.hp}")

    if player.hp <= 0:
        print("Ты погиб.")
        return False
    print(f"Победа! +{enemy.xp_reward} XP")
    player.xp += enemy.xp_reward
    return True
```

Теперь каждый бой уникален. Иногда враг выбивает критичный урон, иногда — почти промахивается.

---

## Концепция 3 — Случайные события при переходе

Добавим события, которые происходят при переходе между комнатами — с определённой вероятностью:

```python
import random

RANDOM_EVENTS = [
    "Ты слышишь далёкий стон. Что-то живое бродит по коридорам.",
    "Капля воды падает с потолка тебе на шею.",
    "Факел мигает. На секунду темнота поглощает всё.",
    "Под ногой хрустит кость. Чья-то.",
    "Сквозняк доносит запах серы.",
]

def maybe_random_event():
    """С вероятностью 25% выводит случайное атмосферное событие."""
    if random.random() < 0.25:
        event = random.choice(RANDOM_EVENTS)
        print(f"\n  ✦ {event}\n")
```

Вызываем в game loop при каждом «идти»:

```python
elif verb == "идти" and args:
    direction = args[0]
    if direction in player.current_room.exits:
        player.current_room = rooms[player.current_room.exits[direction]]
        maybe_random_event()          # ← добавили
        describe_room(player.current_room, rooms)
    else:
        print("Туда не пройти.")
```

---

## Концепция 4 — Случайный лут

Вместо фиксированного лута враг роняет случайный предмет из таблицы:

```python
LOOT_TABLE = {
    "обычный": [
        Item("Монета", "Старая медная монета"),
        Item("Тряпка", "Грязная тряпка. Бесполезна"),
        Item("Кость", "Обычная кость"),
    ],
    "редкий": [
        Item("Зелье здоровья", "Восстанавливает 20 HP"),
        Item("Кинжал", "Острый кинжал"),
    ],
    "эпик": [
        Item("Огненный меч", "Пылает синим огнём"),
    ],
}

def drop_loot(enemy):
    """Определяет лут после победы над врагом."""
    roll = random.random()
    if roll < 0.60:        # 60% — обычный
        return random.choice(LOOT_TABLE["обычный"])
    elif roll < 0.90:      # 30% — редкий
        return random.choice(LOOT_TABLE["редкий"])
    else:                  # 10% — эпик
        return random.choice(LOOT_TABLE["эпик"])
```

В battle() при победе:
```python
loot = drop_loot(enemy)
player.current_room.items.append(loot)
print(f"Враг выронил: {loot.name}!")
```

<!--illustration
file: day_1/day_1_random.png
alt: Таблица лута с тремя уровнями редкости
prompt:
RPG loot drop table visualization, showing probability tiers.

Three vertical panels side by side, styled as item rarity cards:

LEFT panel — "ОБЫЧНЫЙ (60%)" — grey/teal border:
  Items listed with icons: Монета, Тряпка, Кость
  HP bar style probability: ████████████░░░░░░░░ 60%

CENTER panel — "РЕДКИЙ (30%)" — indigo border with glow:
  Зелье здоровья, Кинжал
  HP bar: ██████░░░░░░░░░░░░░░ 30%

RIGHT panel — "ЭПИК (10%)" — amber border, bright glow:
  Огненный меч
  HP bar: ██░░░░░░░░░░░░░░░░░░ 10%

Below all panels: dice icon rolling with "random.random()" label.
Three code snippets as floating stone tablets:
  roll < 0.60 → обычный / roll < 0.90 → редкий / else → эпик

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

---

## Как это выглядит в игре

```
> идти север

  ✦ Под ногой хрустит кость. Чья-то.

══════════════════════════
  ТРОННЫЙ ЗАЛ
══════════════════════════
Огромный зал. Некромант сидит на троне.

> атаковать некромант

Начался бой с Некромант!
Ты атакуешь на 13 урона. HP Некромант: 67
Некромант бьёт тебя на 9 урона. Твой HP: 41
...
Победа! +150 XP
Некромант выронил: Зелье здоровья!
```

---

## Задания

<details>
<summary>Задание 1 — random.shuffle для случайного порядка врагов</summary>

В некоторых RPG враги атакуют в случайном порядке, если их несколько. Используй `random.shuffle(enemy_list)` чтобы перемешать список врагов в комнате перед боем.

```python
import random
enemies = room.enemies[:]   # копия списка
random.shuffle(enemies)
for enemy in enemies:
    if enemy.is_alive():
        battle(player, enemy)
```

Почему мы делаем копию `[:]` перед shuffle? Потому что shuffle изменяет список на месте — если бы мы перемешали `room.enemies`, порядок в комнате изменился бы навсегда.
</details>

---

<details>
<summary>Задание 2 — Случайные реплики врагов</summary>

Добавь в класс `Enemy` список реплик `phrases`. Во время боя, с вероятностью 30%, враг произносит случайную фразу.

```python
class Enemy:
    def __init__(self, name, hp, damage, phrases=None, ...):
        # ...
        self.phrases = phrases or []

# Создание:
goblin = Enemy(
    name="Гоблин", hp=20, damage=5,
    phrases=["Гы-гы!", "Не уйдёшь!", "Ааа!"]
)

# В battle(), в конце хода врага:
if enemy.phrases and random.random() < 0.3:
    print(f'  {enemy.name}: "{random.choice(enemy.phrases)}"')
```
</details>

---

<details>
<summary>Задание 3 — Восстанавливающее зелье</summary>

Добавь обработку предмета «Зелье здоровья» в команду «использовать»: восстанавливает 20 HP, но не больше максимума (100). После использования — удалить из инвентаря.

<details>
<summary>Подсказка</summary>

```python
elif verb == "использовать" and args:
    item = find_item(" ".join(args), player.inventory)
    if item and item.name == "Зелье здоровья":
        heal = min(20, 100 - player.hp)   # не превышаем максимум
        player.hp += heal
        player.inventory.remove(item)
        print(f"Ты выпил зелье. Восстановлено {heal} HP. Текущий HP: {player.hp}")
```
</details>
</details>

---

<details>
<summary>Задание 4 — random.seed для воспроизводимости</summary>

`random.seed(42)` фиксирует генератор случайных чисел — при одном seed последовательность всегда одинакова. Это используют в играх для воспроизводимых миров (как в Minecraft с seed мира).

Добавь в начало игры:
```python
seed = int(input("Введи seed мира (или 0 для случайного): "))
if seed != 0:
    random.seed(seed)
    print(f"Мир создан с seed {seed}. При следующем запуске с тем же seed — тот же мир!")
```

Попробуй запустить дважды с seed=42 и убедись, что события происходят в том же порядке.
</details>

---

<quiz>
q: Чем random.choice() отличается от random.randint()?
a: random.choice() выбирает случайный элемент из готового списка, а random.randint() генерирует случайное целое число в заданном диапазоне. Для выбора из вариантов — choice, для случайного числа — randint.
a: random.choice() работает только со строками, random.randint() — только с числами.
a: random.randint() быстрее, поэтому его всегда предпочтительнее использовать.
a: Они делают одно и то же, просто разный синтаксис.
correct: 0
explanation: Правильно! random.choice(["меч", "щит", "зелье"]) — берёт один элемент из списка. random.randint(1, 20) — генерирует число от 1 до 20 включительно. В таблице лута удобнее choice, для урона — randint.
</quiz>

<quiz>
q: Почему random.random() < 0.3 означает «30% вероятность»?
a: random.random() возвращает число от 0.0 до 1.0 равномерно. Примерно 30% всех чисел в этом диапазоне меньше 0.3 — значит условие выполнится в ~30% случаев.
a: Потому что 0.3 — это специальное значение в Python для вероятностей.
a: Потому что random.random() возвращает числа от 0 до 100, и 30 < 100.
a: Это просто соглашение, математически это ничего не значит.
correct: 0
explanation: Это фундаментальная математика вероятностей. Если число равномерно распределено от 0 до 1, то вероятность попасть в любой подотрезок равна его длине. Отрезок [0, 0.3] имеет длину 0.3 — значит 30%.
</quiz>

---

## Итог дня

Сегодня квест стал живым:

- `import random` — подключили стандартный модуль Python
- `random.randint(a, b)` — случайный урон с разбросом
- `random.choice(list)` — случайный выбор из списка
- `random.random()` — вероятностные события
- Таблица лута с тремя уровнями редкости
- Атмосферные случайные события при переходе между комнатами

Завтра разберём, как разбить `quest.py` на несколько файлов — как это делают настоящие проекты.

← [Week 9 — Финал](../week_9/day_7.md) | [День 2 — Модули →](day_2.md)
