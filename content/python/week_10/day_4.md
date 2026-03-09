---
type: lesson
course: "python"
week: 10
day: 4
title: "День 4 — Финальная архитектура: полный квест"
concepts: [система XP и уровней, финальный босс, полная карта мира, условие победы]
prerequisites: "[\"[week_10/day_3](/python/week_10/day_3/)\"]"
tags: [python, текстовый-квест, проект, архитектура]
status: draft
---

# День 4 — Финальная архитектура: полный квест

← [День 3 — Исключения](/python/week_10/day_3/) | [День 5 — Что дальше →](/python/week_10/day_5/)

---

> **Сегодня:** собираем финальную версию квеста — система уровней, полная карта, сюжет и финальный босс
> **Время:** ~50 минут

---

Три дня мы добавляли инструменты: случайность, модули, исключения. Сегодня всё это идёт в дело. Финальная версия квеста — это не упражнение, это игра, в которую можно играть по-настоящему.

---

## Концепция 1 — Система XP и уровней

Опыт (XP) уже накапливается после боёв. Добавим уровни — прокачку, которая делает игрока сильнее:

```python
LEVEL_THRESHOLDS = [0, 100, 250, 500, 900, 1500]
# Уровень 1 = 0 XP, уровень 2 = 100 XP, и т.д.

def get_level(xp):
    """Возвращает уровень по количеству XP."""
    level = 1
    for threshold in LEVEL_THRESHOLDS:
        if xp >= threshold:
            level += 1
    return min(level, len(LEVEL_THRESHOLDS))

def check_level_up(player):
    """Проверяет повышение уровня и применяет бонусы."""
    new_level = get_level(player.xp)
    if new_level > player.level:
        player.level = new_level
        player.damage += 3         # +3 урона за уровень
        player.max_hp += 10        # +10 HP за уровень
        player.hp = player.max_hp  # полное восстановление!
        print(f"\n★ УРОВЕНЬ {player.level}! +3 урона, +10 HP. HP восстановлен.")
```

Добавляем `level` и `max_hp` в класс Player:

```python
class Player:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp
        self.max_hp = 100
        self.damage = 10
        self.xp = 0
        self.level = 1
        self.inventory = []
        self.current_room = None
        self.rooms_visited = 0
```

После каждого боя вызываем `check_level_up(player)`.

<!--illustration
file: day_4/day_4_xp.png
alt: Система XP и уровней — progression bar RPG стиля
prompt:
RPG level progression system visualization.

Horizontal progression bar spanning full width:
  Level 1 → Level 2 → Level 3 → Level 4 → Level 5 → Level 6
  Thresholds: 0 → 100 → 250 → 500 → 900 → 1500 XP
  Current position marker at ~350 XP glowing amber

Below bar: level-up bonus panel:
  Уровень 3 → 4:  ⚔ Урон +3  ❤ HP +10  ✦ HP восстановлен!

Banner: "★ УРОВЕНЬ 4! +3 урона, +10 HP" — amber/teal glow

LEVEL_THRESHOLDS code: [0, 100, 250, 500, 900, 1500] as milestone markers.

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

---

## Концепция 2 — Финальный босс

Некромант — главный враг. Он особенный: у него несколько фаз и уникальные реплики.

```python
def create_necromancer():
    """Создаёт финального босса."""
    from models import Enemy, Item
    necromancer = Enemy(
        name="Некромант",
        hp=120,
        damage=18,
        xp_reward=300,
        phrases=[
            "Ты думал, что сможешь меня одолеть?",
            "Смерть — это не конец...",
            "Мои кости не сломить!",
            "Ты пожалеешь об этом.",
        ]
    )
    necromancer.loot = [
        Item("Посох Некроманта", "Светится мрачным фиолетовым светом"),
        Item("Древний амулет", "Тёплый на ощупь. Что-то внутри пульсирует"),
    ]
    return necromancer
```

В `battle()` добавляем проверку второй фазы — когда HP упало ниже 50%:

```python
import random

def battle(player, enemy):
    print(f"\n⚔  БОЙ: {player.name} vs {enemy.name}")
    phase_2_triggered = False

    while enemy.is_alive() and player.hp > 0:
        # Проверка второй фазы босса
        if enemy.hp < enemy.max_hp * 0.5 and not phase_2_triggered:
            phase_2_triggered = True
            enemy.damage = int(enemy.damage * 1.3)
            print(f"\n💀 {enemy.name} впадает в ярость! Его урон вырос!")

        # Ход игрока
        dmg = random.randint(int(player.damage * 0.8), int(player.damage * 1.2))
        enemy.take_damage(dmg)
        print(f"Ты: -{dmg} → {enemy.name} HP: {enemy.hp}")

        if enemy.phrases and random.random() < 0.3:
            print(f'  «{random.choice(enemy.phrases)}»')

        if not enemy.is_alive():
            break

        # Ход врага
        edm = random.randint(int(enemy.damage * 0.8), int(enemy.damage * 1.2))
        player.hp -= edm
        print(f"{enemy.name}: -{edm} → Твой HP: {player.hp}")

    return player.hp > 0
```

---

## Концепция 3 — Полная карта

Финальная версия мира — 8 комнат с историей:

```python
def build_world():
    from models import Room, Item, Enemy
    import random

    # Комнаты
    entrance  = Room("Вход в катакомбы",
                     "Пахнет смертью и старым камнем. Назад дороги нет.")
    corridor  = Room("Коридор забвения",
                     "На стенах — имена тех, кто пришёл сюда до тебя.")
    vault     = Room("Сокровищница",
                     "Пусто. Кто-то был здесь раньше.")
    throne    = Room("Тронный зал",
                     "Гигантский зал. На троне — пустой балдахин.")
    dungeon   = Room("Темница",
                     "Ряды клеток. В одной — скелет с ключом на шее.")
    library   = Room("Библиотека",
                     "Тысячи книг. Большинство — на языке, которого ты не знаешь.")
    crypt     = Room("Крипта",
                     "Саркофаги выстроились в ряд. Некоторые открыты изнутри.")
    lair      = Room("Логово Некроманта",
                     "Здесь всё пульсирует мрачной магией. ОН здесь.")

    # Связи
    entrance.add_exit("север", "corridor")
    corridor.add_exit("юг",    "entrance")
    corridor.add_exit("север", "throne")
    corridor.add_exit("запад", "vault")
    corridor.add_exit("восток","dungeon")
    throne.add_exit("юг",     "corridor")
    throne.add_exit("запад",  "library")
    throne.add_exit("север",  "lair")     # заперто — нужен Древний ключ
    vault.add_exit("восток",  "corridor")
    dungeon.add_exit("запад", "corridor")
    dungeon.add_exit("север", "crypt")
    library.add_exit("восток","throne")
    crypt.add_exit("юг",      "dungeon")

    rooms = {
        "entrance": entrance, "corridor": corridor, "vault": vault,
        "throne": throne, "dungeon": dungeon,
        "library": library, "crypt": crypt, "lair": lair,
    }

    # Предметы
    ancient_key = Item("Древний ключ", "Массивный ключ с черепом на рукояти")
    health_pot  = Item("Зелье здоровья", "Восстанавливает 30 HP")
    old_sword   = Item("Старый меч", "Тупой, но лучше чем ничего")
    scroll      = Item("Свиток заклинаний", "Ты не знаешь как читать это")
    lever       = Item("Рычаг", "Вмурован в стену", can_pick_up=False)

    dungeon.items.append(ancient_key)
    vault.items.append(health_pot)
    entrance.items.append(old_sword)
    library.items.append(scroll)
    corridor.items.append(lever)

    # Враги
    from models import Enemy
    goblin  = Enemy("Гоблин",  hp=25, damage=6,  xp_reward=40,
                    phrases=["Гы-гы!", "Убью!", "Не уйдёшь!"])
    skeleton = Enemy("Скелет", hp=20, damage=5,  xp_reward=35,
                    phrases=["...", "*скрежет костей*"])
    troll   = Enemy("Тролль",  hp=60, damage=14, xp_reward=100,
                    phrases=["РРРРР!", "Маленький вкусный!"])

    corridor.enemies.append(goblin)
    crypt.enemies.append(skeleton)
    throne.enemies.append(troll)
    lair.enemies.append(create_necromancer())

    all_items = {i.name: i for i in [ancient_key, health_pot, old_sword, scroll, lever]}

    return rooms, all_items
```

---

## Задания

<details>
<summary>Задание 1 — Заперший вход в логово</summary>

Добавь блокировку выхода «север» из Тронного зала — нужен «Древний ключ» (который лежит в Темнице). Используй `LOCKED_EXITS` из exceptions.py.

Для полного ощущения: при попытке пройти без ключа — выведи описание двери:
```
🔒 Массивная дверь с черепом. Нужен Древний ключ.
```
</details>

---

<details>
<summary>Задание 2 — Условие победы</summary>

После победы над Некромантом бросай `GameWonError` из Day 3. В game loop лови его и показывай финальный экран:

```
╔══════════════════════════════════════╗
║       КАТАКОМБЫ ПОКОРЕНЫ!            ║
║                                      ║
║  Уровень: 4  XP: 875  Комнат: 7     ║
║  Убит Некромант. Ты — Истребитель    ║
║  Нежити.                             ║
╚══════════════════════════════════════╝
```
</details>

---

<details>
<summary>Задание 3 — Сохранение уровня</summary>

Добавь в `save_game()` сохранение `player.level` и `player.xp`. В `load_game()` — восстановление. Убедись, что после загрузки уровень корректен и `check_level_up()` не применяет бонусы повторно.
</details>

---

<quiz>
q: Зачем в Enemy хранить max_hp отдельно от hp?
a: hp уменьшается в бою, max_hp остаётся неизменным. Без max_hp мы не можем вычислить 50% от начального здоровья врага — нужно знать с чего начали, а не где сейчас. Это та же логика, что player.max_hp для восстановления здоровья.
a: max_hp нужен для отображения HP-бара в интерфейсе.
a: Python не позволяет уменьшать атрибут без сохранения начального значения.
a: max_hp используется только для боссов — обычным врагам он не нужен.
correct: 0
explanation: Как только ты начинаешь изменять hp в бою, ты теряешь информацию о начальном значении. max_hp — это "память" об исходном состоянии. Это стандартный паттерн в любой игре: current_hp и max_hp всегда хранятся отдельно.
</quiz>

---

## Итог дня

Квест стал настоящей игрой:

- Система XP с уровнями и бонусами при повышении
- Финальный босс с двумя фазами и репликами
- 8-комнатная карта с заблокированным входом к боссу
- Условие победы и финальный экран

Ты написал RPG с нуля. Завтра — разберём, куда двигаться дальше.

← [День 3 — Исключения](/python/week_10/day_3/) | [День 5 — Что дальше →](/python/week_10/day_5/)
