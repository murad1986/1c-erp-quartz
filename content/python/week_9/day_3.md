---
type: lesson
course: "[[python_basics/README]]"
week: 9
day: 3
title: "День 3 — Предметы: поднять, бросить, использовать"
concepts: [класс Item, команды взять/бросить/инвентарь, размещение предметов в комнатах, команда использовать]
prerequisites: "[\"[[week_9/day_2]]\"]"
tags: [python, текстовый-квест, ооп, проект]
status: draft
---

# День 3 — Предметы

← [День 2 — Карта](day_2.md) | [День 4 — Враги →](day_4.md)

---

> **Сегодня:** добавляем предметы в мир — класс Item, инвентарь игрока и команды для взаимодействия
> **Время:** ~45 минут

---

Пустые комнаты — это декорации. Настоящий квест — это когда ты находишь ключ в темнице и открываешь им запертую дверь тронного зала. Сегодня добавим систему предметов: поднять, бросить, использовать. После этого квест начнёт ощущаться живым.

---

## Концепция 1 — Класс Item

Предмет — объект с именем, описанием и флагом «можно ли поднять». Большинство предметов можно поднять, некоторые — нет (например, огромный камень или встроенный в стену рычаг).

```python
class Item:
    def __init__(self, name, description, can_pick_up=True):
        self.name = name
        self.description = description
        self.can_pick_up = can_pick_up

    def __str__(self):
        return self.name
```

`can_pick_up=True` — значение по умолчанию. Большинство предметов подбираемы. Для рычага в стене напишем `can_pick_up=False`.

Создаём несколько предметов:

```python
key       = Item("Ржавый ключ",   "Старый ключ с гербом замка")
torch     = Item("Факел",         "Горящий факел. Освещает путь")
shield    = Item("Щит",           "Деревянный щит с металлической оковкой")
lever     = Item("Рычаг",         "Вмурован в стену. Не двигается", can_pick_up=False)
```

---

## Концепция 2 — Предметы в комнатах и в инвентаре

Комната уже имеет список `items` (мы заложили его в Day 1). Размещаем предметы при создании карты:

```python
# В build_world(), после создания комнат:
vault.items.append(key)
vault.items.append(torch)
entrance.items.append(shield)
corridor.items.append(lever)
```

Игрок уже имеет `self.inventory = []`. Переброска предметов между комнатой и инвентарём — это просто `.append()` и `.remove()`:

```python
# Поднять предмет:
room.items.remove(item)
player.inventory.append(item)

# Бросить предмет:
player.inventory.remove(item)
room.items.append(item)
```

Ничего нового — те же списки, что в Week 2. Но теперь они хранят объекты, а не строки.

<!--illustration
file: day_3/day_3_inventory.png
alt: Перемещение предметов между комнатой и инвентарём
prompt:
Two-panel RPG inventory screen showing item transfer.

LEFT panel — "КОМНАТА: Сокровищница":
Ground items section with item slots:
  [🗝] Ржавый ключ
  [🔥] Факел
  [⚙] Рычаг  ← (locked slot, grey, "нельзя поднять" label)

CENTER: large animated arrow → "взять" command
Monospace code snippet floating:
  room.items.remove(item)
  player.inventory.append(item)

RIGHT panel — "ИНВЕНТАРЬ ГЕРОЯ":
Belt/pouch slots:
  [🗝] Ржавый ключ  ← (glowing teal, just picked up)
  [ ] пусто
  [ ] пусто
  [ ] пусто
  [ ] пусто

Below right panel: capacity bar "1/5 предметов"

can_pick_up=False shown as locked padlock on Рычаг slot.

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

---

## Концепция 3 — Функции поиска предметов

Нам нужно найти предмет по имени — в комнате или в инвентаре. Напишем одну универсальную функцию:

```python
def find_item(name, item_list):
    """Ищет предмет по имени (без учёта регистра). Возвращает Item или None."""
    name = name.lower()
    for item in item_list:
        if item.name.lower() == name:
            return item
    return None
```

Одна функция — два применения:
- `find_item("факел", room.items)` — ищем в комнате
- `find_item("факел", player.inventory)` — ищем в инвентаре

Это **переиспользование кода**: одна функция решает обе задачи за счёт параметра.

---

## Концепция 4 — Команды в игровом цикле

Добавляем три команды: «взять», «бросить», «инвентарь».

```python
elif verb == "взять" and args:
    item_name = " ".join(args)
    item = find_item(item_name, player.current_room.items)

    if item is None:
        print(f"Здесь нет предмета «{item_name}».")
    elif not item.can_pick_up:
        print(f"«{item.name}» нельзя поднять.")
    else:
        player.current_room.items.remove(item)
        player.inventory.append(item)
        print(f"Ты подобрал: {item.name}.")

elif verb == "бросить" and args:
    item_name = " ".join(args)
    item = find_item(item_name, player.inventory)

    if item is None:
        print(f"У тебя нет предмета «{item_name}».")
    else:
        player.inventory.remove(item)
        player.current_room.items.append(item)
        print(f"Ты бросил {item.name} на пол.")

elif verb == "инвентарь":
    if player.inventory:
        print("Инвентарь:")
        for item in player.inventory:
            print(f"  - {item.name}: {item.description}")
    else:
        print("Инвентарь пуст.")
```

Заметь: `" ".join(args)` объединяет аргументы обратно в строку — это нужно, если имя предмета состоит из нескольких слов: «взять ржавый ключ» → `args = ["ржавый", "ключ"]` → `"ржавый ключ"`.

---

## Бонус: команда «осмотреть»

Команда «осмотреть [предмет]» даёт подробное описание — сначала ищем в комнате, потом в инвентаре:

```python
elif verb == "осмотреть" and args:
    item_name = " ".join(args)
    item = find_item(item_name, player.current_room.items)
    if item is None:
        item = find_item(item_name, player.inventory)
    if item:
        print(f"{item.name}: {item.description}")
    else:
        print(f"Не вижу «{item_name}» ни здесь, ни в инвентаре.")
```

---

## Как это выглядит в игре

```
══════════════════════════════
  СОКРОВИЩНИЦА
══════════════════════════════
Пыльный зал. Когда-то здесь было золото.

Предметы: Ржавый ключ, Факел
Выходы:
  → восток  Длинный коридор

> осмотреть ржавый ключ
Ржавый ключ: Старый ключ с гербом замка

> взять ржавый ключ
Ты подобрал: Ржавый ключ.

> инвентарь
Инвентарь:
  - Ржавый ключ: Старый ключ с гербом замка

> идти восток

══════════════════════════════
  ДЛИННЫЙ КОРИДОР
══════════════════════════════
Узкий коридор. Факелы давно погасли.

Предметы: Рычаг
Выходы:
  → юг      Вход в подземелье
  ...

> взять рычаг
«Рычаг» нельзя поднять.
```

---

## Задания

<details>
<summary>Задание 1 — Наполни мир предметами</summary>

Добавь в `build_world()` минимум 5 предметов в разных комнатах. Обязательно:
- Один нельзя поднять (`can_pick_up=False`)
- Один состоит из двух слов в названии (например, «Старая карта»)

Убедись, что команда «взять старая карта» работает корректно.

</details>

---

<details>
<summary>Задание 2 — Обновлённый HELP_TEXT</summary>

Добавь в `HELP_TEXT` новые команды:
```
взять [предмет]   — поднять предмет
бросить [предмет] — выбросить предмет из инвентаря
инвентарь         — показать содержимое инвентаря
осмотреть [предмет] — подробно осмотреть предмет
```

</details>

---

<details>
<summary>Задание 3 — Ограничение инвентаря</summary>

Добавь в класс Player атрибут `max_inventory = 5`. При попытке поднять предмет, если инвентарь заполнен, выводи сообщение «Инвентарь полон! Сначала выброси что-нибудь.» и не добавляй предмет.

<details>
<summary>Подсказка</summary>

```python
if len(player.inventory) >= player.max_inventory:
    print("Инвентарь полон! Сначала выброси что-нибудь.")
else:
    player.current_room.items.remove(item)
    player.inventory.append(item)
    print(f"Ты подобрал: {item.name}.")
```

</details>
</details>

---

<details>
<summary>Задание 4 — Команда «использовать» (сложное)</summary>

Добавь команду «использовать [предмет]». Пока она должна работать только для «Факела»: если у тебя есть факел и ты находишься в комнате без описания освещения — выводи расширенное описание.

Реализуй это через добавление атрибута `use_effect` в класс Item:

```python
torch = Item(
    name="Факел",
    description="Горящий факел. Освещает путь",
    use_effect="Факел ярко вспыхивает. Тени отступают. Ты видишь тайный проход в северной стене!"
)
```

В команде «использовать»: ищи предмет в инвентаре, выводи `item.use_effect` если он есть, или «Ничего не происходит» если нет.

<details>
<summary>Подсказка для класса Item</summary>

```python
class Item:
    def __init__(self, name, description, can_pick_up=True, use_effect=None):
        self.name = name
        self.description = description
        self.can_pick_up = can_pick_up
        self.use_effect = use_effect
```

В game loop:
```python
elif verb == "использовать" and args:
    item_name = " ".join(args)
    item = find_item(item_name, player.inventory)
    if item is None:
        print(f"У тебя нет «{item_name}».")
    elif item.use_effect:
        print(item.use_effect)
    else:
        print("Ничего не происходит.")
```

</details>
</details>

---

<quiz>
q: Почему find_item() принимает item_list параметром, а не обращается напрямую к room.items или player.inventory?
a: Чтобы одна функция работала для любого списка предметов — комнаты, инвентаря, магазина, сундука. Если бы функция обращалась к room.items напрямую, пришлось бы писать отдельную функцию для инвентаря.
a: Потому что Python не позволяет обращаться к атрибутам объектов внутри функций.
a: Для ускорения поиска.
a: Это требование стиля кода PEP 8.
correct: 0
explanation: Это принцип повторного использования кода. Функция find_item() не знает и не должна знать, откуда пришёл список — она просто ищет. Чем меньше функция «знает» о контексте, тем в большем количестве мест её можно применить.
</quiz>

<quiz>
q: Почему используем " ".join(args) для сборки имени предмета?
a: Потому что split() разбивает строку по пробелам, и «взять ржавый ключ» даёт args = ["ржавый", "ключ"]. Чтобы сравнить с именем предмета "ржавый ключ", нужно собрать слова обратно через join().
a: join() работает быстрее, чем прямой доступ к args[0].
a: Потому что предметы всегда имеют двойные названия.
a: args — это кортеж, и его нельзя сравнивать со строками напрямую.
correct: 0
explanation: split() и join() — обратные операции. split() режет строку на список, join() склеивает список в строку. Эта пара очень часто встречается при парсинге команд.
</quiz>

---

## Итог дня

Сегодня ты добавил в квест:

- Класс `Item` с именем, описанием и флагом `can_pick_up`
- Размещение предметов в комнатах через `build_world()`
- Функцию `find_item()` — универсальный поиск по списку
- Команды `взять`, `бросить`, `инвентарь`, `осмотреть`
- Понял, почему функции с параметрами лучше функций, «знающих» контекст

Завтра добавим врагов и пошаговый бой.

← [День 2 — Карта](day_2.md) | [День 4 — Враги →](day_4.md)
