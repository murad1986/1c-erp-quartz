---
type: lesson
course: "python"
week: 10
day: 2
title: "День 2 — Модули: один файл стал проектом"
concepts: [разбивка на модули, import своего файла, структура проекта, from import]
prerequisites: "[\"[week_10/day_1](/python/week_10/day_1/)\"]"
tags: [python, модули, структура-проекта, текстовый-квест]
status: draft
---

# День 2 — Модули: один файл стал проектом

← [День 1 — random](/python/week_10/day_1/) | [День 3 — Исключения →](/python/week_10/day_3/)

---

> **Сегодня:** разбиваем `quest.py` на несколько файлов — учимся строить настоящие проекты
> **Время:** ~45 минут

---

К этому моменту `quest.py` — уже несколько сотен строк. Попробуй найти в нём функцию `battle()`. Придётся скроллить. А что если над квестом работают двое? Оба редактируют один файл — конфликты гарантированы.

Настоящие проекты так не устроены. Stardew Valley — 400 000 строк кода, разбитых на сотни файлов. Django (популярный Python-фреймворк) — 250 файлов. Твой квест готов к тому же шагу.

---

## Концепция 1 — Модуль — это просто файл

Любой `.py` файл — это модуль. Когда ты пишешь `import random`, Python находит файл `random.py` в стандартной библиотеке и загружает его. Точно так же можно импортировать свои файлы.

<!--illustration
file: day_2/day_2_modules.png
alt: Структура проекта из 5 модулей как карта здания
prompt:
Project structure visualization as an RPG dungeon floor map / blueprint.

Five rooms connected by glowing import arrows:

Center room — "main.py" (large, lit by amber torch):
  Labels: parse_command(), game loop, HELP_TEXT

Four rooms around it connected by light threads:
  TOP LEFT — "models.py": Room, Player, Item, Enemy
  TOP RIGHT — "world.py": build_world()
  BOTTOM LEFT — "commands.py": describe_room(), battle(), find_item()
  BOTTOM RIGHT — "save.py": save_game(), load_game()

Connecting arrows labeled:
  "from models import Player, Room" (indigo arrow)
  "from world import build_world" (teal arrow)
  Blueprint grid background. Each module as a glass panel with file icon.

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

Создадим структуру проекта:

```
quest/
├── main.py        ← запускаем отсюда
├── models.py      ← классы: Room, Player, Item, Enemy
├── world.py       ← build_world()
├── commands.py    ← describe_room, battle, find_item и др.
└── save.py        ← save_game, load_game
```

Каждый файл — своя зона ответственности. `models.py` не знает о сохранении. `save.py` не знает о боях. Это называется **разделение ответственности** — один из главных принципов хорошего кода.

---

## Концепция 2 — Переносим классы в models.py

```python
# models.py

class Item:
    def __init__(self, name, description, can_pick_up=True, use_effect=None):
        self.name = name
        self.description = description
        self.can_pick_up = can_pick_up
        self.use_effect = use_effect

    def __str__(self):
        return self.name


class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []
        self.enemies = []

    def add_exit(self, direction, room_id):
        self.exits[direction] = room_id

    def has_living_enemies(self):
        return any(e.is_alive() for e in self.enemies)


class Enemy:
    def __init__(self, name, hp, damage, loot=None, xp_reward=0, phrases=None):
        self.name = name
        self.hp = hp
        self.max_hp = hp       # нужен для проверки второй фазы в бою
        self.damage = damage
        self.loot = loot if loot is not None else []
        self.xp_reward = xp_reward
        self.phrases = phrases or []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)


class Player:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp
        self.damage = 10
        self.xp = 0
        self.inventory = []
        self.current_room = None
        self.rooms_visited = 0

    def is_alive(self):
        return self.hp > 0
```

Обрати внимание: `models.py` содержит **только классы**. Никаких функций игровой логики, никаких print. Чистые данные.

---

## Концепция 3 — import своего модуля

В `main.py` импортируем классы из `models.py`:

```python
# main.py

from models import Room, Player, Item, Enemy
from world import build_world
from commands import describe_room, battle, find_item
from save import save_game, load_game
import random
```

`from models import Room, Player` — берём конкретные имена из модуля. Теперь можно писать `Player(name="Герой")` прямо, без `models.Player(...)`.

Разница между `import` и `from ... import`:

```python
import random
random.randint(1, 6)   # нужно писать random. перед каждой функцией

from random import randint, choice
randint(1, 6)          # можно писать напрямую
choice(["а", "б"])
```

Первый вариант — безопаснее: явно видно, откуда пришла функция. Второй — удобнее для часто используемых имён.

---

## Концепция 4 — world.py и commands.py

```python
# world.py
from models import Room, Item, Enemy

def build_world():
    entrance = Room("Вход", "Массивные ворота позади.")
    corridor = Room("Коридор", "Узкий каменный коридор.")
    # ... остальные комнаты ...

    entrance.add_exit("север", "corridor")
    corridor.add_exit("юг", "entrance")

    rooms = {"entrance": entrance, "corridor": corridor}
    all_items = {}
    return rooms, all_items
```

```python
# commands.py
from models import Player, Room
import random

def describe_room(room, rooms):
    print(f"\n{'═' * 42}")
    print(f"  {room.name.upper()}")
    print(f"{'═' * 42}")
    print(room.description)
    if room.exits:
        print("\nВыходы:")
        for direction, room_id in room.exits.items():
            print(f"  → {direction:8} {rooms[room_id].name}")
    print()

def find_item(name, item_list):
    name = name.lower()
    for item in item_list:
        if item.name.lower() == name:
            return item
    return None

def get_room_id(room, rooms):
    for room_id, r in rooms.items():
        if r is room:
            return room_id
    return None
```

Теперь `commands.py` знает о классах (импортирует из `models`), но не знает о сохранении — это в `save.py`.

---

## Структура main.py

```python
# main.py — только запуск и game loop
from models import Player
from world import build_world
from commands import describe_room, find_item, get_room_id, battle
from save import save_game, load_game
import random
import os

SAVE_FILE = "save.json"
HELP_TEXT = """
Команды: смотреть | карта | статус | помощь | выход
         идти [направление]
         взять / бросить / инвентарь / осмотреть [предмет]
         атаковать [враг] | сохранить
"""

def parse_command(command_str):
    parts = command_str.strip().lower().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]

def main():
    rooms, all_items = build_world()
    # ... стартовый экран, загрузка сейва ...
    player = Player(name="Герой")
    player.current_room = rooms["entrance"]

    describe_room(player.current_room, rooms)

    while player.is_alive():
        verb, args = parse_command(input("> "))
        # ... обработка команд ...

if __name__ == "__main__":
    main()
```

`if __name__ == "__main__"` — важная строка. Она означает: «запускай `main()` только если этот файл запущен напрямую, а не импортирован». Без неё, если кто-то напишет `import main`, игра запустится сама по себе.

---

## Задания

<details>
<summary>Задание 1 — Разбей свой quest.py</summary>

Создай папку `quest/` и разбей свой `quest.py` на 5 файлов:
- `models.py` — классы
- `world.py` — `build_world()`
- `commands.py` — `describe_room`, `battle`, `find_item`, `get_room_id`, `show_map`
- `save.py` — `save_game`, `load_game`
- `main.py` — константы, `parse_command`, `main()`, game loop

Запусти `python main.py` и убедись, что всё работает.
</details>

---

<details>
<summary>Задание 2 — Отдельный файл loot.py</summary>

Вынеси таблицу лута и функцию `drop_loot()` из Day 1 в отдельный файл `loot.py`. Импортируй `drop_loot` в `commands.py` и используй в `battle()`.

<details>
<summary>Подсказка</summary>

```python
# loot.py
import random
from models import Item

LOOT_TABLE = { ... }

def drop_loot(enemy):
    roll = random.random()
    if roll < 0.60:
        return random.choice(LOOT_TABLE["обычный"])
    elif roll < 0.90:
        return random.choice(LOOT_TABLE["редкий"])
    else:
        return random.choice(LOOT_TABLE["эпик"])
```

В commands.py: `from loot import drop_loot`
</details>
</details>

---

<details>
<summary>Задание 3 — __all__ в модуле</summary>

Добавь в `models.py` строку:

```python
__all__ = ["Room", "Player", "Item", "Enemy"]
```

`__all__` — список имён, которые экспортируются при `from models import *`. Это способ сказать: «вот публичный API модуля, остальное — внутренняя реализация». Попробуй `from models import *` и убедись, что все четыре класса доступны.
</details>

---

<quiz>
q: Чем "from models import Player" отличается от "import models"?
a: "from models import Player" делает имя Player доступным напрямую. "import models" требует писать models.Player при каждом обращении. Первый вариант удобнее для часто используемых имён, второй — безопаснее, так как явно указывает источник.
a: "from models import Player" быстрее выполняется.
a: "import models" загружает весь файл, "from models import Player" — только класс Player.
a: Разницы нет, это просто разный синтаксис.
correct: 0
explanation: Оба варианта загружают весь модуль целиком — Python всегда выполняет весь файл при импорте. Разница только в том, что становится доступным в текущем пространстве имён. Это важно понимать: нет выигрыша в скорости от частичного импорта.
</quiz>

<quiz>
q: Зачем нужна строка "if __name__ == '__main__'"?
a: Когда Python запускает файл напрямую, он устанавливает __name__ = "__main__". Когда файл импортируется, __name__ = имя_модуля. Проверка позволяет не запускать игру автоматически при импорте main.py из другого файла.
a: Это обязательный синтаксис для любого Python-файла с функцией main().
a: Без этой строки Python не найдёт функцию main().
a: Это способ обозначить главный файл проекта для интерпретатора.
correct: 0
explanation: Это одна из самых важных идиом Python. Каждый хороший Python-скрипт должен иметь эту проверку — она позволяет файлу быть одновременно запускаемым скриптом И импортируемым модулем, не вызывая побочных эффектов при импорте.
</quiz>

---

## Итог дня

Сегодня `quest.py` вырос в настоящий проект:

- Модуль — любой `.py` файл, который можно импортировать
- `import module` и `from module import name` — два способа импорта
- Структура: `models`, `world`, `commands`, `save`, `main`
- `if __name__ == "__main__"` — защита от нежелательного запуска при импорте
- **Разделение ответственности**: каждый файл знает только то, что ему нужно

Именно так устроены все Python-проекты — от скриптов до веб-серверов. Ты только что освоил основу профессиональной разработки.

← [День 1 — random](/python/week_10/day_1/) | [День 3 — Исключения →](/python/week_10/day_3/)
