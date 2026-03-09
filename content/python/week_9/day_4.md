---
type: lesson
course: "[[python_basics/README]]"
week: 9
day: 4
title: "День 4 — Враги и бой"
concepts: [класс Enemy, функция battle, команда атаковать, лут после победы]
prerequisites: "[\"[[week_9/day_3]]\"]"
tags: [python, текстовый-квест, ооп, проект]
status: draft
---

# День 4 — Враги и бой

← [День 3 — Предметы](day_3.md) | [День 5 — Сохранение →](day_5.md)

---

Квест без врагов — это просто прогулка. Сегодня ты добавишь монстров, пошаговый бой и систему лута. После этого твоя игра станет настоящим dungeon crawler'ом.

---

## Концепция 1 — Класс Enemy

Враг — это тоже объект. У него есть имя, здоровье, урон и список предметов, которые он роняет после смерти.

```python
class Enemy:
    def __init__(self, name, hp, damage, loot=None, xp_reward=0):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.loot = loot if loot is not None else []  # список Item
        self.xp_reward = xp_reward

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
```

Создаём нескольких врагов:

```python
goblin = Enemy(
    name="Гоблин",
    hp=20,
    damage=5,
    loot=[Item("Ржавый нож", "Старый, но острый нож")],
    xp_reward=30
)

troll = Enemy(
    name="Тролль",
    hp=50,
    damage=12,
    loot=[Item("Дубина", "Массивная дубина тролля")],
    xp_reward=80
)
```

> Обрати внимание: `loot=None` в параметрах, а не `loot=[]`. Это важно — мутабельные значения по умолчанию в Python работают не так, как ожидаешь. Всегда используй `None` и потом заменяй на `[]` внутри метода.

---

## Концепция 2 — Враги в комнате

Добавим список врагов в класс `Room`. Враги появляются при создании комнаты и исчезают после победы над ними.

```python
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []
        self.enemies = []  # список Enemy

    def has_living_enemies(self):
        return any(e.is_alive() for e in self.enemies)
```

Размещаем врагов при создании карты:

```python
dungeon = Room("Подземелье", "Сырые стены, капает вода.")
dungeon.enemies.append(goblin)

cave = Room("Пещера", "Темно и пахнет серой.")
cave.enemies.append(troll)
```

---

## Концепция 3 — Функция battle()

Бой идёт по очереди: сначала атакует игрок, потом враг. Цикл продолжается, пока кто-то не умрёт.

```python
def battle(player, enemy):
    print(f"\nНачался бой с {enemy.name}!")
    print(f"Твой HP: {player.hp} | HP врага: {enemy.hp}\n")

    while enemy.is_alive() and player.hp > 0:
        # Ход игрока
        enemy.take_damage(player.damage)
        print(f"Ты атакуешь {enemy.name} на {player.damage} урона.")
        print(f"HP {enemy.name}: {enemy.hp}")

        if not enemy.is_alive():
            break

        # Ход врага
        player.hp -= enemy.damage
        print(f"{enemy.name} атакует тебя на {enemy.damage} урона.")
        print(f"Твой HP: {player.hp}\n")

    if player.hp <= 0:
        print("Ты погиб... Игра окончена.")
        return False   # поражение

    print(f"\nТы победил {enemy.name}!")
    player.xp += enemy.xp_reward
    print(f"Получено {enemy.xp_reward} XP.")
    return True        # победа
```

Обрати внимание: функция возвращает `True` (победа) или `False` (поражение). Это позволяет game loop'у решить, что делать дальше.

<!--illustration
file: day_4/day_4_battle.png
alt: Экран пошагового боя — игрок против гоблина
prompt:
Turn-based battle screen in RPG style, showing one round of combat.

TOP HALF — combat arena:
Left side: ГЕРОЙ silhouette (warrior), HP bar ████████░░ 45/50 HP (teal)
Right side: ГОБЛИН silhouette (creature), HP bar ███░░░░░░░ 10/20 HP (red/amber)

Center between them: crossed swords icon, amber glow

BOTTOM HALF — combat log panel (stone tablet):
Combat log in monospace:
  "Ты атакуешь Гоблин на 10 урона."
  "HP Гоблин: 10"
  "Гоблин атакует тебя на 5 урона."
  "Твой HP: 45"

Turn indicator:
  [ХОД ИГРОКА] → [ХОД ВРАГА] → [ПОВТОРИТЬ]
  glowing nodes in sequence

BOTTOM: function signature stone:
  battle(player, enemy) → True / False

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

---

## Концепция 4 — Команда «атаковать» и лут

После победы лут врага добавляется в комнату — игрок сам решает, подбирать его или нет.

```python
def find_enemy(room, name):
    for enemy in room.enemies:
        if enemy.name.lower() == name.lower() and enemy.is_alive():
            return enemy
    return None
```

Обрабатываем команду в game loop:

```python
elif parts[0] == "атаковать" and len(parts) > 1:
    enemy_name = " ".join(parts[1:])
    enemy = find_enemy(current_room, enemy_name)

    if enemy is None:
        print("Здесь нет такого врага.")
    else:
        won = battle(player, enemy)
        if not won:
            running = False          # game over
        else:
            # Добавляем лут в комнату
            for item in enemy.loot:
                current_room.items.append(item)
                print(f"Враг выронил: {item.name}")
```

Блокировка движения при живых врагах (необязательно, но круто):

```python
elif parts[0] == "идти" and len(parts) > 1:
    if current_room.has_living_enemies():
        print("Нельзя уйти — в комнате есть живые враги!")
    elif parts[1] in current_room.exits:
        current_room = current_room.exits[parts[1]]
    else:
        print("В этом направлении нет выхода.")
```

---

## Как это всё выглядит в игре

```
Подземелье
Сырые стены, капает вода.
Враги: Гоблин (HP: 20)
Выходы: север

> атаковать гоблин

Начался бой с Гоблин!
Твой HP: 50 | HP врага: 20

Ты атакуешь Гоблин на 10 урона.
HP Гоблин: 10
Гоблин атакует тебя на 5 урона.
Твой HP: 45

Ты атакуешь Гоблин на 10 урона.
HP Гоблин: 0

Ты победил Гоблин!
Получено 30 XP.
Враг выронил: Ржавый нож
```

---

## Задания

<details>
<summary>Задание 1 — Создай трёх разных врагов</summary>

Создай три объекта `Enemy` с разными характеристиками:

- **Скелет**: HP 15, урон 4, лут — «Кость», 20 XP
- **Орк**: HP 35, урон 8, лут — «Топор орка», 60 XP
- **Дракон**: HP 100, урон 20, лут — «Драконья чешуя» и «Огненный меч», 200 XP

Добавь Скелета и Орка в разные комнаты своей карты.

<details>
<summary>Подсказка</summary>

```python
skeleton = Enemy(
    name="Скелет",
    hp=15,
    damage=4,
    loot=[Item("Кость", "Обычная кость")],
    xp_reward=20
)
```

</details>
</details>

<details>
<summary>Задание 2 — Обнови describe_room()</summary>

Измени функцию `describe_room()` так, чтобы она показывала живых врагов в комнате.

Пример вывода:
```
Подземелье
Сырые стены, капает вода.
Враги: Гоблин (HP: 20), Скелет (HP: 15)
Предметы: Факел
Выходы: север, восток
```

<details>
<summary>Подсказка</summary>

```python
living = [e for e in room.enemies if e.is_alive()]
if living:
    names = ", ".join(f"{e.name} (HP: {e.hp})" for e in living)
    print(f"Враги: {names}")
```

</details>
</details>

<details>
<summary>Задание 3 — Добавь атрибут damage в Player</summary>

У игрока тоже должен быть урон. Добавь атрибут `self.damage = 10` в класс `Player`. Позволь игроку повышать урон при подборе определённых предметов.

Пример: если в инвентаре есть «Меч», урон = 15. Реализуй это как отдельную функцию `update_damage(player)`.

<details>
<summary>Подсказка</summary>

```python
def update_damage(player):
    base = 10
    for item in player.inventory:
        if item.name == "Меч":
            base += 5
    player.damage = base
```

Вызывай `update_damage(player)` после каждого подбора или выброса предмета.

</details>
</details>

<details>
<summary>Задание 4 — Команда «осмотреть [враг]»</summary>

Добавь команду `осмотреть [враг]`, которая выводит информацию о враге: имя, HP, урон.

Пример:
```
> осмотреть гоблин
Гоблин — коварное существо.
HP: 20 | Урон: 5
```

Реализуй через `find_enemy()` и добавь описание `description` в класс `Enemy`.

<details>
<summary>Подсказка</summary>

```python
class Enemy:
    def __init__(self, name, hp, damage, loot=None, xp_reward=0, description=""):
        # ... остальные поля ...
        self.description = description
```

В game loop:
```python
elif parts[0] == "осмотреть" and len(parts) > 1:
    enemy = find_enemy(current_room, " ".join(parts[1:]))
    if enemy:
        print(f"{enemy.name} — {enemy.description}")
        print(f"HP: {enemy.hp} | Урон: {enemy.damage}")
```

</details>
</details>

---

<quiz>
q: Почему в параметрах Enemy.__init__ написано loot=None, а не loot=[]?
a: В Python изменяемые объекты (списки, словари) как значения по умолчанию создаются один раз и разделяются между всеми вызовами функции. Если написать loot=[], все враги будут делить один и тот же список лута.
---
q: Что возвращает функция battle() и зачем?
a: True при победе игрока и False при поражении. Это позволяет game loop'у знать, продолжать игру или завершить её с сообщением «Game Over».
---
q: Зачем нам метод has_living_enemies() в классе Room?
a: Чтобы проверять, есть ли в комнате живые враги перед тем, как позволить игроку уйти. Это делает бой обязательным, а игру — более честной.
</quiz>

---

## Итог дня

Сегодня ты добавил в игру:

- Класс `Enemy` с HP, уроном, лутом и XP наградой
- Метод `has_living_enemies()` в класс `Room`
- Функцию `battle()` с пошаговым боем
- Команду `атаковать [враг]` и систему лута после победы
- Блокировку движения при живых врагах

Твой текстовый квест превратился в настоящую RPG. Завтра сделаем так, чтобы прогресс не пропадал после закрытия программы.

← [День 3 — Предметы](day_3.md) | [День 5 — Сохранение →](day_5.md)
