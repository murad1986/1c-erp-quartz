---
type: lesson
course: "[[python_basics/README]]"
week: 9
day: 2
title: "Карта мира — 5 комнат и навигация"
concepts: [функция build_world, улучшенный describe_room, ASCII-карта, команда помощь]
prerequisites: "[\"[[week_9/day_1]]\"]"
tags: [python, текстовый-квест, ооп, проект]
status: draft
---

# День 2 — Карта мира

← [День 1 — Архитектура](day_1.md) | [День 3 — Предметы →](day_3.md)

---

> **Сегодня:** строим полноценный мир из 5 комнат, выносим создание карты в отдельную функцию и добавляем ASCII-визуализацию
> **Время:** ~40 минут

---

Вчера у тебя были две комнаты. Это прототип. Сегодня делаем настоящий мир — тёмное подземелье с пятью локациями, разветвлёнными путями и ASCII-картой. Именно так делали Zork и Colossal Cave: сначала маленькая карта, потом слой за слоем.

---

## Часть 1. Функция build_world()

Прямо сейчас весь код создания комнат лежит в одной куче с игровым циклом. Это уже неудобно с двумя комнатами — с пятью станет катастрофой. Решение: вынести создание мира в отдельную функцию.

```python
def build_world():
    """Создаёт все комнаты и возвращает словарь {id: Room}."""

    # --- Создаём комнаты ---
    entrance = Room(
        name="Вход в подземелье",
        description="Массивные каменные ворота позади. Впереди — темнота и запах сырости."
    )
    corridor = Room(
        name="Длинный коридор",
        description="Узкий коридор. Факелы давно погасли. Под ногами — битый камень."
    )
    vault = Room(
        name="Сокровищница",
        description="Пыльный зал. Когда-то здесь было золото — теперь только ржавые решётки."
    )
    throne = Room(
        name="Тронный зал",
        description="Огромный зал. Пустой трон из чёрного камня смотрит на тебя."
    )
    dungeon = Room(
        name="Темница",
        description="Ряды пустых клеток. На полу — старые кандалы."
    )

    # --- Соединяем выходами ---
    entrance.add_exit("север", "corridor")

    corridor.add_exit("юг",    "entrance")
    corridor.add_exit("север", "throne")
    corridor.add_exit("запад", "vault")
    corridor.add_exit("восток","dungeon")

    throne.add_exit("юг",     "corridor")
    vault.add_exit("восток",  "corridor")
    dungeon.add_exit("запад", "corridor")

    # --- Собираем в словарь ---
    rooms = {
        "entrance": entrance,
        "corridor": corridor,
        "vault":    vault,
        "throne":   throne,
        "dungeon":  dungeon,
    }
    return rooms
```

Теперь вся карта — один вызов `rooms = build_world()`. Хочешь добавить комнату? Открываешь `build_world()`, не трогая ничего остального. Это называется **инкапсуляция** — ты уже знаешь это слово по классам.

---

## Часть 2. Улучшенный describe_room()

В Day 1 было задание — сделать выходы красивее. Вот решение, которое теперь становится стандартом нашего квеста:

```python
def describe_room(room, rooms):
    """Описывает комнату: название, текст, предметы, выходы."""
    print(f"\n{'═' * 42}")
    print(f"  {room.name.upper()}")
    print(f"{'═' * 42}")
    print(room.description)

    # Предметы (пока пустые — добавим в Day 3)
    if room.items:
        items_str = ", ".join(item.name for item in room.items)
        print(f"\nПредметы: {items_str}")

    # Выходы со стрелками и названиями комнат
    if room.exits:
        print("\nВыходы:")
        for direction, room_id in room.exits.items():
            next_name = rooms[room_id].name
            print(f"  → {direction:8} {next_name}")
    else:
        print("\nВыходов нет.")
    print()
```

Обрати внимание на `{direction:8}` — это форматирование с шириной поля 8 символов. Оно выравнивает текст по левой границе, дополняя пробелами справа. «север   » и «запад   » будут одинаковой ширины — как колонки в таблице.

Пример вывода:
```
══════════════════════════════════════════
  ДЛИННЫЙ КОРИДОР
══════════════════════════════════════════
Узкий коридор. Факелы давно погасли.

Выходы:
  → юг      Вход в подземелье
  → север   Тронный зал
  → запад   Сокровищница
  → восток  Темница
```

---

## Часть 3. ASCII-карта

Текстовые квесты часто дают игроку карту — это честно и удобно. Нарисуем простую схему мира жёстко «закодированную» в функцию. Да, это не автоматическая генерация — зато просто и понятно.

```python
def show_map(current_room_id):
    """Выводит ASCII-карту подземелья."""
    # Символы: [X] = ты здесь, [ ] = обычная комната
    markers = {
        "entrance": "ENT",
        "corridor": "COR",
        "vault":    "VLT",
        "throne":   "THR",
        "dungeon":  "DNG",
    }

    def cell(room_id):
        label = markers[room_id]
        if room_id == current_room_id:
            return f"[*{label}*]"   # текущая комната
        return f"[ {label} ]"

    print("\n--- КАРТА ПОДЗЕМЕЛЬЯ ---")
    print(f"         {cell('throne')}")
    print(f"             |")
    print(f"{cell('vault')} -- {cell('corridor')} -- {cell('dungeon')}")
    print(f"             |")
    print(f"         {cell('entrance')}")
    print("------------------------")
    print("[*XXX*] = ты здесь")
```

Вызов `show_map("corridor")` даст:
```
--- КАРТА ПОДЗЕМЕЛЬЯ ---
         [ THR ]
             |
[ VLT ] -- [*COR*] -- [ DNG ]
             |
         [ ENT ]
------------------------
[*XXX*] = ты здесь
```

<!--illustration
file: day_2/day_2_map.png
alt: Карта подземелья с пятью комнатами в стиле RPG
prompt:
Top-down dungeon map showing 5 rooms connected by corridors, RPG style.

Room nodes (stone chamber icons):
- [ENT] "Вход" — south position, entrance gate symbol, amber glow (current room marked with star)
- [COR] "Коридор" — center, crossroads symbol, neutral teal
- [VLT] "Сокровищница" — west of corridor, treasure chest symbol
- [THR] "Тронный зал" — north of corridor, crown symbol
- [DNG] "Темница" — east of corridor, chains symbol

Connecting corridors as stone passages with directional labels:
север↑ / юг↓ / запад← / восток→

In corner: legend panel with two entries:
  [★ COR] = ты здесь
  [ VLT ] = другая комната

Parchment-style overlay at center showing ASCII version:
"[ THR ]" / "[ VLT ]--[*COR*]--[ DNG ]" / "[ ENT ]"

Floating map pins, ancient cartography aesthetic.

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

---

## Часть 4. Команда «помощь»

Квест без справки — плохой UX. Добавим команду, которая выводит все доступные команды:

```python
HELP_TEXT = """
Доступные команды:
  смотреть          — осмотреть текущую комнату
  идти [направление]— перейти в другую комнату (север/юг/запад/восток)
  карта             — показать карту подземелья
  статус            — показать HP и инвентарь
  помощь            — эта подсказка
  выход             — выйти из игры
"""

# В игровом цикле:
elif verb == "помощь":
    print(HELP_TEXT)
```

`HELP_TEXT` — константа (всё заглавными буквами = константа по соглашению Python). Один раз определяем вверху файла, используем везде.

---

## Собираем всё вместе

Вот как теперь выглядит запуск игры:

```python
# Создаём мир и игрока
rooms = build_world()
player = Player(name="Странник")
player.current_room = rooms["entrance"]

print("=== ПОДЗЕМЕЛЬЕ ТЕНЕЙ ===")
print('Введи "помощь" для списка команд.\n')
describe_room(player.current_room, rooms)

while True:
    command_str = input("> ")
    verb, args = parse_command(command_str)

    if verb is None:
        print('Введи команду. "помощь" — список команд.')
    elif verb == "смотреть":
        describe_room(player.current_room, rooms)
    elif verb == "карта":
        show_map(get_room_id(player.current_room, rooms))
    elif verb == "помощь":
        print(HELP_TEXT)
    elif verb == "статус":
        print(f"Игрок: {player.name} | HP: {player.hp}")
    elif verb == "идти" and args:
        direction = args[0]
        exits = player.current_room.exits
        if direction in exits:
            player.current_room = rooms[exits[direction]]
            describe_room(player.current_room, rooms)
        else:
            print("Туда не пройти.")
    elif verb == "выход":
        print("До свидания!")
        break
    else:
        print(f'Не знаю команду "{verb}". Введи "помощь".')
```

Для команды «карта» нам нужна вспомогательная функция — найти id текущей комнаты:

```python
def get_room_id(room, rooms):
    """Возвращает id комнаты по её объекту."""
    for room_id, r in rooms.items():
        if r is room:       # is — сравниваем объекты, не значения
            return room_id
    return None
```

Обрати внимание на `is` вместо `==`. Здесь нам нужно именно сравнение объектов — «это тот же самый объект в памяти», а не «объекты с одинаковыми полями».

---

## Задания

<details>
<summary>Задание 1 — Шестая комната</summary>

Добавь в `build_world()` новую комнату «Библиотека» и соедини её с Тронным залом выходом «запад» (и обратно «восток» из Библиотеки в Тронный зал). Обнови ASCII-карту, чтобы Библиотека отображалась.

<details>
<summary>Подсказка</summary>

```python
library = Room(
    name="Библиотека",
    description="Пыльные полки. Большинство книг сгнило, но некоторые ещё целы."
)
throne.add_exit("запад", "library")
library.add_exit("восток", "throne")
rooms["library"] = library
```

В `show_map()` добавь ещё одну строку рядом с тронным залом.
</details>
</details>

---

<details>
<summary>Задание 2 — Длина описания</summary>

Измени `describe_room()` так, чтобы ширина разделительной линии `═` подстраивалась под длину названия комнаты, а не была фиксированной 42 символа.

<details>
<summary>Подсказка</summary>

```python
title = f"  {room.name.upper()}  "
line = "═" * len(title)
print(line)
print(title)
print(line)
```

</details>
</details>

---

<details>
<summary>Задание 3 — Краткая карта</summary>

Добавь в `describe_room()` отображение текущей позиции на мини-карте — одну строку в стиле:

```
Ты в: [ENT] -- [COR] (доступные выходы: север, запад, восток)
```

Это не полная карта, а «хлебные крошки» — краткий контекст о том, где ты и куда можно пойти.

</details>

---

<details>
<summary>Задание 4 — Псевдонимы команд</summary>

Игроки часто вводят «с» вместо «смотреть» или «n» вместо «север». Добавь словарь псевдонимов и применяй его при обработке ввода:

```python
ALIASES = {
    "с": "смотреть",
    "к": "карта",
    "п": "помощь",
    "n": "север",
    "s": "юг",
    "w": "запад",
    "e": "восток",
}
```

<details>
<summary>Подсказка</summary>

В `parse_command()` добавь замену псевдонима перед возвратом:

```python
verb = ALIASES.get(verb, verb)   # если псевдоним есть — заменяем, нет — оставляем
args = [ALIASES.get(a, a) for a in args]
```

Заметь: для `args` мы применяем замену к каждому аргументу — это нужно для направлений («n», «s»).
</details>
</details>

---

<quiz>
q: В функции get_room_id() используется `r is room`, а не `r == room`. Почему?
a: `is` проверяет, что это один и тот же объект в памяти, а не просто два объекта с одинаковыми полями. У нас могут быть две комнаты с одинаковым названием — `==` нашёл бы обе, `is` найдёт только ту, что мы ищем.
a: Потому что `==` работает медленнее для объектов.
a: Класс Room не поддерживает `==`.
a: `is` — это синтаксический сахар для более читаемого кода, работают они одинаково.
correct: 0
explanation: Правильно! `is` сравнивает адреса в памяти — два разных объекта никогда не будут `is`-равны, даже если все их поля совпадают. Это важный нюанс Python: `==` вызывает метод __eq__, а `is` проверяет идентичность объекта.
</quiz>

<quiz>
q: Почему HELP_TEXT — константа (имя заглавными буквами), а не обычная переменная?
a: Это соглашение Python: заглавные буквы сигнализируют другим программистам (и себе), что значение не должно меняться после определения. Python технически позволяет изменить её, но это нарушение договорённости.
a: Python запрещает изменять переменные с заглавными именами.
a: Константы работают быстрее обычных переменных.
a: Это требование синтаксиса для строковых переменных.
correct: 0
explanation: В Python нет настоящих констант — технически можно написать HELP_TEXT = "другое". Но соглашение CAPS_LOCK говорит: «я определил это один раз и больше трогать не буду». Это часть стиля кода (PEP 8), которому следуют все Python-разработчики.
</quiz>

---

## Итог дня

Сегодня ты:
- Вынес создание карты в `build_world()` — теперь добавить комнату занимает 3 строки
- Улучшил `describe_room()` с выровненными стрелками выходов
- Добавил ASCII-карту с маркером текущей позиции
- Добавил команду «помощь» и константу `HELP_TEXT`
- Разобрал разницу между `is` и `==`

Завтра добавим предметы — их можно будет поднимать, бросать и использовать.

← [День 1 — Архитектура](day_1.md) | [День 3 — Предметы →](day_3.md)
