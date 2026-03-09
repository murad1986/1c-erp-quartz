---
type: lesson
course: "[[python_basics/README]]"
week: 8
day: 3
title: "Сортировка — пузырёк, выбор, встроенная"
concepts: [пузырьковая сортировка O(n²), сортировка выбором O(n²), sorted() O(n log n), ключ сортировки]
prerequisites: "[\"[[week_8/day_2]]\"]"
tags: [python, алгоритмы, сортировка, bubble sort, selection sort, sorted]
status: draft
---

# Day 3: Сортировка — пузырёк, выбор, встроенная

> **Сегодня:** разберём, как устроена сортировка изнутри, напишем два классических алгоритма своими руками — и убедимся, что встроенный `sorted()` побеждает их вчистую.
> **Время:** ~40 минут

---

## Часть 1 — Зачем вообще сортировать?

Вчера мы узнали: бинарный поиск работает только на **отсортированном** списке. Но это не единственная причина.

**Реальные задачи, где нужна сортировка:**
- Топ-10 игроков по очкам на доске почёта
- Инвентарь, отсортированный по редкости предметов
- Плейлист Spotify, отсортированный по количеству прослушиваний
- Лента TikTok — видео по релевантности (внутри — сложная сортировка)

Сортировка — одна из самых фундаментальных задач в программировании. И способов решить её — десятки. Сегодня разберём три.

---

## Часть 2 — Пузырьковая сортировка: тяжёлые всплывают вверх

**Идея:** проходим по списку и сравниваем соседние элементы. Если левый больше правого — меняем их местами. После каждого прохода самый большой элемент «всплывает» в конец. Повторяем, пока список не будет отсортирован.

Аналогия: представь, что числа — это пузыри разного размера в стакане. Большие пузыри всегда поднимаются вверх.

```python
def bubble_sort(lst):
    arr = lst.copy()        # не трогаем оригинал
    n = len(arr)
    total_swaps = 0

    for i in range(n):                     # n проходов
        for j in range(0, n - i - 1):     # каждый раз на 1 короче
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # swap
                total_swaps += 1

    print(f"Перестановок: {total_swaps}")
    return arr

hp_list = [450, 120, 890, 230, 670, 55, 340]
sorted_hp = bubble_sort(hp_list)
print(sorted_hp)
# → Перестановок: 11
# → [55, 120, 230, 340, 450, 670, 890]
```

**Сложность:** O(n²) — два вложенных цикла. На 1000 элементах — до 500 000 операций.

<!--illustration
file: day_3/day_3_bubble_sort_steps.png
alt: Шаги пузырьковой сортировки [5,3,8,1,4] — первые три прохода с обменами
prompt:
Create a Dark RPG UI infographic showing bubble sort steps on [5, 3, 8, 1, 4].

Title: "ПУЗЫРЬКОВАЯ СОРТИРОВКА" in cream (#e8e0d4). Subtitle: "[5, 3, 8, 1, 4] — смотрим первые 3 прохода" in gray-blue.

Three horizontal rows, each showing one pass:

PASS 1 (label "Проход 1"):
[5][3][8][1][4] → compare 5,3: swap → [3][5][8][1][4] → compare 5,8: ok → compare 8,1: swap → [3][5][1][8][4] → compare 8,4: swap → [3][5][1][4][8]
The "8" element glows amber — it "bubbled up" to the end. Upward bubble arrow on the 8.
Swapped pairs connected with curved amber arrows showing the swap.

PASS 2 (label "Проход 2"):
[3][5][1][4][8] → compare 5,1: swap → [3][1][5][4][8] → compare 5,4: swap → [3][1][4][5][8]
The last slot (8) is dimmed — already in place.

PASS 3 (label "Проход 3"):
[3][1][4][5][8] → compare 3,1: swap → [1][3][4][5][8]
Last two slots dimmed. Elements settling into place.

Bottom: "Перестановок: 11 | Сложность: O(n²)"

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette is MUTED and atmospheric, like cave crystals and bioluminescent fungi:
  - Teal #4db8c7 for primary elements (soft crystal light, NOT bright cyan)
  - Indigo #8b6cc1 for secondary elements (like glowing fungi)
  - Amber #d4854a for accents and highlights (like distant torchlight)
  - Cream #e8e0d4 for text (warm parchment white)
  - Green #7bc88f only for positive/success states
- ALL glows are SOFT and DIFFUSED: blur radius 10-15px, opacity 20-35%. Like bioluminescence in a dark cave. NEVER sharp neon edges. NEVER bright cyan #00ffff or bright purple #ff00ff.
- RPG ornamental frame: thin border 1px rgba(77,184,199,0.12), weathered stone corner ornaments (aged, slightly eroded, NOT polished).
- Nodes/orbs: dark glass rgba(10,14,26,0.85) with thin colored border. Icons inside as white silhouettes at 50% opacity.
- Connecting lines: organic curves (like roots/vines/light threads), NOT straight mechanical wires. 1-1.5px, soft glow.
- Glass-morphism panels for info cards: semi-transparent dark with subtle blur and soft shadow.
- Floating spore particles (1-3px dots) scattered across image — like Hollow Knight spores.
- Monospace font for all code text. Code colored: teal for keywords, amber for values, indigo for strings.
- Slight grain/noise texture on background surfaces.
- Russian (Cyrillic) text for all titles, labels, annotations.
- Three tiny color swatches (6x6px) at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight's City of Tears — contemplative, beautiful, mysterious. NOT aggressive, NOT cyberpunk.
-->

---

## Часть 3 — Сортировка выбором: ищем минимум, ставим на место

**Идея:** делим список на две части — отсортированную (слева) и неотсортированную (справа). На каждом шаге находим **минимальный** элемент в неотсортированной части и ставим его в конец отсортированной.

Аналогия: раскладываешь карточки врагов по убыванию HP. Каждый раз берёшь самого слабого из оставшихся и кладёшь следующим.

```python
def selection_sort(lst):
    arr = lst.copy()
    n = len(arr)
    total_ops = 0

    for i in range(n):
        min_idx = i                        # предполагаем: минимум — первый
        for j in range(i + 1, n):         # ищем настоящий минимум
            total_ops += 1
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]  # ставим минимум на место

    print(f"Сравнений: {total_ops}")
    return arr

damage_list = [85, 32, 140, 67, 210, 15, 95]
sorted_dmg = selection_sort(damage_list)
print(sorted_dmg)
# → Сравнений: 21
# → [15, 32, 67, 85, 95, 140, 210]
```

**Сложность:** O(n²) — тоже два вложенных цикла. Количество **сравнений** одинаково всегда, зато **перестановок** меньше, чем у пузырька.

---

## Часть 4 — Реальное сравнение на 1000 элементов

```python
import time
import random

data = [random.randint(1, 10000) for _ in range(1000)]

# Bubble sort
start = time.time()
bubble_sort(data)
bubble_time = time.time() - start

# Selection sort
start = time.time()
selection_sort(data)
selection_time = time.time() - start

# Встроенный sorted()
start = time.time()
sorted(data)
builtin_time = time.time() - start

print(f"Пузырёк:        {bubble_time:.4f} сек")    # → ~0.1200 сек
print(f"Выбор:          {selection_time:.4f} сек")  # → ~0.0600 сек
print(f"sorted():       {builtin_time:.6f} сек")    # → ~0.000089 сек
print(f"sorted() быстрее пузырька в {bubble_time/builtin_time:.0f}x раз!")
```

Почему `sorted()` так быстро? Потому что Python использует **Timsort** — гибридный алгоритм сортировки со сложностью O(n log n). На 1000 элементов это ~10 000 операций против ~1 000 000 у пузырька.

<!--illustration
file: day_3/day_3_sort_complexity_arena.png
alt: Арена трёх алгоритмов сортировки — пузырёк, выбор и sorted() на 1000 элементах
prompt:
Create a Dark RPG UI infographic comparing three sorting algorithms as an RPG arena battle.

Title: "АРЕНА СОРТИРОВОК: 1000 ЭЛЕМЕНТОВ" in cream (#e8e0d4).

Three fighter panels side by side, styled as RPG character cards:

FIGHTER 1 (dim amber): "Пузырьковая O(n²)"
- Worn-looking card, slightly cracked
- Operations badge: "~500 000 операций"
- Time badge: "~0.1200 сек"
- Icon: slow bubble

FIGHTER 2 (dim indigo): "Сортировка выбором O(n²)"
- Similar worn card
- Operations badge: "~500 000 операций"
- Time badge: "~0.0600 сек"
- Icon: selection cursor

FIGHTER 3 (bright teal, glowing): "sorted() — Timsort O(n log n)"
- Clean, glowing card with a golden crown icon
- Operations badge: "~10 000 операций"
- Time badge: "~0.000089 сек"
- Icon: lightning bolt
- "ПОБЕДИТЕЛЬ" label in green (#7bc88f) with glow

Below: a glass banner: "sorted() быстрее пузырька в ~1000x раз!"

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette is MUTED and atmospheric, like cave crystals and bioluminescent fungi:
  - Teal #4db8c7 for primary elements (soft crystal light, NOT bright cyan)
  - Indigo #8b6cc1 for secondary elements (like glowing fungi)
  - Amber #d4854a for accents and highlights (like distant torchlight)
  - Cream #e8e0d4 for text (warm parchment white)
  - Green #7bc88f only for positive/success states
- ALL glows are SOFT and DIFFUSED: blur radius 10-15px, opacity 20-35%. Like bioluminescence in a dark cave. NEVER sharp neon edges. NEVER bright cyan #00ffff or bright purple #ff00ff.
- RPG ornamental frame: thin border 1px rgba(77,184,199,0.12), weathered stone corner ornaments (aged, slightly eroded, NOT polished).
- Nodes/orbs: dark glass rgba(10,14,26,0.85) with thin colored border. Icons inside as white silhouettes at 50% opacity.
- Connecting lines: organic curves (like roots/vines/light threads), NOT straight mechanical wires. 1-1.5px, soft glow.
- Glass-morphism panels for info cards: semi-transparent dark with subtle blur and soft shadow.
- Floating spore particles (1-3px dots) scattered across image — like Hollow Knight spores.
- Monospace font for all code text. Code colored: teal for keywords, amber for values, indigo for strings.
- Slight grain/noise texture on background surfaces.
- Russian (Cyrillic) text for all titles, labels, annotations.
- Three tiny color swatches (6x6px) at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight's City of Tears — contemplative, beautiful, mysterious. NOT aggressive, NOT cyberpunk.
-->

---

## Часть 5 — `sorted()` с ключом: сортируем что угодно

`sorted()` умеет сортировать сложные объекты — если объяснить ему, **по какому полю** сортировать. Для этого используется параметр `key=`. Сюда передаётся функция (можно `lambda`!).

```python
enemies = [
    {"name": "Hollow Soldier", "hp": 150, "level": 3},
    {"name": "Black Knight",   "hp": 680, "level": 15},
    {"name": "Silver Knight",  "hp": 420, "level": 10},
    {"name": "Undead Archer",  "hp": 95,  "level": 2},
    {"name": "Gargoyle",       "hp": 560, "level": 12},
]

# Сортировка по HP (от меньшего к большему)
by_hp = sorted(enemies, key=lambda e: e["hp"])
for e in by_hp:
    print(f"{e['name']}: {e['hp']} HP")
# → Undead Archer: 95 HP
# → Hollow Soldier: 150 HP
# → Silver Knight: 420 HP
# → Gargoyle: 560 HP
# → Black Knight: 680 HP

# Сортировка по уровню, по убыванию
by_level_desc = sorted(enemies, key=lambda e: e["level"], reverse=True)
print(by_level_desc[0]["name"])  # → Black Knight (самый высокоуровневый)
```

Можно сортировать по нескольким полям сразу — через кортеж в `key=`:

```python
# Сначала по уровню, при равных уровнях — по имени
by_level_then_name = sorted(
    enemies,
    key=lambda e: (e["level"], e["name"])
)
```

<!--illustration
file: day_3/day_3_sorted_key_lambda.png
alt: sorted() с key=lambda сортирует список врагов по HP — до и после
prompt:
Create a Dark RPG UI infographic showing sorted() with key=lambda transforming an enemy list by HP.

Title: "sorted() С КЛЮЧОМ — СОРТИРУЕМ ЧТО УГОДНО" in cream (#e8e0d4).

Left side: unsorted enemy list — 5 RPG enemy cards in random order:
- "Hollow Soldier" HP: 150
- "Black Knight" HP: 680
- "Silver Knight" HP: 420
- "Undead Archer" HP: 95
- "Gargoyle" HP: 560

Each card is a dark glass panel with enemy name (cream) and HP bar (colored by HP value).

Center: a large arrow pointing right, labeled:
sorted(enemies, key=lambda e: e["hp"])
in teal monospace, with "lambda e: e['hp']" in amber highlight.

Right side: sorted enemy cards in ascending HP order:
1. Undead Archer: 95 HP
2. Hollow Soldier: 150 HP
3. Silver Knight: 420 HP
4. Gargoyle: 560 HP
5. Black Knight: 680 HP

HP bars now form a neat ascending staircase. Numbers 1-5 in teal above each card.

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette is MUTED and atmospheric, like cave crystals and bioluminescent fungi:
  - Teal #4db8c7 for primary elements (soft crystal light, NOT bright cyan)
  - Indigo #8b6cc1 for secondary elements (like glowing fungi)
  - Amber #d4854a for accents and highlights (like distant torchlight)
  - Cream #e8e0d4 for text (warm parchment white)
  - Green #7bc88f only for positive/success states
- ALL glows are SOFT and DIFFUSED: blur radius 10-15px, opacity 20-35%. Like bioluminescence in a dark cave. NEVER sharp neon edges. NEVER bright cyan #00ffff or bright purple #ff00ff.
- RPG ornamental frame: thin border 1px rgba(77,184,199,0.12), weathered stone corner ornaments (aged, slightly eroded, NOT polished).
- Nodes/orbs: dark glass rgba(10,14,26,0.85) with thin colored border. Icons inside as white silhouettes at 50% opacity.
- Connecting lines: organic curves (like roots/vines/light threads), NOT straight mechanical wires. 1-1.5px, soft glow.
- Glass-morphism panels for info cards: semi-transparent dark with subtle blur and soft shadow.
- Floating spore particles (1-3px dots) scattered across image — like Hollow Knight spores.
- Monospace font for all code text. Code colored: teal for keywords, amber for values, indigo for strings.
- Slight grain/noise texture on background surfaces.
- Russian (Cyrillic) text for all titles, labels, annotations.
- Three tiny color swatches (6x6px) at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight's City of Tears — contemplative, beautiful, mysterious. NOT aggressive, NOT cyberpunk.
-->

---

## Задание 1 — Пузырёк с оптимизацией (7 мин)

Классический пузырьковый алгоритм продолжает делать проходы, даже если список уже отсортирован. Добавь оптимизацию: если за весь проход не было ни одной перестановки — значит список уже отсортирован, и можно выходить досрочно.

Проверь: на уже отсортированном списке оптимизированная версия должна сделать всего 1 проход.

<details>
<summary>Решение</summary>

```python
def bubble_sort_optimized(lst):
    arr = lst.copy()
    n = len(arr)
    passes = 0

    for i in range(n):
        passes += 1
        swapped = False                    # флаг: была ли перестановка

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:                    # ни одной перестановки — готово!
            print(f"Готово досрочно за {passes} проход(ов)")
            break

    return arr

# Уже отсортированный список
already_sorted = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
bubble_sort_optimized(already_sorted)
# → Готово досрочно за 1 проход(ов)

# Случайный список
mixed = [5, 3, 8, 1, 9, 2, 7]
result = bubble_sort_optimized(mixed)
print(result)   # → [1, 2, 3, 5, 7, 8, 9]
```

</details>

---

## Задание 2 — Сортировка выбором с визуализацией (8 мин)

Напиши функцию `selection_sort_visual(lst)`, которая на каждом шаге выводит текущее состояние списка. Минимальный элемент, который выбирается, обозначай символом `*` (просто выводи его отдельно).

```
Шаг 1: минимум=15 → [15, 85, 32, 140, 67, 210, 95]
Шаг 2: минимум=32 → [15, 32, 85, 140, 67, 210, 95]
...
```

<details>
<summary>Решение</summary>

```python
def selection_sort_visual(lst):
    arr = lst.copy()
    n = len(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        print(f"Шаг {i + 1}: минимум={arr[i]} → {arr}")

    print(f"\nГотово: {arr}")
    return arr

damage_list = [85, 15, 140, 32, 210, 67]
selection_sort_visual(damage_list)
# → Шаг 1: минимум=15 → [15, 85, 140, 32, 210, 67]
# → Шаг 2: минимум=32 → [15, 32, 140, 85, 210, 67]
# → Шаг 3: минимум=67 → [15, 32, 67, 85, 210, 140]
# → Шаг 4: минимум=85 → [15, 32, 67, 85, 210, 140]
# → Шаг 5: минимум=140 → [15, 32, 67, 85, 140, 210]
# → Шаг 6: минимум=210 → [15, 32, 67, 85, 140, 210]
# → Готово: [15, 32, 67, 85, 140, 210]
```

</details>

---

## Задание 3 — Доска лидеров (7 мин)

У тебя есть список игроков с их статистикой. Используй `sorted()` с `key=` и `lambda`, чтобы:

1. Отсортировать по убыванию очков (score)
2. Отсортировать по возрастанию смертей (deaths)
3. Отсортировать по «отношению K/D» — `kills / max(deaths, 1)` по убыванию

Выведи топ-3 в каждой категории.

```python
players = [
    {"name": "ShadowX",    "score": 4200, "kills": 87, "deaths": 12},
    {"name": "IronWolf",   "score": 3800, "kills": 65, "deaths": 8},
    {"name": "NightRaven", "score": 5100, "kills": 102,"deaths": 31},
    {"name": "BladeStorm", "score": 4900, "kills": 94, "deaths": 14},
    {"name": "GhostAce",   "score": 2700, "kills": 55, "deaths": 5},
]
```

<details>
<summary>Решение</summary>

```python
players = [
    {"name": "ShadowX",    "score": 4200, "kills": 87, "deaths": 12},
    {"name": "IronWolf",   "score": 3800, "kills": 65, "deaths": 8},
    {"name": "NightRaven", "score": 5100, "kills": 102,"deaths": 31},
    {"name": "BladeStorm", "score": 4900, "kills": 94, "deaths": 14},
    {"name": "GhostAce",   "score": 2700, "kills": 55, "deaths": 5},
]

# 1. По убыванию очков
by_score = sorted(players, key=lambda p: p["score"], reverse=True)
print("Топ-3 по очкам:")
for p in by_score[:3]:
    print(f"  {p['name']}: {p['score']} очков")
# → NightRaven: 5100 | BladeStorm: 4900 | ShadowX: 4200

# 2. По убыванию смертей (меньше — лучше)
by_deaths = sorted(players, key=lambda p: p["deaths"])
print("\nТоп-3 по наименьшим смертям:")
for p in by_deaths[:3]:
    print(f"  {p['name']}: {p['deaths']} смертей")
# → GhostAce: 5 | IronWolf: 8 | ShadowX: 12

# 3. По K/D
by_kd = sorted(
    players,
    key=lambda p: p["kills"] / max(p["deaths"], 1),
    reverse=True
)
print("\nТоп-3 по K/D:")
for p in by_kd[:3]:
    kd = p["kills"] / max(p["deaths"], 1)
    print(f"  {p['name']}: K/D = {kd:.2f}")
# → GhostAce: K/D = 11.00 | IronWolf: K/D = 8.12 | ShadowX: K/D = 7.25
```

</details>

---

## Задание 4 — Сортировка инвентаря (7 мин)

Напиши функцию `sort_inventory(items, by)`, которая принимает список предметов и строку `by` — название поля сортировки (`"name"`, `"rarity"`, `"weight"`). Редкость (`rarity`) должна сортироваться по порядку: `common → rare → epic → legendary`. Для других полей — обычная сортировка по возрастанию.

<details>
<summary>Решение</summary>

```python
RARITY_ORDER = {"common": 1, "rare": 2, "epic": 3, "legendary": 4}

inventory = [
    {"name": "Iron Sword",    "rarity": "common",    "weight": 8},
    {"name": "Dragon Shield", "rarity": "legendary", "weight": 15},
    {"name": "Shadow Cloak",  "rarity": "epic",      "weight": 3},
    {"name": "Steel Helm",    "rarity": "rare",      "weight": 5},
    {"name": "Flame Ring",    "rarity": "epic",      "weight": 1},
    {"name": "Bone Sword",    "rarity": "common",    "weight": 6},
]

def sort_inventory(items, by):
    if by == "rarity":
        return sorted(items, key=lambda item: RARITY_ORDER[item["rarity"]])
    elif by in ("name", "weight"):
        return sorted(items, key=lambda item: item[by])
    else:
        print(f"Неизвестное поле: {by}")
        return items

# По редкости
sorted_by_rarity = sort_inventory(inventory, "rarity")
for item in sorted_by_rarity:
    print(f"{item['name']} ({item['rarity']})")
# → Iron Sword (common) → Bone Sword (common) → Steel Helm (rare)
# → Shadow Cloak (epic) → Flame Ring (epic) → Dragon Shield (legendary)

# По весу
sorted_by_weight = sort_inventory(inventory, "weight")
for item in sorted_by_weight:
    print(f"{item['name']}: {item['weight']} кг")
# → Flame Ring: 1 → Shadow Cloak: 3 → Steel Helm: 5 ...
```

</details>

---

<quiz>
[
  {
    "question": "Какова сложность пузырьковой сортировки в худшем случае?",
    "options": [
      "A. O(n)",
      "B. O(n log n)",
      "C. O(n²)",
      "D. O(log n)"
    ],
    "answer": "C",
    "explanation": "Пузырьковая сортировка использует два вложенных цикла: внешний n раз, внутренний до n-1 раз. Итого n × (n-1) / 2 ≈ n² операций."
  },
  {
    "question": "Ты сортируешь список из 1000 игроков. Что будет быстрее?",
    "options": [
      "A. bubble_sort() — он простой и понятный",
      "B. selection_sort() — он делает меньше перестановок",
      "C. sorted() — встроенная функция Python",
      "D. Все три работают одинаково на 1000 элементах"
    ],
    "answer": "C",
    "explanation": "sorted() использует Timsort с O(n log n). На 1000 элементах: sorted() ~10 000 операций, bubble/selection ~500 000 операций. Разница в скорости — в десятки-сотни раз."
  },
  {
    "question": "Как отсортировать список врагов по убыванию их HP?",
    "options": [
      "A. sorted(enemies, key='hp', reverse=True)",
      "B. sorted(enemies, key=lambda e: e['hp'], reverse=True)",
      "C. enemies.sort('hp', descending=True)",
      "D. sorted(enemies, by=lambda e: -e['hp'])"
    ],
    "answer": "B",
    "explanation": "Параметр key= принимает функцию. lambda e: e['hp'] извлекает значение HP для сравнения. reverse=True переворачивает порядок — от большего к меньшему."
  },
  {
    "question": "В чём главное отличие сортировки выбором от пузырьковой?",
    "options": [
      "A. Выбор быстрее — его сложность O(n log n)",
      "B. Выбор делает меньше перестановок (всегда ровно n-1), но то же количество сравнений",
      "C. Выбор не требует отсортированного списка, а пузырёк — требует",
      "D. Пузырёк работает только с числами, выбор — с любыми данными"
    ],
    "answer": "B",
    "explanation": "Оба алгоритма O(n²) по сравнениям. Но selection sort делает ровно n-1 перестановок (по одной за проход), тогда как bubble sort может делать перестановки на каждом шаге внутреннего цикла."
  }
]
</quiz>

---

## Итог дня

Сегодня ты узнал:
- **Пузырьковая сортировка** O(n²) — сравниваем соседей, большие «всплывают» вверх. Проста в понимании, медленна на практике
- **Сортировка выбором** O(n²) — ищем минимум, ставим на место. Меньше перестановок, та же скорость
- **`sorted()`** O(n log n) — встроенный Timsort, в 100+ раз быстрее на реальных данных. **Используй его в реальном коде**
- **`key=` с `lambda`** — сортировка по любому полю объекта

Зачем тогда знать пузырёк и выбор, если `sorted()` лучше? Потому что они — фундамент. Понимая простые алгоритмы, ты поймёшь и сложные. И на собеседованиях их спрашивают часто.

---

<!--illustration
file: day_3/day_3_skill_tree.png
alt: Дерево навыков дня 3 — пузырьковая O(n²), выбор O(n²), Timsort O(n log n), key=lambda
prompt:
Create a Dark RPG UI skill tree infographic for Day 3 summary.

Title: "НАВЫКИ ДНЯ 3" in cream (#e8e0d4). Subtitle: "Алгоритмы сортировки" in gray-blue (#8ea4b8).

A branching skill tree:

Root node (teal glow): cards/stack icon — "Сортировка"

Branching:
- Node 1 (dim amber): "Пузырьковая O(n²)" — bubble icon, "понимаем, не используем"
- Node 2 (dim indigo): "Выбор O(n²)" — cursor icon, "чуть меньше перестановок"
- Node 3 (bright teal, largest): "Timsort O(n log n)" — lightning bolt, "sorted() — используем всегда"
  - Child (amber): lambda icon — "key=lambda"

The sorted() node is significantly larger and brighter.

Bottom glass checklist:
✓ Пузырьковая O(n²)
✓ Выбор O(n²)
✓ Timsort O(n log n)
✓ key=lambda

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette is MUTED and atmospheric, like cave crystals and bioluminescent fungi:
  - Teal #4db8c7 for primary elements (soft crystal light, NOT bright cyan)
  - Indigo #8b6cc1 for secondary elements (like glowing fungi)
  - Amber #d4854a for accents and highlights (like distant torchlight)
  - Cream #e8e0d4 for text (warm parchment white)
  - Green #7bc88f only for positive/success states
- ALL glows are SOFT and DIFFUSED: blur radius 10-15px, opacity 20-35%. Like bioluminescence in a dark cave. NEVER sharp neon edges. NEVER bright cyan #00ffff or bright purple #ff00ff.
- RPG ornamental frame: thin border 1px rgba(77,184,199,0.12), weathered stone corner ornaments (aged, slightly eroded, NOT polished).
- Nodes/orbs: dark glass rgba(10,14,26,0.85) with thin colored border. Icons inside as white silhouettes at 50% opacity.
- Connecting lines: organic curves (like roots/vines/light threads), NOT straight mechanical wires. 1-1.5px, soft glow.
- Glass-morphism panels for info cards: semi-transparent dark with subtle blur and soft shadow.
- Floating spore particles (1-3px dots) scattered across image — like Hollow Knight spores.
- Monospace font for all code text. Code colored: teal for keywords, amber for values, indigo for strings.
- Slight grain/noise texture on background surfaces.
- Russian (Cyrillic) text for all titles, labels, annotations.
- Three tiny color swatches (6x6px) at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight's City of Tears — contemplative, beautiful, mysterious. NOT aggressive, NOT cyberpunk.
-->

← [Day 2 — Бинарный поиск](day_2.md) | [Day 4 →](day_4.md)
