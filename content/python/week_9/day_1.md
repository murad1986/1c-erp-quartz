---
type: lesson
course: "[[python_basics/README]]"
week: 9
day: 1
title: "Архитектура квеста — комнаты и игрок"
concepts: [класс Room, класс Player, игровой цикл, команды как строки]
prerequisites: "[\"[[week_8/day_7]]\"]"
tags: [python, текстовый-квест, ооп, проект]
status: draft
---

# Day 1: Архитектура квеста — комнаты и игрок

> **Сегодня:** проектируем скелет текстового квеста — два класса и первый игровой цикл
> **Время:** ~45 минут

---

Девять недель ты учился: переменные, циклы, функции, ООП, алгоритмы. Сегодня всё это складывается в одно — ты начинаешь строить собственный текстовый квест с нуля. Каждый день этой недели добавляет новый слой. К Day 6 у тебя будет полноценная играбельная игра.

Текстовые квесты — предок всех RPG. Zork, Colossal Cave Adventure — именно отсюда пошли Baldur's Gate, Dark Souls, The Witcher. Никакой графики, только слова — и при этом невероятная атмосфера. Ты поймёшь почему, когда запустишь свою первую версию.

---

## Часть 1. Аналогия: квест как граф

Вспомни курс по алгоритмам (Week 8). Граф — это вершины и рёбра между ними. Текстовый квест устроен точно так же:

- **Вершины** — комнаты (локации): тёмная пещера, замок, лес
- **Рёбра** — переходы между ними: «север», «юг», «восток», «запад»
- **Игрок** — точка на графе, которая движется по рёбрам

```
[Замок] --север--> [Башня]
   |
  юг
   |
[Деревня] --восток--> [Лес]
```

Ты всегда находишься в одной вершине. Когда вводишь «идти север» — переходишь по ребру в соседнюю вершину. Вот и весь квест. Теперь закодируем это.

---

## Часть 2. Класс Room

Каждая комната — объект. У неё есть:
- `name` — название («Тронный зал»)
- `description` — описание, которое видит игрок
- `exits` — словарь: направление → id следующей комнаты
- `items` — список предметов в комнате (пока пустой, добавим в Day 3)

```python
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}       # {"север": "forest", "юг": "village"}
        self.items = []       # список Item (добавим в Day 3)

    def add_exit(self, direction, room_id):
        self.exits[direction] = room_id

    def __str__(self):
        exits_str = ", ".join(self.exits.keys())
        return f"[{self.name}] Выходы: {exits_str}"
```

`exits` — это словарь. Ключ — строка-направление («север»), значение — строка-id комнаты («forest»). Не сама комната, а её идентификатор. Почему? Потому что комнаты хранятся в общем словаре, и мы будем искать их по id. Это стандартный приём — хранить ссылку, а не объект.

---

## Часть 3. Класс Player

Игрок — тоже объект. У него есть:
- `name` — имя
- `hp` — очки здоровья
- `inventory` — список предметов при себе
- `current_room` — текущая комната (объект Room, не id!)

```python
class Player:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp
        self.inventory = []          # список Item
        self.current_room = None     # установим при старте игры

    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return f"{self.name} (HP: {self.hp})"
```

Обрати внимание: `current_room` хранит сам объект `Room`, а не его id. Так удобнее — можно сразу обращаться к `player.current_room.name`, `player.current_room.exits` и т.д.

<!--illustration
file: day_1/day_1_classes.png
alt: Классы Room и Player как RPG-карточки персонажа
prompt:
Two RPG character-sheet panels side by side on dark background.

LEFT panel — "КЛАСС ROOM" (dungeon chamber card):
- Header: stone tablet with text "КЛАСС ROOM"
- Fields as inventory slots:
  • self.name = "Темница" (glowing teal text)
  • self.description = "Сырые стены..." (muted cream text)
  • self.exits = {"север": "corridor"} (compass rose icon, indigo)
  • self.items = [] (empty chest icon, amber)
- Method badge: add_exit(direction, room_id) — carved rune style

RIGHT panel — "КЛАСС PLAYER" (warrior character card):
- Header: stone tablet with text "КЛАСС PLAYER"
- HP bar: ████████░░ 80/100 HP (teal glow)
- Fields as stat rows:
  • self.name = "Герой"
  • self.hp = 100 (HP bar)
  • self.inventory = [] (belt pouches, empty)
  • self.current_room → arrow pointing to Room panel
- Method badge: is_alive() → True/False rune

Connecting light thread between panels: "current_room" arrow from Player to Room.
Floating dungeon spores. RPG ornamental frame.

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

---

## Часть 4. Игровой цикл и команды

Сердце любого текстового квеста — **game loop**: бесконечный цикл, который:
1. Показывает текущее состояние
2. Ждёт команду от игрока
3. Обрабатывает команду
4. Повторяет

Команды — обычные строки. Мы разбиваем ввод на слова через `split()` и смотрим на первое слово — это глагол-команда.

```python
def parse_command(command_str):
    """Разбивает строку команды на части."""
    parts = command_str.strip().lower().split()
    if not parts:
        return None, []
    verb = parts[0]          # "взять", "идти", "смотреть"
    args = parts[1:]         # ["меч"], ["север"], []
    return verb, args

def describe_room(room):
    """Описывает текущую комнату."""
    print(f"\n{'='*40}")
    print(f"  {room.name.upper()}")
    print(f"{'='*40}")
    print(room.description)
    if room.exits:
        exits_str = ", ".join(room.exits.keys())
        print(f"\nВыходы: {exits_str}")
    else:
        print("\nВыходов нет.")
```

Команды «смотреть» и «выход» — самые простые: одно слово, никаких аргументов.

<!--illustration
file: day_1/day_1_gameloop.png
alt: Игровой цикл как кольцевая квестовая цепочка
prompt:
Circular quest chain diagram showing the game loop as 4 connected stages, arranged in a clockwise cycle.

Center: glowing text "GAME LOOP" with teal ring

4 nodes connected by glowing light threads:
① "ПОКАЗАТЬ" (top) — eye icon, describes current room display
② "ЖДАТЬ" (right) — hourglass icon, input prompt "> "
③ "ОБРАБОТАТЬ" (bottom) — gear/rune icon, parse_command()
④ "ПОВТОРИТЬ" (left) — loop arrow icon

Between nodes: directional arrows with faint amber glow.
Below the cycle: three command examples as small stone tablets:
  "смотреть" → describe_room()
  "идти север" → player.current_room = rooms[next_id]
  "выход" → break ⬡

Background: dark dungeon atmosphere. Floating particles.

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

---

## Мини-демо: две комнаты, первый цикл

Собираем всё вместе. Две комнаты, переход между ними, две команды:

```python
# Создаём комнаты
dungeon = Room(
    name="Темница",
    description="Сырое подземелье. Пахнет плесенью. На стене факел."
)
corridor = Room(
    name="Коридор",
    description="Длинный коридор с каменными стенами. Где-то капает вода."
)

# Соединяем выходами
dungeon.add_exit("север", "corridor")
corridor.add_exit("юг", "dungeon")

# Словарь всех комнат
rooms = {"dungeon": dungeon, "corridor": corridor}

# Создаём игрока
player = Player(name="Герой")
player.current_room = dungeon

# Игровой цикл
print("Добро пожаловать в квест!\n")
describe_room(player.current_room)

while True:
    command_str = input("\n> ")
    verb, args = parse_command(command_str)

    if verb == "смотреть":
        describe_room(player.current_room)

    elif verb == "идти" and args:
        direction = args[0]
        exits = player.current_room.exits
        if direction in exits:
            next_id = exits[direction]
            player.current_room = rooms[next_id]
            describe_room(player.current_room)
        else:
            print(f"Туда не пройти.")

    elif verb == "выход":
        print("До свидания!")
        break

    else:
        print("Не понимаю команду. Попробуй: смотреть, идти [направление], выход")
```

Запусти этот код. Введи «смотреть», затем «идти север», потом «идти юг». Работает? Отлично — это уже квест.

---

## Задания

### Задание 1. Третья комната

Добавь третью комнату — «Тронный зал» — и соедини её с коридором выходом «север» (и обратно «юг» из Тронного зала в коридор).

<details>
<summary>Решение</summary>

```python
throne = Room(
    name="Тронный зал",
    description="Огромный зал с высокими потолками. Пустой трон покрыт пылью."
)
corridor.add_exit("север", "throne")
throne.add_exit("юг", "corridor")
rooms["throne"] = throne
```

После этого из коридора можно идти и на юг (в темницу), и на север (в тронный зал).
</details>

---

### Задание 2. Команда «статус»

Добавь команду «статус», которая выводит имя игрока и его HP.

<details>
<summary>Решение</summary>

```python
elif verb == "статус":
    print(f"Игрок: {player.name}")
    print(f"Здоровье: {player.hp} HP")
    print(f"Местонахождение: {player.current_room.name}")
```

Добавь эту ветку в игровой цикл после обработки «смотреть».
</details>

---

### Задание 3. Красивое описание выходов

Сейчас выходы выводятся просто через запятую. Измени функцию `describe_room()` так, чтобы каждый выход был на отдельной строке с символом стрелки: `→ север (Коридор)`. Для этого тебе понадобится передавать в функцию и `rooms`, чтобы получить название следующей комнаты.

<details>
<summary>Решение</summary>

```python
def describe_room(room, rooms):
    print(f"\n{'='*40}")
    print(f"  {room.name.upper()}")
    print(f"{'='*40}")
    print(room.description)
    if room.exits:
        print("\nВыходы:")
        for direction, room_id in room.exits.items():
            next_name = rooms[room_id].name
            print(f"  → {direction} ({next_name})")
    else:
        print("\nВыходов нет.")
```

Не забудь обновить все вызовы `describe_room(player.current_room)` на `describe_room(player.current_room, rooms)`.
</details>

---

### Задание 4. Защита от пустого ввода

Если игрок нажмёт Enter без текста, программа сейчас просто выводит сообщение об ошибке. Добавь проверку: если `verb` равен `None`, выводи подсказку со списком доступных команд, а не сообщение об ошибке.

<details>
<summary>Решение</summary>

```python
if verb is None:
    print("Введи команду. Доступные команды: смотреть, идти [направление], статус, выход")
    continue   # пропускаем остальные проверки, начинаем цикл заново
```

Добавь эту проверку первой в цикле, сразу после `verb, args = parse_command(command_str)`.
</details>

---

<quiz>
q: Почему в поле `exits` класса Room хранится id следующей комнаты (строка), а не сам объект Room?
a: Чтобы избежать циклических ссылок — если комната А хранит объект комнаты Б, а Б хранит объект А, Python не сможет правильно создать их. Хранение id решает проблему: все комнаты создаются сначала, потом соединяются через словарь `rooms`.
a: Потому что строки занимают меньше памяти, чем объекты.
a: Так принято в программировании игр — всегда хранить только идентификаторы.
a: Python не умеет хранить объекты внутри других объектов.
correct: 0
explanation: Правильно! Когда мы храним id, мы создаём все комнаты независимо, а потом связываем их через словарь rooms. Это также называется «слабая ссылка» — мы ссылаемся не напрямую на объект, а через ключ в общем хранилище. Это стандартный паттерн в играх и базах данных.
</quiz>

---

## Итог дня

Сегодня ты построил скелет квеста:

- `Room` — комната с названием, описанием, выходами и списком предметов
- `Player` — игрок с именем, HP, инвентарём и текущей комнатой
- `parse_command()` — разбивает строку на глагол и аргументы
- `describe_room()` — красиво выводит информацию о локации
- Игровой цикл с командами «смотреть», «идти», «выход»

Завтра добавим полноценную карту из 5 комнат и улучшим систему переходов.

---

← [Week 8 Practice](../week_8/day_6.md) | [Day 2 — Карта →](day_2.md)
