---
type: lesson
course: "[[python_basics/README]]"
week: 4
day: 7
title: "Лонгрид: как устроены сейвы в Minecraft, Hollow Knight и Stardew Valley"
concepts: []
prerequisites: "[\"[[week_4/day_6]]\"]"
tags: [python, файлы, json, сейвы, игры, лонгрид]
status: draft
---

# Day 7: Как игры хранят твой прогресс

> **Сегодня:** никакого нового кода. Только истории о том, как работают сейвы в реальных играх — и почему это сложнее, чем кажется.
>
> **Время:** ~60 минут чтения

---

## Введение

Ты провёл неделю, изучая работу с файлами: `open()`, `with`, JSON, `os.path`. Всё это казалось учебными упражнениями.

Но каждый раз, когда Dark Souls сохраняет твою смерть, Hollow Knight записывает открытый чарм, или Stardew Valley помнит, что ты женился на Абигейл три игровых года назад — за этим стоят те же принципы, которые ты изучал. Только в продакшне, где ошибки стоят репутации студии.

Сегодня три кейса. В каждом — реальная инженерная проблема и её решение.

---

## Кейс 1. Minecraft — формат, который менялся 15 лет

### Данные в NBT

Minecraft появился в 2009 году. Нотч придумал формат **NBT** (Named Binary Tag) — бинарный формат для хранения данных. Если открыть файл `level.dat` из папки мира, там окажется вот что (в упрощённом виде):

```
TAG_Compound: {
  "Data": {
    "version": 19133,
    "LevelName": "My World",
    "GameType": 0,
    "Player": {
      "Inventory": [
        {
          "id": "minecraft:diamond_sword",
          "Count": 1,
          "tag": {
            "Enchantments": [
              {"id": "minecraft:sharpness", "lvl": 3}
            ]
          }
        }
      ],
      "XpLevel": 42,
      "Health": 18.0
    }
  }
}
```

Если убрать технические детали — это вложенный словарь с вложенными списками. Точно то, что ты делал в Week 3 и Week 4.

В Python это выглядело бы так:

```python
import json   # ← скопируй эту строку — разберём import в Week 5

level_data = {
    "version": 19133,
    "LevelName": "My World",
    "GameType": 0,
    "Player": {
        "Inventory": [
            {
                "id": "minecraft:diamond_sword",
                "Count": 1,
                "Enchantments": [{"id": "sharpness", "lvl": 3}]
            }
        ],
        "XpLevel": 42,
        "Health": 18.0
    }
}

# Достать данные:
player_level = level_data["Player"]["XpLevel"]
first_item = level_data["Player"]["Inventory"][0]["id"]
print(player_level)   # → 42
print(first_item)     # → minecraft:diamond_sword
```

Разница между NBT и JSON минимальна: NBT — бинарный (быстрее), JSON — текстовый (читаемый). Mojang выбрала бинарный для скорости. Многие инди-игры выбирают JSON — потому что его можно открыть блокнотом и понять.

### Миграция данных — самая больная проблема

В 2012 году Minecraft вышел из беты. В 2013 году добавили новые биомы — и алгоритм генерации мира изменился. Старые миры с новым алгоритмом выдавали «шрамы» на границах чанков: резкие переходы, где биом менялся с леса на пустыню посреди горы.

В 2021 году при обновлении 1.18 «Caves & Cliffs» мир полностью изменился по вертикали: высота увеличилась с 256 до 384. Starе миры нужно было «расширить вниз». Mojang написала **конвертер миров** — программу, которая автоматически мигрировала старые данные в новый формат.

Помнишь задание про миграцию сейва в Day 4?

```python
DEFAULTS = {
    "stamina": 100,
    "achievements": [],
}

def migrate_save(data):
    for key, default_value in DEFAULTS.items():
        if key not in data:
            data[key] = default_value
    return data
```

Это именно то, что делает Mojang — только для 1,5 миллиарда Minecraft-миров.

### Файловая структура мира

Каждый мир Minecraft — это папка:

```
MyWorld/
├── level.dat          ← главный сейв (данные игрока, время, сид)
├── level.dat_old      ← резервная копия предыдущего сейва
├── session.lock       ← блокировка (мир открыт)
└── region/
    ├── r.0.0.mca      ← чанки 0-31 по x, 0-31 по z
    ├── r.-1.0.mca     ← чанки -32-(-1) по x
    └── ...
```

Видишь `level.dat_old`? Это резервная копия. Прежде чем записать новый `level.dat`, Minecraft переименовывает старый в `level.dat_old`. Если запись прервётся — старый сейв цел.

Это именно тот паттерн атомарной записи из Day 4:

```python
# Атомарная запись через временный файл
def save_game_safe(data, save_file):
    temp_file = save_file + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(temp_file, save_file)  # атомарная замена
```

Нотч придумал это не потому что хотел — а потому что у первых игроков ломались миры при крашах. Пришлось изобрести атомарную запись.

---

![Файловая структура мира Minecraft: папки, файлы, атомарная запись level.dat](day_7/day_7_minecraft_saves_structure.png)

## Кейс 2. Hollow Knight — баг с потерей сейва и как его починили

### Самый болезненный баг в истории игры

В 2017 году вышел Hollow Knight. Через несколько недель на форумах появились отзывы: «Потерял 40 часов прогресса. Сейв исчез». Это была не единичная жалоба — это была эпидемия.

Team Cherry начала расследование. Что произошло?

### Как была устроена запись сейва изначально

Упрощённо, первая версия выглядела так:

```python
# Ранняя версия (упрощённо) — ТАК ДЕЛАТЬ НЕЛЬЗЯ
def save_game(data, slot):
    filename = f"save{slot}.dat"
    with open(filename, "w") as f:
        f.write(serialize(data))   # запись в файл
```

Проблема: если компьютер завис, свет выключился или Windows решил перезагрузиться для обновления **прямо во время записи** — файл оказывался повреждён. Наполовину старые данные, наполовину новые. Или вообще пустой файл.

При следующем запуске игра видела повреждённый файл и не могла его прочитать — и создавала **новый сейв с нуля**. 40 часов прогресса пропали.

### Решение: бэкап и проверка целостности

Team Cherry выпустила патч. Новая схема:

```python
# Патч — защита от повреждения (упрощённо)
import os   # ← скопируй эту строку — разберём import в Week 5
import json

def save_game_safe(data, slot):
    main_file = f"save{slot}.dat"
    backup_file = f"save{slot}.dat.bak"
    temp_file = f"save{slot}.dat.tmp"

    # Шаг 1: пишем во временный файл
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    # Шаг 2: если основной файл есть — делаем из него бэкап
    if os.path.exists(main_file):
        os.replace(main_file, backup_file)

    # Шаг 3: временный файл становится основным
    os.replace(temp_file, main_file)

def load_game(slot):
    main_file = f"save{slot}.dat"
    backup_file = f"save{slot}.dat.bak"

    # Пробуем основной файл
    if os.path.exists(main_file):
        try:
            with open(main_file, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass  # файл повреждён — пробуем бэкап

    # Основной повреждён — используем бэкап
    if os.path.exists(backup_file):
        with open(backup_file, encoding="utf-8") as f:
            return json.load(f)

    return None  # нет ни основного, ни бэкапа
```

Эта схема устойчива к любому прерыванию:
- Краш до шага 2 → `main_file` не тронут, `temp_file` выбрасываем
- Краш между шагами 2 и 3 → `backup_file` цел, `main_file` тоже
- Краш после шага 3 → новый `main_file` записан, `backup_file` — предыдущая версия

Потерять прогресс можно только при двух последовательных крашах в момент записи. Это почти невозможно.

### Реальная структура сейва Hollow Knight

В реальности Hollow Knight хранит данные в формате `.dat` — JSON, но зашифрованный base64. Это делается чтобы усложнить читерство (изменение файла вручную).

Структура сейва (после расшифровки) выглядит примерно так:

```json
{
  "playTime": 145800,
  "mapZone": "CROSSROADS",
  "charms": [true, false, true, true, false],
  "equippedCharms": [6, 12, 25],
  "killedBigFly": true,
  "killedInfectedKnight": false,
  "geo": 1240,
  "maxHealth": 9,
  "healthBlue": 2
}
```

Список `charms` — 45 элементов, `true`/`false` для каждого чарма в игре. Список `equippedCharms` — индексы надетых чармов. Снова знакомые структуры: список булеан + список индексов.

Когда Team Cherry добавляла новые чармы в DLC — они добавляли `true`/`false` в конец списка. Старые сейвы автоматически получали `false` для новых чармов (чарм не найден). Это та же идея миграции, которую ты реализовывал.

---

![Hollow Knight схема защиты сейва: временный файл, бэкап, восстановление при краше](day_7/day_7_hollow_knight_save_recovery.png)

## Кейс 3. Stardew Valley — один разработчик написал всё, включая сейвы

### История ConcernedApe

Эрик Барон (ConcernedApe) разрабатывал Stardew Valley **в одиночку четыре с половиной года**. Всё: графика, музыка, программирование. В том числе — система сейвов.

В 2016 году игра вышла и немедленно стала хитом: миллион копий за первые два дня. Всё это время сейвы работали без единого серьёзного сбоя. Почему?

### Формат XML вместо JSON

Stardew Valley хранит данные в **XML** (eXtensible Markup Language) — ещё один текстовый формат:

```xml
<?xml version="1.0" encoding="utf-8"?>
<SaveGame xmlns:xsi="..." xmlns:xsd="...">
  <player>
    <name>Фермер</name>
    <farmName>Звёздная</farmName>
    <totalMoneyEarned>48200</totalMoneyEarned>
    <stamina>270</stamina>
    <maxStamina>270</maxStamina>
    <inventory>
      <Item xsi:type="Pickaxe">
        <name>Pickaxe</name>
        <upgradeLevel>3</upgradeLevel>
      </Item>
      <Item xsi:type="Object">
        <name>Cauliflower</name>
        <stack>12</stack>
      </Item>
    </inventory>
  </player>
  <year>3</year>
  <season>summer</season>
  <dayOfMonth>14</dayOfMonth>
</SaveGame>
```

XML и JSON — разные синтаксисы для одной идеи: иерархические данные. В Python это всё равно превратилось бы в тот же вложенный словарь.

### Файловая структура сейвов Stardew

```
Stardew Valley/Saves/
└── Звёздная_123456789/
    ├── Звёздная_123456789        ← основной сейв (XML, без расширения)
    ├── Звёздная_123456789_old    ← предыдущая версия
    ├── SaveGameInfo              ← краткая информация (имя, дата, деньги)
    └── SaveGameInfo_old          ← предыдущая краткая информация
```

Видишь паттерн? Снова `_old` суффикс — как `level.dat_old` у Minecraft. Это стандартный способ держать резервную копию: переименовать текущий файл в `_old`, записать новый.

`SaveGameInfo` — отдельный маленький файл с краткими данными. Он нужен для экрана загрузки: чтобы показать список сейвов с именами и датами, не нужно загружать весь огромный XML — достаточно прочитать маленький `SaveGameInfo`.

В Python это выглядело бы так:

```python
import os   # ← скопируй эту строку — разберём import в Week 5
import json

SAVES_DIR = "saves"

def save_game(player, farm_data):
    # Папка для этого персонажа
    save_dir = os.path.join(SAVES_DIR, f"{player['farm_name']}_{player['id']}")
    os.makedirs(save_dir, exist_ok=True)

    main_file = os.path.join(save_dir, "save")
    old_file = os.path.join(save_dir, "save_old")
    info_file = os.path.join(save_dir, "save_info")

    # Сдвигаем старый сейв в _old
    if os.path.exists(main_file):
        os.replace(main_file, old_file)

    # Пишем полный сейв
    with open(main_file, "w", encoding="utf-8") as f:
        json.dump({"player": player, "farm": farm_data}, f, ensure_ascii=False, indent=2)

    # Пишем краткую информацию (для экрана загрузки)
    summary = {
        "name": player["name"],
        "farm": player["farm_name"],
        "day": farm_data["day"],
        "season": farm_data["season"],
        "year": farm_data["year"],
        "money": player["money"]
    }
    with open(info_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False)

    print(f"Сохранено: {player['farm_name']}")
```

Обрати внимание: краткий `info_file` (только основные поля) записывается отдельно от полного сейва. Это оптимизация: при показе 5 слотов сохранений не нужно читать 5 мегабайтных файлов — только 5 маленьких `info`.

### Как ConcernedApe справился с миграцией

Когда Stardew Valley выходила крупные обновления (1.3 — мультиплеер, 1.4 — новые предметы), структура сейвов менялась. Старые сейвы нужно было читать.

ConcernedApe решил это через поле версии в каждом сейве:

```xml
<gameVersion>1.4.0</gameVersion>
```

При загрузке игра проверяет версию и применяет «миграторы»:

```python
def load_and_migrate(filename):
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    version = data.get("gameVersion", "1.0.0")

    # Применяем миграции по очереди
    if version < "1.3.0":
        data = migrate_to_1_3(data)   # добавить поля для мультиплеера
    if version < "1.4.0":
        data = migrate_to_1_4(data)   # добавить новые предметы
    if version < "1.5.0":
        data = migrate_to_1_5(data)   # добавить остров Гингер

    data["gameVersion"] = "1.5.0"    # обновить версию
    return data
```

Сейв из 2016 года открывается в версии 2024 года — и всё работает. Это и есть правильно спроектированная миграция данных.

---

![Stardew Valley файловая структура сейвов и краткий файл SaveGameInfo для экрана загрузки](day_7/day_7_stardew_save_structure.png)

## Сравнение: три подхода к одной задаче

| Игра | Формат | Резервная копия | Защита от краша |
|:-----|:-------|:----------------|:----------------|
| Minecraft | NBT (бинарный) | `level.dat_old` | `os.replace()` |
| Hollow Knight | JSON + base64 | `.dat.bak` | Временный файл → replace |
| Stardew Valley | XML | `save_old` | Rename old → write new |

Разные технологии, разные языки, разные студии — но **одна инженерная идея**: не перезаписывать файл напрямую. Всегда держи резервную копию.

Это не теория. Это стандарт индустрии.

---

## Что ещё происходит «за кулисами»

### Автосохранение — сложнее, чем кажется

В Dark Souls автосохранение происходит почти мгновенно — после каждого действия. Как FromSoftware умудряется не тормозить игру при каждом сохранении?

Ответ: **асинхронная запись**. Основной игровой поток продолжает работать. Параллельно — отдельный поток записывает данные в файл. Игрок этого не замечает.

В Python это реализовано через `threading` или `asyncio` — инструменты, которые ты изучишь позже. Но принцип прост: «запусти запись в файл, не жди пока она закончится, продолжай игру».

### Cloud saves — ещё один уровень сложности

Steam Cloud автоматически синхронизирует сейвы между компьютерами. Это добавляет новую проблему: конфликт версий.

Ты сыграл час на ноутбуке. Потом открыл игру на ПК без интернета — и продолжил. Теперь оба компьютера думают, что у них «последний» сейв. Чей правильный?

Steam решает через метки времени (`timestamp` в сейве) и иногда спрашивает пользователя. Это точно та же проблема, которую решают системы контроля версий (Git). Конфликт данных — фундаментальная проблема информатики.

### Читерство и защита сейвов

Hollow Knight зашифровал сейвы не случайно. Если сейв — читаемый JSON, любой игрок может открыть его блокнотом и написать `"geo": 9999999`. Некоторые игры на это не реагируют (Stardew Valley, Minecraft — читы разрешены). Другие это предотвращают.

Один способ — хранить хэш данных:

```python
import json

def save_with_checksum(data, filename):
    content = json.dumps(data, ensure_ascii=False, sort_keys=True)
    checksum = hash(content)   # упрощённо
    save_data = {"data": data, "checksum": checksum}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(save_data, f)

def load_with_checksum(filename):
    with open(filename, encoding="utf-8") as f:
        save_data = json.load(f)
    content = json.dumps(save_data["data"], ensure_ascii=False, sort_keys=True)
    expected = hash(content)
    if expected != save_data["checksum"]:
        print("Сейв изменён вручную!")
        return None
    return save_data["data"]
```

Если изменить данные в файле, хэш не совпадёт — игра обнаружит читерство. Реальные системы используют более сложные криптографические хэши (SHA-256), но принцип тот же.

---

## Что это всё значит для тебя

За три кейса ты видел:

1. **Minecraft** — NBT как JSON, `_old` паттерн, миграция данных для 1,5 миллиарда миров
2. **Hollow Knight** — баг потери сейвов из-за отсутствия атомарной записи, трёхфайловая защита
3. **Stardew Valley** — разделение полного сейва и краткого, версионирование для миграции

Всё это — те же принципы, которые ты изучал всю неделю:
- `open()` с `with` и правильным режимом
- JSON как универсальный формат
- `os.path.join()` для путей
- `os.makedirs()` для создания папок
- `os.replace()` для атомарной записи
- Паттерн save/load с проверкой существования файла

Единственная разница между твоим менеджером персонажей из Day 6 и системой сейвов Hollow Knight — количество продуманных крайних случаев и масштаб. Архитектура та же.

---

## Факт-бомба

В 2014 году из-за бага в системе сейвов Dark Souls II игроки на PC потеряли свои персонажи после серверного обновления. FromSoftware пришлось вручную восстанавливать данные игроков с серверных бэкапов.

Оказалось, что в коде синхронизации сейвов не было проверки: сервер просто перезаписывал локальный файл облачной копией — даже если облачная копия была старее. Из-за сбоя в облаке сотни игроков получили откат на несколько часов.

С тех пор у FromSoftware всегда сравниваются временные метки перед любой синхронизацией.

Одна проверка `if local_timestamp > cloud_timestamp:` могла предотвратить весь инцидент.

---

← [Day 6 — Практика](day_6.md) | [Week 5, Day 1 — Функции →](../week_5/day_1.md)
