---
type: practice
course: "[[python_basics/README]]"
week: 9
day: 6
title: "День 6 — Практика: собери квест целиком"
prerequisites: "[\"[[week_9/day_5]]\"]"
tags: [python, текстовый-квест, практика, проект]
status: draft
---

# День 6 — Практика

← [День 5 — Сохранение](day_5.md) | [День 7 — Лонгрид →](day_7.md)

---

> **Сегодня:** только практика — никаких новых концепций. Собери квест из всех частей и добавь своё.

---

За неделю ты построил все части текстового квеста:

- **Day 1** — `Room`, `Player`, игровой цикл, `parse_command()`
- **Day 2** — `build_world()`, ASCII-карта, `describe_room()` с выходами, `HELP_TEXT`
- **Day 3** — `Item`, `find_item()`, команды `взять`/`бросить`/`инвентарь`
- **Day 4** — `Enemy`, `battle()`, команда `атаковать`, лут
- **Day 5** — `save_game()`, `load_game()`, `try/except FileNotFoundError`

Сегодня — финальная сборка. Один файл `quest.py`, полноценная игра.

---

## Задание 1 — Собери весь код

Создай файл `quest.py` и перенеси туда весь код недели в правильном порядке:

1. `import json` и `import os` (в самом начале)
2. Константы (`SAVE_FILE`, `HELP_TEXT`, `ALIASES`)
3. Классы: `Item`, `Room`, `Enemy`, `Player`
4. Вспомогательные функции: `parse_command`, `find_item`, `find_enemy`, `get_room_id`
5. Игровые функции: `describe_room`, `show_map`, `battle`
6. Функции сохранения: `save_game`, `load_game`
7. `build_world()`
8. `start_game()`
9. Игровой цикл

Запусти и убедись, что все команды работают:

```
смотреть | карта | статус | помощь | выход
идти [направление]
взять / бросить / инвентарь / осмотреть [предмет]
атаковать [враг]
сохранить
```

---

## Задание 2 — Добавь свои 3 комнаты

Расширь `build_world()`: добавь минимум 3 новые локации с уникальными описаниями. Идеи:

- **Кухня** — запах гнилой еды, лежит «Тухлое мясо» (можно поднять, но зачем?)
- **Оружейная** — на стойках только сломанное оружие, висит «Арбалет без тетивы»
- **Колодец** — в центре комнаты, у края — «Верёвка»
- **Криптa** — ряды саркофагов, в одном — «Амулет»

Добавь не менее 4 предметов в новых комнатах.

---

## Задание 3 — Придумай мини-квест

Реализуй простой квест через предметы:

> Игрок находит **Ржавый ключ** в сокровищнице. С ключом в инвентаре он может войти в **Запертую камеру** (комната, которая изначально недоступна). Без ключа переход заблокирован.

Для реализации: при команде «идти [направление]», перед переходом проверяй, не заблокирован ли выход и есть ли нужный предмет в инвентаре.

```python
# Пример блокировки выхода
LOCKED_EXITS = {
    ("vault", "север"): "Ржавый ключ"   # (room_id, direction): нужный предмет
}
```

В game loop, при команде «идти»:
```python
lock_key = (get_room_id(player.current_room, rooms), direction)
if lock_key in LOCKED_EXITS:
    required_item = LOCKED_EXITS[lock_key]
    if not find_item(required_item, player.inventory):
        print(f"Дверь заперта. Нужен: {required_item}.")
        # не переходим
        ...
```

---

## Задание 4 — Добавь 2 новых врага

Создай двух новых врагов (кроме гоблина и тролля из Day 4) и размести их в разных комнатах. Для каждого:
- Уникальное имя и описание
- Сбалансированные характеристики (HP, урон)
- Уникальный лут (хотя бы один предмет)
- XP-награда

---

## Задание 5 — Финальная «комната босса»

Создай комнату «Логово Некроманта» — финальную. Условия:
- Доступна только с ключом (из задания 3)
- В комнате — один сильный враг («Некромант», HP 80, урон 15)
- После победы над Некромантом — вывести: «Поздравляем! Ты прошёл подземелье Теней!» и завершить игру

---

## Задание 6 — Красивый game over

Сейчас при смерти игрока (HP ≤ 0) игра просто останавливается. Сделай красивый экран поражения:

```
╔══════════════════════════════╗
║        ВЫ ПОГИБЛИ...         ║
║                              ║
║  Комната: Длинный коридор    ║
║  Убийца: Гоблин              ║
║  Пройдено комнат: 3          ║
╚══════════════════════════════╝
```

Для счётчика комнат добавь в `Player` атрибут `rooms_visited = 0` и увеличивай его при каждом переходе.

---

<!--illustration
file: day_6/day_6_checklist.png
alt: Квестовый лог финальной сборки — чеклист заданий
prompt:
RPG quest log / journal page showing week 9 completion checklist.

Aged parchment scroll design with stone frame.
Title at top: "КВЕСТ: ПОДЗЕМЕЛЬЕ ТЕНЕЙ" with quest marker icon.

Quest objectives list (checkboxes as rune seals):
  ☑ Day 1 — Room, Player, parse_command()  [ВЫПОЛНЕНО — green seal]
  ☑ Day 2 — build_world(), карта  [ВЫПОЛНЕНО — green seal]
  ☑ Day 3 — Item, инвентарь  [ВЫПОЛНЕНО — green seal]
  ☑ Day 4 — Enemy, battle()  [ВЫПОЛНЕНО — green seal]
  ☑ Day 5 — save_game(), load_game()  [ВЫПОЛНЕНО — green seal]
  ◻ Добавить 3 комнаты  [В ПРОЦЕССЕ — amber glow]
  ◻ Финальный босс  [В ПРОЦЕССЕ — amber glow]

BOTTOM: XP reward notification:
  "+500 XP — Архитектор Квеста"
  Progress bar: ████████░░ до следующего уровня

Floating ink droplets, candlelight atmosphere.

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

## Чеклист финального квеста

Перед тем как считать задание выполненным, проверь:

- [ ] Все команды из задания 1 работают без ошибок
- [ ] Добавлены 3+ новые комнаты с уникальными описаниями
- [ ] Есть хотя бы один запертый проход с ключом
- [ ] Есть 2+ новых врага с лутом
- [ ] Финальная комната с боссом и сообщением победы
- [ ] Сохранение/загрузка работает корректно
- [ ] При смерти — красивый экран game over

← [День 5 — Сохранение](day_5.md) | [День 7 — Лонгрид →](day_7.md)
