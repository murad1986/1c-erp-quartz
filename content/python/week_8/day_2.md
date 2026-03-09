---
type: lesson
course: "python"
week: 8
day: 2
title: "Линейный и бинарный поиск"
concepts: [линейный поиск O(n), бинарный поиск O(log n), условие отсортированности, bisect]
prerequisites: "[\"[week_8/day_1](/python/week_8/day_1/)\"]"
tags: [python, алгоритмы, поиск, бинарный поиск, bisect]
status: draft
---

# Day 2: Линейный и бинарный поиск

> **Сегодня:** научимся искать данные эффективно — поймём, почему бинарный поиск делает за 10 шагов то, на что у линейного уходит 1000.
> **Время:** ~40 минут

---

## Часть 1 — Задача: угадай число за минимум вопросов

Представь игру: я загадал число от 1 до 1000. Ты можешь задавать вопросы, я отвечаю «больше», «меньше» или «точно».

**Стратегия 1:** начинаешь с 1, потом 2, потом 3... В худшем случае — 1000 вопросов. Это **линейный поиск**.

**Стратегия 2:** называешь 500. Я говорю «больше». Называешь 750. Я говорю «меньше». Называешь 625... Каждый вопрос **отсекает половину** оставшихся чисел. За 10 вопросов — гарантированно найдёшь любое число от 1 до 1000. Это **бинарный поиск**.

Почему 10? Потому что log₂(1000) ≈ 10. Каждый шаг делит задачу пополам.

---

## Часть 2 — Линейный поиск: честный, но медленный

Линейный поиск — перебираем элементы один за другим, пока не найдём нужный.

```python
def linear_search(lst, target):
    steps = 0
    for i, item in enumerate(lst):
        steps += 1
        if item == target:
            print(f"Найдено за {steps} шагов на позиции {i}")
            return i
    print(f"Не найдено, проверено {steps} элементов")
    return -1

bosses = ["Asylum Demon", "Gaping Dragon", "Sif", "Ornstein", "Gwyn"]
linear_search(bosses, "Gwyn")     # → Найдено за 5 шагов на позиции 4
linear_search(bosses, "Aldrich") # → Не найдено, проверено 5 элементов
```

**Сложность:** O(n) — в худшем случае просматриваем все n элементов.

Для списка из 1 000 000 элементов: до миллиона проверок. Каждый раз.

---

## Часть 3 — Бинарный поиск: делим пополам

Бинарный поиск работает **только на отсортированном** списке. Это его главное условие. Почему? Потому что нам нужно знать: если средний элемент меньше нужного — значит, нужный точно справа. Без сортировки это невозможно гарантировать.

**Алгоритм:**
1. Берём левую и правую границы: `left = 0`, `right = len(lst) - 1`
2. Находим середину: `mid = (left + right) // 2`
3. Если `lst[mid] == target` — нашли!
4. Если `lst[mid] < target` — нужный правее: `left = mid + 1`
5. Если `lst[mid] > target` — нужный левее: `right = mid - 1`
6. Повторяем, пока `left <= right`

```python
def binary_search(lst, target):
    left, right = 0, len(lst) - 1
    steps = 0

    while left <= right:
        steps += 1
        mid = (left + right) // 2

        if lst[mid] == target:
            print(f"Найдено за {steps} шагов на позиции {mid}")
            return mid
        elif lst[mid] < target:
            left = mid + 1      # ищем в правой половине
        else:
            right = mid - 1     # ищем в левой половине

    print(f"Не найдено за {steps} шагов")
    return -1

levels = list(range(1, 1001))          # [1, 2, 3, ..., 1000]
binary_search(levels, 1000)            # → Найдено за 10 шагов на позиции 999
binary_search(levels, 777)             # → Найдено за 8 шагов на позиции 776
```

**Сложность:** O(log n). На миллионе элементов — максимум 20 шагов!

<!--illustration
file: day_2/day_2_binary_search_flow.png
alt: Блок-схема алгоритма бинарного поиска: left, right, mid, три ветки решения
prompt:
Create a Dark RPG UI infographic showing the binary search algorithm as an RPG quest flowchart.

Title: "АЛГОРИТМ БИНАРНОГО ПОИСКА" in cream (#e8e0d4).

A top-to-bottom flowchart with RPG quest-style nodes connected by organic glowing lines:

Step 1 (teal orb): "left=0, right=n-1" — "задаём границы"
↓
Step 2 (teal orb): "mid = (left+right) // 2" — "находим середину"
↓
Decision diamond (amber): "lst[mid] == target?"
- YES (green arrow right): "НАЙДЕНО! Возвращаем mid" (green orb with check mark)
- NO (continue down): "lst[mid] < target?"
  - YES (teal arrow): "left = mid + 1" → back to Step 2 (cycle arrow)
  - NO (indigo arrow): "right = mid - 1" → back to Step 2 (cycle arrow)

Exit condition: "left > right → НЕ НАЙДЕНО" (small amber orb with X)

Code reference panel at bottom in monospace:
left, right = 0, len(lst) - 1
mid = (left + right) // 2

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

## Часть 4 — Сравнение в числах

| Размер данных | Линейный O(n) | Бинарный O(log n) |
|---------------|---------------|-------------------|
| 1 000 | до 1 000 шагов | до 10 шагов |
| 1 000 000 | до 1 000 000 шагов | до 20 шагов |
| 1 000 000 000 | до 1 млрд шагов | до 30 шагов |

Это не опечатка. Бинарный поиск на миллиарде элементов делает максимум **30 шагов**.

<!--illustration
file: day_2/day_2_linear_vs_binary.png
alt: Сравнение линейного (731 шаг) и бинарного (7 шагов) поиска числа 731 в списке 1..1000
prompt:
Create a Dark RPG UI infographic comparing linear and binary search for number 731 in a list 1..1000.

Title: "ЛИНЕЙНЫЙ VS БИНАРНЫЙ ПОИСК" in cream (#e8e0d4). Subtitle: "ищем число 731 в списке 1..1000" in gray-blue.

Two panels side by side:

LEFT panel ("Линейный O(n)") — dim red-amber tint:
A long vertical bar representing 1000 elements. A scanning arrow starts at 1, goes down slowly. Numbers shown: 1, 2, 3, ... with "..." in the middle, ending at 731.
Badge: "731 шаг" in amber.
Small tired icon / skull hint at bottom.

RIGHT panel ("Бинарный O(log n)") — teal, bright:
A vertical bar split in halves. Show the binary search steps as a decision tree:
500 → (731 > 500, идём вправо) → 750 → (731 < 750, влево) → 625 → 687 → 718 → 734 → 731
Each step labeled with step number. Only 7 steps total.
Badge: "7 шагов" in green (#7bc88f).

Below both panels, a math glass card:
"1000 элементов → log₂(1000) ≈ 10 шагов максимум"

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

## Часть 5 — `bisect`: встроенный бинарный поиск

Python уже умеет в бинарный поиск — модуль `bisect`. Он не просто ищет, но и показывает, **куда вставить** новый элемент, чтобы список остался отсортированным.

```python
import bisect

scores = [100, 250, 400, 650, 800, 950]  # отсортировано!

# bisect_left: позиция для вставки нового элемента
pos = bisect.bisect_left(scores, 400)
print(pos)                               # → 2 (позиция числа 400)

# bisect_right: позиция после совпадения
pos = bisect.bisect_right(scores, 400)
print(pos)                               # → 3 (после 400)

# insort: вставить с сохранением порядка
bisect.insort(scores, 500)
print(scores)  # → [100, 250, 400, 500, 650, 800, 950]

# Проверка наличия через bisect_left
def is_in_sorted(lst, target):
    pos = bisect.bisect_left(lst, target)
    return pos < len(lst) and lst[pos] == target

print(is_in_sorted(scores, 650))  # → True
print(is_in_sorted(scores, 999))  # → False
```

<!--illustration
file: day_2/day_2_bisect_module.png
alt: Модуль bisect — bisect_left, bisect_right и insort на отсортированном списке очков
prompt:
Create a Dark RPG UI infographic showing the bisect module's bisect_left() function in action.

Title: "МОДУЛЬ bisect — ВСТРОЕННЫЙ БИНАРНЫЙ ПОИСК" in cream (#e8e0d4).

Central: a sorted list as inventory slots:
[100] [250] [400] [650] [800] [950]
Index: 0     1     2     3     4     5

Three operations shown as glass panels:

Panel 1 (teal): bisect_left(scores, 400)
Arrow pointing between index 1 and 2, landing at slot 400. Label: "→ 2 (позиция числа 400)"

Panel 2 (indigo): bisect_right(scores, 400)
Arrow pointing after slot 400, to position 3. Label: "→ 3 (после 400)"

Panel 3 (amber): insort(scores, 500)
Before: [100, 250, 400, 650, 800, 950]
After: [100, 250, 400, 500, 650, 800, 950]
New slot "500" glows amber, sliding into place between 400 and 650.

Bottom info card: "bisect — это бинарный поиск в одной строке" with teal glow.

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

## Задание 1 — Угадай число (5 мин)

Реализуй игру «Угадай число». Программа загадывает случайное число от 1 до 100, пользователь угадывает. После каждой попытки — подсказка «больше» или «меньше». Считай попытки. Если угадал — выведи, сколько попыток понадобилось.

<details>
<summary>Решение</summary>

```python
import random

def guess_game():
    secret = random.randint(1, 100)
    attempts = 0
    print("Я загадал число от 1 до 100. Угадывай!")

    while True:
        try:
            guess = int(input("Твоя догадка: "))
        except ValueError:
            print("Введи целое число!")
            continue

        attempts += 1

        if guess == secret:
            print(f"Точно! Ты угадал за {attempts} попыток.")
            if attempts <= 7:
                print("Отличная стратегия! Деление пополам?")
            break
        elif guess < secret:
            print("Больше!")
        else:
            print("Меньше!")

guess_game()
```

</details>

---

## Задание 2 — Бинарный поиск с подробным выводом (7 мин)

Напиши функцию `binary_search_verbose(lst, target)`, которая на каждом шаге выводит: номер шага, текущие границы `[left, right]`, индекс середины и значение в середине. В конце — итог: найдено или нет.

```
Шаг 1: границы [0, 999], mid=499, значение=500
Шаг 2: границы [500, 999], mid=749, значение=750
...
Найдено на позиции 776 за 8 шагов
```

<details>
<summary>Решение</summary>

```python
def binary_search_verbose(lst, target):
    left, right = 0, len(lst) - 1
    step = 0

    while left <= right:
        step += 1
        mid = (left + right) // 2
        print(f"Шаг {step}: границы [{left}, {right}], "
              f"mid={mid}, значение={lst[mid]}")

        if lst[mid] == target:
            print(f"Найдено на позиции {mid} за {step} шагов")
            return mid
        elif lst[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    print(f"Не найдено за {step} шагов")
    return -1

data = list(range(1, 1001))
binary_search_verbose(data, 777)
# → Шаг 1: границы [0, 999], mid=499, значение=500
# → Шаг 2: границы [500, 999], mid=749, значение=750
# → Шаг 3: границы [750, 999], mid=874, значение=875
# → ...
# → Найдено на позиции 776 за 8 шагов
```

</details>

---

## Задание 3 — Поиск в базе игроков (8 мин)

У тебя есть отсортированный список ников игроков. Напиши функцию `find_player_rank(players, name)`, которая:
- Использует `bisect.bisect_left` для поиска
- Если игрок найден — возвращает его ранг (позиция + 1, т.к. ранги с 1)
- Если не найден — возвращает `None` и выводит «Игрок не найден»

Протестируй на списке из 20+ игроков.

<details>
<summary>Решение</summary>

```python
import bisect

players = sorted([
    "AceHunter", "BladeRunner", "CryptoKnight", "DarkPhoenix",
    "EchoStrike", "FrostByte", "GhostWalker", "HyperZone",
    "IronFist", "JadeWolf", "KillSwitch", "LegendSlayer",
    "MegaForce", "NightCrawler", "OmegaRed", "PhantomX",
    "QuantumLeap", "RavenClaw", "ShadowBlade", "TurboNova",
    "UltraVoid", "VenomStrike", "WarpSpeed", "XenonRush",
    "YellowFlash", "ZeroCool"
])

def find_player_rank(players, name):
    pos = bisect.bisect_left(players, name)
    if pos < len(players) and players[pos] == name:
        rank = pos + 1
        print(f"Игрок {name} найден, ранг: #{rank}")
        return rank
    else:
        print(f"Игрок {name} не найден")
        return None

find_player_rank(players, "ShadowBlade")   # → Игрок ShadowBlade найден, ранг: #19
find_player_rank(players, "ZeroCool")      # → Игрок ZeroCool найден, ранг: #26
find_player_rank(players, "BananaSlug")    # → Игрок BananaSlug не найден
```

</details>

---

## Задание 4 — Сравни скорость (8 мин)

Создай отсортированный список из 500 000 чисел. Замерь время поиска последнего элемента тремя способами:
1. Линейный поиск (цикл `for`)
2. Твоя `binary_search()` из Части 3
3. `bisect.bisect_left()` из стандартной библиотеки

Выведи результаты и вычисли, во сколько раз бинарный быстрее линейного.

<details>
<summary>Решение</summary>

```python
import time
import bisect

SIZE = 500_000
data = list(range(SIZE))
target = SIZE - 1  # последний элемент — worst case для линейного

# 1. Линейный поиск
start = time.time()
for i, x in enumerate(data):
    if x == target:
        found_at = i
        break
linear_time = time.time() - start

# 2. Наш binary_search
def binary_search(lst, target):
    left, right = 0, len(lst) - 1
    while left <= right:
        mid = (left + right) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

start = time.time()
binary_search(data, target)
binary_time = time.time() - start

# 3. bisect
start = time.time()
pos = bisect.bisect_left(data, target)
bisect_time = time.time() - start

print(f"Линейный поиск:  {linear_time:.6f} сек")
print(f"Бинарный поиск:  {binary_time:.6f} сек")
print(f"bisect:          {bisect_time:.6f} сек")
print(f"Бинарный быстрее линейного в {linear_time/binary_time:.0f}x раз")
# → Линейный поиск:  0.018234 сек
# → Бинарный поиск:  0.000018 сек
# → bisect:          0.000001 сек
# → Бинарный быстрее линейного в ~1000x раз
```

</details>

---

<quiz>
[
  {
    "question": "Главное условие для работы бинарного поиска — это...",
    "options": [
      "A. Список должен содержать только числа",
      "B. Список должен быть отсортирован",
      "C. Список должен иметь чётное количество элементов",
      "D. Список должен быть короче 1000 элементов"
    ],
    "answer": "B",
    "explanation": "Бинарный поиск делит список пополам, опираясь на то, что элементы упорядочены. Без сортировки невозможно знать, в какой половине искать дальше."
  },
  {
    "question": "Сколько максимум шагов нужно бинарному поиску, чтобы найти элемент в списке из 1024 элементов?",
    "options": [
      "A. 1024",
      "B. 512",
      "C. 10",
      "D. 100"
    ],
    "answer": "C",
    "explanation": "log₂(1024) = 10. Каждый шаг делит задачу пополам: 1024 → 512 → 256 → 128 → 64 → 32 → 16 → 8 → 4 → 2 → 1."
  },
  {
    "question": "Что делает bisect.insort(lst, value)?",
    "options": [
      "A. Ищет value в lst и возвращает его позицию",
      "B. Удаляет все вхождения value из lst",
      "C. Вставляет value в lst, сохраняя сортировку",
      "D. Создаёт новый отсортированный список из lst и value"
    ],
    "answer": "C",
    "explanation": "bisect.insort использует бинарный поиск, чтобы найти правильную позицию, и вставляет элемент туда — список остаётся отсортированным."
  },
  {
    "question": "Ты ищешь элемент в несортированном списке из 1 000 000 элементов. Можешь ли ты использовать бинарный поиск прямо сейчас?",
    "options": [
      "A. Да, бинарный поиск работает на любом списке",
      "B. Нет, сначала нужно отсортировать список",
      "C. Да, но только если элемент — число",
      "D. Нет, бинарный поиск работает только на списках до 10 000 элементов"
    ],
    "answer": "B",
    "explanation": "Бинарный поиск требует отсортированного списка. Но учти: если поиск нужен только один раз, может быть выгоднее использовать линейный — сортировка сама по себе стоит O(n log n)."
  }
]
</quiz>

---

## Итог дня

Сегодня ты узнал:
- **Линейный поиск** O(n) — надёжный, но медленный на больших данных
- **Бинарный поиск** O(log n) — в тысячи раз быстрее, но **требует отсортированного списка**
- log₂(1 000 000) ≈ 20 — это максимум шагов бинарного поиска на миллионе элементов
- **`bisect`** — встроенный модуль Python с оптимизированным бинарным поиском

Завтра разберёмся с сортировкой — поймём, как именно данные оказываются в нужном порядке и почему одни алгоритмы делают это в тысячу раз быстрее других.

---

<!--illustration
file: day_2/day_2_skill_tree.png
alt: Дерево навыков дня 2 — линейный O(n), бинарный O(log n), условие сортировки, bisect
prompt:
Create a Dark RPG UI skill tree infographic for Day 2 summary.

Title: "НАВЫКИ ДНЯ 2" in cream (#e8e0d4). Subtitle: "Поиск в данных" in gray-blue (#8ea4b8).

A branching skill tree with circular nodes:

Root node (teal glow): magnifier icon — "Поиск"

Branching:
- Node 1 (amber): "Линейный O(n)" with sub-label "перебор всех"
- Node 2 (teal, larger): "Бинарный O(log n)" with sub-label "делим пополам"
  - Child (indigo): warning triangle — "Условие: список отсортирован!"
  - Child (green): star — "bisect — встроенный"

Connecting lines: organic glowing vines. The binary search node is brighter than linear.

Bottom glass checklist panel:
✓ Линейный поиск O(n)
✓ Бинарный поиск O(log n)
✓ Условие: отсортированный список
✓ bisect

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

← [Day 1 — Сложность алгоритмов](/python/week_8/day_1/) | [Day 3 — Сортировка →](/python/week_8/day_3/)
