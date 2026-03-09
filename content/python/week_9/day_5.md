---
type: lesson
course: "[[python_basics/README]]"
week: 9
day: 5
title: "День 5 — Сохранение и загрузка"
concepts: [сохранение в JSON, загрузка из JSON, автосохранение, обработка отсутствующего файла]
prerequisites: "[\"[[week_9/day_4]]\"]"
tags: [python, текстовый-квест, ооп, проект, json]
status: draft
---

# День 5 — Сохранение и загрузка

← [День 4 — Враги](day_4.md) | [День 6 — Практика →](day_6.md)

---

> **Сегодня:** делаем сохранение прогресса — игрок может выйти и вернуться в ту же точку
> **Время:** ~40 минут

---

Ты дошёл до тронного зала, победил тролля, собрал лут — и выключил компьютер. Запускаешь игру снова... и начинаешь с нуля. Это неприемлемо. Сегодня исправим: добавим сохранение в JSON-файл и загрузку при старте.

---

## Концепция 1 — Что сохранять

Нам не нужно сохранять всё. Комнаты — статичны, они всегда одинаковые. Нужно сохранить только **состояние, которое меняется**:

- Имя и HP игрока
- Текущая комната (её id)
- Инвентарь (список предметов)
- Какие предметы остались в каких комнатах
- Какие враги живы

Упрощённый вариант (для начала): сохраняем только игрока и его позицию.

```python
import json

SAVE_FILE = "save.json"
```

---

## Концепция 2 — Сохранение (save_game)

Чтобы сохранить игрока, нужно преобразовать его объект в словарь, а словарь — в JSON-строку. Это называется **сериализация**.

```python
def save_game(player, rooms):
    """Сохраняет прогресс в файл save.json"""

    # Находим id текущей комнаты
    current_room_id = get_room_id(player.current_room, rooms)

    # Собираем инвентарь как список имён
    inventory_names = [item.name for item in player.inventory]

    # Строим словарь для сохранения
    data = {
        "player_name":    player.name,
        "player_hp":      player.hp,
        "current_room":   current_room_id,
        "inventory":      inventory_names,
    }

    # Записываем в файл
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Игра сохранена.")
```

<!--illustration
file: day_5/day_5_save.png
alt: Сохранение игры — объект превращается в JSON
prompt:
Save/load crystal mechanic shown as alchemical transformation.

LEFT side — "ОБЪЕКТ PYTHON":
Glass-morphism panel showing Player object:
  player.name = "Странник"
  player.hp = 45
  player.current_room = <Room>
  player.inventory = [Item, Item]

CENTER — glowing save crystal (Hollow Knight style benchwarp / bonfire):
Large crystal with inner light, amber/teal glow
Arrow DOWN labeled "json.dump() → сериализация"
Arrow UP labeled "json.load() ← десериализация"

RIGHT side — "ФАЙЛ save.json":
Stone tablet with glowing JSON text:
  {
    "player_name": "Странник",
    "player_hp": 45,
    "current_room": "throne",
    "inventory": ["Ржавый ключ"]
  }

BOTTOM: two-node flow:
  [FileNotFoundError] → "первый запуск → новая игра"

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

`json.dump(data, f)` — записывает словарь `data` в файл `f` в формате JSON. `ensure_ascii=False` позволяет сохранять кириллицу без экранирования. `indent=2` делает файл читаемым — с отступами.

Файл `save.json` будет выглядеть так:
```json
{
  "player_name": "Странник",
  "player_hp": 45,
  "current_room": "throne",
  "inventory": ["Ржавый ключ", "Факел"]
}
```

---

## Концепция 3 — Загрузка (load_game)

Загрузка — обратная операция: читаем JSON, восстанавливаем объекты.

```python
def load_game(rooms, all_items):
    """Загружает сохранение. Возвращает Player или None если файла нет."""

    # Проверяем, существует ли файл сохранения
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None   # файла нет — новая игра

    # Восстанавливаем игрока
    player = Player(name=data["player_name"], hp=data["player_hp"])

    # Устанавливаем текущую комнату
    room_id = data["current_room"]
    player.current_room = rooms.get(room_id, rooms["entrance"])

    # Восстанавливаем инвентарь по именам предметов
    for item_name in data["inventory"]:
        item = all_items.get(item_name)
        if item:
            player.inventory.append(item)

    print(f"Сохранение загружено. Ты в: {player.current_room.name}")
    return player
```

`try/except FileNotFoundError` — если файла нет (первый запуск), функция возвращает `None`. Это сигнал: начинаем новую игру.

`all_items` — словарь всех предметов игры по имени: `{"Факел": torch, "Ржавый ключ": key}`. Его нужно собрать в `build_world()` и вернуть вместе с комнатами.

---

## Концепция 4 — Автосохранение и старт игры

Обновляем начало программы: если сохранение есть — предлагаем загрузить.

```python
def start_game():
    """Запускает игру: загружает сейв или начинает новую."""
    rooms, all_items = build_world()

    print("=== ПОДЗЕМЕЛЬЕ ТЕНЕЙ ===\n")

    # Есть ли сохранение?
    import os
    if os.path.exists(SAVE_FILE):
        answer = input("Найдено сохранение. Загрузить? (да/нет): ").strip().lower()
        if answer == "да":
            player = load_game(rooms, all_items)
        else:
            player = Player(name=input("Имя персонажа: "))
            player.current_room = rooms["entrance"]
    else:
        player = Player(name=input("Имя персонажа: "))
        player.current_room = rooms["entrance"]

    return player, rooms
```

Добавляем в game loop команду «сохранить» и автосохранение при выходе:

```python
elif verb == "сохранить":
    save_game(player, rooms)

elif verb == "выход":
    save_game(player, rooms)    # автосохранение перед выходом
    print("До свидания!")
    break
```

---

## Обновляем build_world()

Теперь `build_world()` должна возвращать и комнаты, и словарь всех предметов:

```python
def build_world():
    # ... создаём комнаты и предметы как раньше ...

    # Собираем все предметы в словарь по имени
    all_items = {
        key.name:    key,
        torch.name:  torch,
        shield.name: shield,
        lever.name:  lever,
    }

    return rooms, all_items
```

---

## Как это работает

```
=== ПОДЗЕМЕЛЬЕ ТЕНЕЙ ===

Найдено сохранение. Загрузить? (да/нет): да
Сохранение загружено. Ты в: Тронный зал

══════════════════════════
  ТРОННЫЙ ЗАЛ
══════════════════════════
Огромный зал. Пустой трон из чёрного камня.

> инвентарь
Инвентарь:
  - Ржавый ключ: Старый ключ с гербом замка
  - Факел: Горящий факел

> выход
Игра сохранена.
До свидания!
```

---

## Задания

<details>
<summary>Задание 1 — Сохранение предметов в комнатах</summary>

Расширь `save_game()` так, чтобы сохранялись и предметы, оставшиеся в комнатах. Добавь в `data`:

```python
"rooms_items": {
    room_id: [item.name for item in room.items]
    for room_id, room in rooms.items()
}
```

В `load_game()` восстанови содержимое комнат из этого словаря.

</details>

---

<details>
<summary>Задание 2 — Сохранение врагов</summary>

Добавь в сохранение информацию о живых врагах в каждой комнате. Сохрани имя врага и его текущий HP. При загрузке — найди врага в комнате по имени и установи ему сохранённый HP.

</details>

---

<details>
<summary>Задание 3 — Несколько слотов сохранения</summary>

Измени систему так, чтобы поддерживать 3 слота сохранения: `save_1.json`, `save_2.json`, `save_3.json`. При команде «сохранить» спрашивай: «В какой слот? (1/2/3)».

<details>
<summary>Подсказка</summary>

```python
def save_game(player, rooms, slot=1):
    filename = f"save_{slot}.json"
    # остальной код тот же, используй filename вместо SAVE_FILE
```

</details>
</details>

---

<details>
<summary>Задание 4 — Защита от битого файла</summary>

Что будет, если `save.json` повреждён (например, файл обрезан)? `json.load()` выбросит `json.JSONDecodeError`. Добавь обработку этой ошибки:

```python
try:
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    return None
except ???:          # какой Exception ловить?
    print("Файл сохранения повреждён. Начинаем новую игру.")
    return None
```

Выясни, какой тип исключения бросает `json.load()` при битом JSON, и добавь правильный except.

<details>
<summary>Ответ</summary>

```python
except json.JSONDecodeError:
    print("Файл сохранения повреждён. Начинаем новую игру.")
    return None
```

`json.JSONDecodeError` — это подкласс `ValueError`. Перехватывая его конкретно, мы не скрываем другие возможные ошибки.
</details>
</details>

---

<quiz>
q: Почему save_game() сохраняет инвентарь как список имён предметов, а не как список объектов Item напрямую?
a: JSON умеет сохранять только базовые типы: строки, числа, списки, словари. Объект Python — это не JSON. Чтобы сохранить объект, нужно преобразовать его в словарь вручную.
a: Объекты Item слишком большие для файла.
a: Python запрещает сохранять объекты в файлы.
a: Это требование формата JSON — только строки.
correct: 0
explanation: Это ключевое ограничение JSON: он работает только с примитивными типами. Преобразование объекта в словарь называется сериализацией, обратное — десериализацией. Это фундаментальная задача при сохранении любых данных.
</quiz>

<quiz>
q: Зачем в load_game() используется rooms.get(room_id, rooms["entrance"]) вместо просто rooms[room_id]?
a: rooms.get(key, default) возвращает default если ключ не найден, вместо KeyError. Если в файле сохранения оказался несуществующий id комнаты — игра не упадёт, а вернёт игрока ко входу.
a: get() работает быстрее, чем прямой доступ по ключу.
a: Это требование при работе с JSON.
a: rooms[] не работает со строковыми ключами.
correct: 0
explanation: Защитное программирование: мы не доверяем данным из файла на 100%. Файл могли отредактировать вручную, он мог быть записан в старой версии игры. rooms.get() с fallback-значением — простой способ избежать краша.
</quiz>

---

## Итог дня

Сегодня квест получил память:

- `save_game()` — сериализует состояние в JSON-файл
- `load_game()` — десериализует обратно в объекты
- `try/except FileNotFoundError` — обработка первого запуска
- Автосохранение при команде «выход»
- Старт игры с предложением загрузить сейв

Завтра — день практики. Ты собираешь весь квест целиком и добавляешь собственные идеи.

← [День 4 — Враги](day_4.md) | [День 6 — Практика →](day_6.md)
