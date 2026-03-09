---
type: lesson
course: "python"
week: 10
day: 3
title: "День 3 — Свои исключения: ошибки как часть дизайна"
concepts: [создание своих исключений, raise, иерархия исключений, обработка в game loop]
prerequisites: "[\"[week_10/day_2](/python/week_10/day_2/)\"]"
tags: [python, исключения, try-except, текстовый-квест]
status: draft
---

# День 3 — Свои исключения: ошибки как часть дизайна

← [День 2 — Модули](/python/week_10/day_2/) | [День 4 — Финальная архитектура →](/python/week_10/day_4/)

---

> **Сегодня:** создаём собственные исключения — квест начинает сообщать об ошибках понятно и по-дизайнерски
> **Время:** ~40 минут

---

В Week 6 ты познакомился с `try/except`. Тогда мы ловили чужие ошибки — `FileNotFoundError`, `ValueError`. Сегодня идём дальше: создаём **собственные** исключения. Это разница между «программа упала» и «программа сказала что именно пошло не так».

В Dark Souls нет сообщения «ERROR: player_died». Есть экран «YOU DIED» — спроектированный, намеренный, часть игры. Твой квест заслуживает того же.

---

## Концепция 1 — Зачем создавать свои исключения

Стандартные исключения (`ValueError`, `KeyError`) описывают технические ошибки. Твои исключения описывают **игровые ситуации**:

- Игрок умер → `PlayerDeadError`
- Дверь заперта → `LockedExitError`
- Инвентарь полон → `InventoryFullError`
- Предмет не найден → `ItemNotFoundError`

Это не просто красиво. Когда исключение называется `LockedExitError`, любой кто читает код сразу понимает что произошло. Это документация через код.

---

## Концепция 2 — Создаём иерархию исключений

```python
# exceptions.py

class QuestError(Exception):
    """Базовый класс для всех ошибок квеста."""
    pass


class PlayerDeadError(QuestError):
    """Игрок погиб."""
    def __init__(self, killer_name="неизвестно"):
        self.killer_name = killer_name
        super().__init__(f"Игрок погиб. Убийца: {killer_name}")


class LockedExitError(QuestError):
    """Выход заблокирован — нужен ключ."""
    def __init__(self, direction, required_item):
        self.direction = direction
        self.required_item = required_item
        super().__init__(f"Выход «{direction}» заперт. Нужен: {required_item}")


class InventoryFullError(QuestError):
    """Инвентарь заполнен."""
    def __init__(self, max_size):
        super().__init__(f"Инвентарь полон ({max_size} предметов максимум)")


class ItemNotFoundError(QuestError):
    """Предмет не найден."""
    def __init__(self, item_name, location=""):
        super().__init__(f"Предмет «{item_name}» не найден{' в ' + location if location else ''}")
```

`class PlayerDeadError(QuestError)` — наследование. Наш класс расширяет `QuestError`, который расширяет `Exception`. Это иерархия: можно поймать конкретный тип или весь `QuestError` сразу.

`super().__init__(message)` — вызываем `__init__` родительского класса (`Exception`) и передаём ему текст ошибки. `super()` — это способ обратиться к родителю в иерархии наследования. Без этого вызова Python не знал бы, что это за ошибка при выводе traceback.

<!--illustration
file: day_3/day_3_exceptions.png
alt: Иерархия исключений квеста как RPG skill tree
prompt:
Exception hierarchy shown as an RPG skill tree.

ROOT node at top — "Exception" — grey stone tablet
  ↓ glowing thread
SECOND level — "QuestError" — large teal panel, glowing border
  Label: "Базовый класс всех ошибок квеста"
  ↓ four branches spreading downward

FOUR leaf nodes:
  "PlayerDeadError" — skull icon, killer_name="Гоблин"
  "LockedExitError" — padlock icon, required_item="Ключ"
  "InventoryFullError" — full bag icon, max_size=5
  "ItemNotFoundError" — question mark icon

At bottom: "raise → try → except" flow as three connected beacons.

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

---

## Концепция 3 — raise: бросаем исключение

```python
# commands.py
from exceptions import LockedExitError, ItemNotFoundError, InventoryFullError

LOCKED_EXITS = {
    ("vault", "север"): "Ржавый ключ"
}

def try_move(player, direction, rooms):
    """Перемещает игрока или бросает исключение."""
    room_id = get_room_id(player.current_room, rooms)
    lock_key = (room_id, direction)

    if lock_key in LOCKED_EXITS:
        required = LOCKED_EXITS[lock_key]
        if not find_item(required, player.inventory):
            raise LockedExitError(direction, required)   # ← raise!

    exits = player.current_room.exits
    if direction not in exits:
        raise ItemNotFoundError(f"выход «{direction}»", "этой комнате")

    player.current_room = rooms[exits[direction]]
    player.rooms_visited += 1


def pick_up(player, item_name, room):
    """Поднимает предмет или бросает исключение."""
    item = find_item(item_name, room.items)
    if item is None:
        raise ItemNotFoundError(item_name, room.name)
    if not item.can_pick_up:
        raise QuestError(f"«{item.name}» нельзя поднять")
    if len(player.inventory) >= 5:
        raise InventoryFullError(5)
    room.items.remove(item)
    player.inventory.append(item)
    return item
```

`raise ExceptionClass(args)` — создаёт и бросает исключение. Выполнение немедленно прерывается и Python ищет ближайший `except`.

---

## Концепция 4 — Ловим исключения в game loop

Теперь game loop становится чистым: вся логика ошибок — в функциях, loop только ловит и показывает сообщения:

```python
# main.py
from exceptions import QuestError, PlayerDeadError, LockedExitError, InventoryFullError

while player.is_alive():
    verb, args = parse_command(input("> "))

    try:
        if verb == "идти" and args:
            try_move(player, args[0], rooms)
            maybe_random_event()
            describe_room(player.current_room, rooms)

        elif verb == "взять" and args:
            item = pick_up(player, " ".join(args), player.current_room)
            print(f"Ты подобрал: {item.name}.")

        elif verb == "атаковать" and args:
            won = battle(player, " ".join(args), player.current_room)
            if not won:
                raise PlayerDeadError(killer_name=" ".join(args))

    except LockedExitError as e:
        print(f"🔒 {e}")

    except InventoryFullError as e:
        print(f"🎒 {e}")

    except ItemNotFoundError as e:
        print(f"❓ {e}")

    except PlayerDeadError as e:
        print(f"\n╔══════════════════════════╗")
        print(f"║       ВЫ ПОГИБЛИ...      ║")
        print(f"║  Убийца: {e.killer_name:<14}║")
        print(f"╚══════════════════════════╝")
        break

    except QuestError as e:
        print(f"⚠ {e}")
```

Обрати внимание на порядок: сначала конкретные (`LockedExitError`), потом общий (`QuestError`). Python проверяет `except` сверху вниз и останавливается на первом совпадении.

---

## Задания

<details>
<summary>Задание 1 — GameWonError</summary>

Создай исключение `GameWonError(QuestError)` для ситуации победы над финальным боссом. Когда игрок побеждает Некроманта, бросай `raise GameWonError("Некромант")`. Лови в game loop и показывай экран победы:

```
╔══════════════════════════════╗
║     ПОДЗЕМЕЛЬЕ ПОКОРЕНО!     ║
║  Ты победил Некроманта.      ║
╚══════════════════════════════╝
```

</details>

---

<details>
<summary>Задание 2 — Логирование ошибок в файл</summary>

Добавь в game loop запись необработанных ошибок в файл `quest_errors.log`:

```python
import traceback

try:
    # game loop код
    ...
except Exception as e:
    with open("quest_errors.log", "a") as f:
        f.write(f"\n--- Ошибка ---\n")
        traceback.print_exc(file=f)
    print("Произошла неизвестная ошибка. Игра сохранена.")
    save_game(player, rooms)
    break
```

`traceback.print_exc()` записывает полный стек вызовов — это первое, что просят показать при баг-репорте.

</details>

---

<details>
<summary>Задание 3 — Цепочка исключений (raise from)</summary>

Если `save_game()` падает из-за ошибки записи файла, она бросает `OSError`. Оберни это в понятное исключение:

```python
class SaveError(QuestError):
    pass

def save_game(player, rooms):
    try:
        # ... код сохранения ...
    except OSError as original:
        raise SaveError("Не удалось сохранить игру") from original
```

`raise SaveError(...) from original` — цепочка исключений. Python запомнит оба: и твоё `SaveError`, и исходный `OSError`. При выводе traceback будут видны оба уровня.
</details>

---

<quiz>
q: Почему в except нужно располагать конкретные исключения выше, а общие (QuestError) ниже?
a: Python проверяет except блоки сверху вниз и останавливается на первом подходящем. Если поставить QuestError первым, он перехватит все дочерние ошибки (LockedExitError, InventoryFullError) — и ты никогда не доберёшься до конкретных обработчиков.
a: Это просто стилевое соглашение, на работу кода не влияет.
a: Конкретные исключения быстрее обрабатываются Python.
a: Общие исключения занимают больше памяти, поэтому их ставят позже.
correct: 0
explanation: Наследование + порядок проверки. LockedExitError IS A QuestError (дочерний класс). Если QuestError стоит первым, он поймает всё подряд — ты потеряешь информацию о том, какая именно ошибка произошла. Конкретное всегда выше общего.
</quiz>

<quiz>
q: Зачем передавать дополнительные атрибуты в исключение (например, killer_name в PlayerDeadError)?
a: Чтобы обработчик мог использовать эти данные. В except блоке мы обращаемся к e.killer_name и показываем пользователю конкретную информацию — кто убил, что требуется, где произошла ошибка. Голое сообщение менее информативно.
a: Это обязательный синтаксис при создании своих классов исключений.
a: Для ускорения обработки исключений Python использует эти атрибуты внутри.
a: Дополнительные атрибуты нужны только для логирования, на поведение программы они не влияют.
correct: 0
explanation: Исключение — это объект, как любой другой. У него могут быть любые атрибуты. Когда ты пишешь "except PlayerDeadError as e:", переменная e — это объект с доступом ко всем атрибутам. Это делает обработку ошибок выразительной и информативной.
</quiz>

---

## Итог дня

Сегодня ошибки стали частью дизайна:

- `class MyError(Exception)` — создаём своё исключение через наследование
- `raise MyError(args)` — бросаем исключение из любого места
- Иерархия: `QuestError` → `PlayerDeadError`, `LockedExitError` и т.д.
- Порядок `except`: конкретное → общее
- Атрибуты исключения дают обработчику контекст

Это не просто Python — это как все серьёзные программы сообщают об ошибках: Django, Flask, Pygame — везде своя иерархия исключений.

← [День 2 — Модули](/python/week_10/day_2/) | [День 4 — Финальная архитектура →](/python/week_10/day_4/)
