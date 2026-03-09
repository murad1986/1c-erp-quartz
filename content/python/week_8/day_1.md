---
type: lesson
course: "python"
week: 8
day: 1
title: "Алгоритмы вокруг нас — что такое сложность"
concepts: [алгоритм, Big O нотация, O(1) O(n) O(n²), time.time()]
prerequisites: "[\"[week_7/day_7](/python/week_7/day_7/)\"]"
tags: [python, алгоритмы, big-o, сложность, time]
status: draft
---

# Day 1: Алгоритмы вокруг нас — что такое сложность

> **Сегодня:** узнаем, что такое алгоритм, почему одни программы работают мгновенно, а другие лагают — и научимся это измерять.
> **Время:** ~40 минут

---

## Часть 1 — Алгоритм: точный рецепт без права на ошибку

Представь, что ты объясняешь другу, как скрафтить меч в Minecraft. Ты не можешь сказать «ну, там положи что-нибудь металлическое». Нужен **точный** порядок действий: 2 палки снизу, 3 железных слитка сверху, строго по сетке.

Это и есть **алгоритм** — точная последовательность шагов, которая решает задачу и всегда даёт правильный результат.

Свойства хорошего алгоритма:
- **Точность** — каждый шаг однозначен
- **Конечность** — алгоритм заканчивается (не зависает в бесконечном цикле)
- **Результат** — даёт ответ для любых допустимых входных данных

```python
# Алгоритм: найти максимум в списке
def find_max(numbers):
    maximum = numbers[0]          # начинаем с первого
    for num in numbers:           # смотрим каждый элемент
        if num > maximum:
            maximum = num         # обновляем максимум
    return maximum

print(find_max([3, 7, 1, 9, 4]))  # → 9
```

---

## Часть 2 — Реальная проблема: миллион контактов

У тебя в телефоне 1 000 000 контактов (ладно, пусть это будет база игроков крупного сервера). Тебе нужно найти игрока «ZeroCool_88».

**Вариант 1:** листаешь всех по очереди — от «Aaronite» до «ZeroCool_88». В худшем случае это 1 000 000 проверок.

**Вариант 2:** имена хранятся в словаре. Ты просто пишешь `players["ZeroCool_88"]` — и получаешь ответ **мгновенно**, независимо от размера базы.

Разница — в **алгоритме**. И эту разницу описывает **Big O нотация**.

---

## Часть 3 — Big O: язык для описания скорости

Big O — это способ сказать «как быстро растёт время работы алгоритма, если растут данные».

Не точное время в секундах (оно зависит от компьютера), а **темп роста**.

| Нотация | Название | Пример |
|---------|----------|--------|
| **O(1)** | Константная | Доступ по ключу в словаре |
| **O(n)** | Линейная | Перебор всего списка |
| **O(n²)** | Квадратичная | Два вложенных цикла по списку |

**Аналогия с игровым лагом:**

Представь: движок Dark Souls каждый кадр проверяет, попал ли меч во врага.

- O(1) — проверка одной точки попадания. 60 FPS. Игра летает.
- O(n) — проверка всех врагов на уровне. Чем больше врагов, тем медленнее. 30 FPS на большой арене.
- O(n²) — каждый враг проверяется против каждого другого врага. 100 врагов = 10 000 проверок. **Лаг. Смерть. Позор.**

<!--illustration
file: day_1/day_1_big_o_complexity.png
alt: График кривых сложности Big O: O(1), O(log n), O(n), O(n log n), O(n²)
prompt:
Create a Dark RPG UI infographic showing Big O complexity curves as a graph.

Title: "НОТАЦИЯ BIG O — СКОРОСТЬ РОСТА" in cream (#e8e0d4). Subtitle: "чем круче кривая, тем сильнее лагает" in muted gray-blue (#8ea4b8).

Central element: a coordinate graph with RPG styling — axes as glowing stone edges.
- X-axis labeled "размер данных (n)" in cream, with markers: 10, 100, 1000.
- Y-axis labeled "время работы" in cream.

Five curves, each color-coded and labeled:
- O(1) — flat horizontal line, GREEN (#7bc88f). Label: "O(1) — мгновенно (словарь)"
- O(log n) — gently rising curve, TEAL (#4db8c7). Label: "O(log n) — бинарный поиск"
- O(n) — diagonal line, CREAM (#e8e0d4). Label: "O(n) — перебор списка"
- O(n log n) — slightly steeper curve, AMBER (#d4854a). Label: "O(n log n) — sorted()"
- O(n²) — sharply rising parabola, INDIGO (#8b6cc1) with soft red-amber tint. Label: "O(n²) — два цикла → ЛАГ"

Gaming annotation panel at top-right: "FPS аналогия:" with three lines:
- "O(1) → 60 FPS" (green)
- "O(n) → 30 FPS на арене" (amber)
- "O(n²) → смерть. Позор." (red-amber)

The O(n²) curve glows with a soft warning amber at the steep end.

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

```python
# O(1) — время не зависит от размера данных
def get_player(players_dict, name):
    return players_dict.get(name, "не найден")  # мгновенно всегда

# O(n) — время растёт вместе с размером списка
def find_player_linear(players_list, name):
    for player in players_list:     # в худшем — перебираем всех
        if player == name:
            return True
    return False

# O(n²) — два вложенных цикла = катастрофа на больших данных
def find_duplicates_slow(players_list):
    duplicates = []
    for i in range(len(players_list)):          # внешний цикл
        for j in range(i + 1, len(players_list)):  # внутренний цикл
            if players_list[i] == players_list[j]:
                duplicates.append(players_list[i])
    return duplicates
```

<!--illustration
file: day_1/day_1_algo_in_game.png
alt: Dark Souls арена — каскад проверок коллизий O(n²) для каждой пары врагов
prompt:
Create a Dark RPG UI infographic showing O(n²) collision detection in a Dark Souls-style arena.

Title: "DARK SOULS: O(n²) — КАСКАД ПРОВЕРОК" in cream (#e8e0d4). Subtitle: "каждый враг против каждого другого" in muted amber.

Central: a dark stone arena viewed from above. Multiple enemy silhouettes (small knight icons) — 5 of them, labeled Enemy 1 through Enemy 5.

Between every pair of enemies: a glowing amber line with a collision check marker (small shield/sword icon). All pairs connected: 5×4/2 = 10 lines total, creating a web of checks.

Below arena: math panel in glass:
"5 врагов → 10 проверок"
"10 врагов → 45 проверок"
"100 врагов → 4950 проверок"

Annotations on the side with teal → amber → red-amber gradient:
- 10 врагов: OK
- 50 врагов: лаг
- 100 врагов: краш

Top label: "Каждый кадр движок проверяет все пары" in cream.

Ominous red-amber glow at the edges — the arena is overloading.

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

## Часть 4 — Замеряем время: `time.time()`

Теория — хорошо. Но давай **измерим** разницу своими руками.

`time.time()` возвращает текущее время в секундах (с момента 1 января 1970 года). Если взять время до и после выполнения кода — получим, сколько он работал.

```python
import time

start = time.time()         # запоминаем момент начала
# ... здесь код, который измеряем ...
end = time.time()           # запоминаем момент конца

elapsed = end - start       # разница = время выполнения
print(f"Время: {elapsed:.6f} сек")  # → Время: 0.000123 сек
```

---

## Часть 5 — Эксперимент: список vs словарь

Посмотрим на реальные числа:

```python
import time

# Создаём тестовые данные
SIZE = 100_000
players_list = [f"player_{i}" for i in range(SIZE)]
players_dict = {f"player_{i}": i for i in range(SIZE)}
target = f"player_{SIZE - 1}"  # самый последний — worst case

# Замер линейного поиска O(n)
start = time.time()
result = target in players_list
end = time.time()
print(f"Список (линейный): {end - start:.6f} сек")  # → ~0.003 сек

# Замер поиска по словарю O(1)
start = time.time()
result = target in players_dict
end = time.time()
print(f"Словарь (хэш):     {end - start:.6f} сек")  # → ~0.000001 сек
```

На 100 000 элементов разница — в **тысячи раз**. На миллионе будет ещё больше.

<!--illustration
file: day_1/day_1_list_vs_dict_search.png
alt: Сравнение поиска в списке O(n) и словаре O(1) с замером времени
prompt:
Create a Dark RPG UI infographic comparing linear search in a list vs O(1) lookup in a dict.

Title: "СПИСОК VS СЛОВАРЬ: ПОИСК" in cream (#e8e0d4).

Two glass-morphism panels side by side:

LEFT panel (dim, labelled "Список O(n)"):
- A vertical column of 12 dark stone inventory slots, each containing "player_N" (small text). A magnifying glass icon starts at the top and draws a long scanning arrow all the way down, stopping at the last slot — "player_99999".
- Red-amber tint on the panel.
- Time badge below: "~0.003 сек" in amber.
- Label: "перебирает ВСЕ 100 000"

RIGHT panel (bright, labelled "Словарь O(1)"):
- A single dark glass panel with a key icon and arrow pointing directly to "player_99999". No scanning — instant.
- Teal glow, clean.
- Time badge below: "~0.000001 сек" in green (#7bc88f).
- Label: "мгновенно всегда"

Large divider arrow between panels. Below both panels: a glass info card:
"Разница: в 3000 раз на 100 000 элементах"

Code snippet at bottom in monospace:
target in players_list  →  O(n)
target in players_dict  →  O(1)

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

## Задание 1 — Напиши свою функцию замера (5 мин)

Каждый раз писать `start = time.time()` ... `end = time.time()` — неудобно. Напиши функцию `measure(func, *args)`, которая принимает функцию и аргументы, запускает её, измеряет время и возвращает результат и время.

```python
# Пример использования:
result, elapsed = measure(sum, range(1_000_000))
print(f"Результат: {result}, время: {elapsed:.6f} сек")
```

<details>
<summary>Решение</summary>

```python
import time

def measure(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    elapsed = end - start
    return result, elapsed

# Тест
result, elapsed = measure(sum, range(1_000_000))
print(f"Результат: {result}")              # → Результат: 499999500000
print(f"Время: {elapsed:.6f} сек")        # → Время: 0.023451 сек

# Ещё тест
result, elapsed = measure(max, [3, 7, 1, 9, 4])
print(f"Максимум: {result}")              # → Максимум: 9
print(f"Время: {elapsed:.6f} сек")        # → Время: 0.000003 сек
```

</details>

---

## Задание 2 — O(1) vs O(n): почувствуй разницу (7 мин)

Создай список и словарь с 10 000 и 100 000 игроков. Замерь поиск последнего элемента в обоих случаях. Выведи результаты в виде таблицы.

Ожидаемый вывод:
```
Размер    | Список (сек)  | Словарь (сек)
10000     | 0.000412      | 0.000001
100000    | 0.003891      | 0.000001
```

<details>
<summary>Решение</summary>

```python
import time

def search_list(lst, target):
    return target in lst

def search_dict(dct, target):
    return target in dct

print(f"{'Размер':<10}| {'Список (сек)':<15}| {'Словарь (сек)'}")
print("-" * 45)

for size in [10_000, 100_000]:
    lst = [f"player_{i}" for i in range(size)]
    dct = {f"player_{i}": i for i in range(size)}
    target = f"player_{size - 1}"

    start = time.time()
    search_list(lst, target)
    list_time = time.time() - start

    start = time.time()
    search_dict(dct, target)
    dict_time = time.time() - start

    print(f"{size:<10}| {list_time:<15.6f}| {dict_time:.6f}")
# → 10000     | 0.000412      | 0.000001
# → 100000    | 0.003891      | 0.000001
```

</details>

---

## Задание 3 — Определи сложность (5 мин)

Посмотри на функции ниже и определи их Big O сложность. Объясни почему.

```python
def func_a(players):
    return players[0]

def func_b(players):
    for p in players:
        print(p)

def func_c(players):
    for p1 in players:
        for p2 in players:
            if p1 != p2:
                print(p1, p2)

def func_d(players, name):
    return name in set(players)
```

<details>
<summary>Решение</summary>

```python
# func_a — O(1)
# Доступ по индексу всегда мгновенный, не зависит от длины списка

# func_b — O(n)
# Один цикл по всем элементам — время растёт линейно

# func_c — O(n²)
# Два вложенных цикла: для каждого из n элементов
# проходим ещё раз по всем n → n * n = n²

# func_d — O(n) в среднем
# set(players) создаёт множество — это O(n)
# проверка "in set" — это O(1)
# Итого: O(n) + O(1) = O(n) (доминирует создание множества)
```

</details>

---

## Задание 4 — O(n²) на практике: найди дубликаты (8 мин)

Напиши **две версии** функции поиска дубликатов в списке игроков:
- `find_duplicates_slow(lst)` — через два вложенных цикла, O(n²)
- `find_duplicates_fast(lst)` — через множество (set), O(n)

Замерь обе на списке из 5000 элементов с несколькими дубликатами. Выведи время каждой.

<details>
<summary>Решение</summary>

```python
import time

def find_duplicates_slow(lst):
    duplicates = set()
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):    # O(n²)
            if lst[i] == lst[j]:
                duplicates.add(lst[i])
    return duplicates

def find_duplicates_fast(lst):
    seen = set()
    duplicates = set()
    for item in lst:                        # O(n)
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return duplicates

# Тестовые данные: 5000 игроков, среди которых есть дубликаты
players = [f"player_{i % 4900}" for i in range(5000)]

start = time.time()
result_slow = find_duplicates_slow(players)
slow_time = time.time() - start
print(f"Медленная O(n²): {slow_time:.4f} сек")  # → ~1.2 сек

start = time.time()
result_fast = find_duplicates_fast(players)
fast_time = time.time() - start
print(f"Быстрая O(n):   {fast_time:.6f} сек")   # → ~0.001 сек

print(f"Быстрая версия в {slow_time/fast_time:.0f}x раз быстрее!")
```

</details>

---

<quiz>
[
  {
    "question": "Что означает O(1) в нотации Big O?",
    "options": [
      "A. Алгоритм работает 1 секунду",
      "B. Время выполнения не зависит от размера данных",
      "C. Алгоритм делает ровно 1 операцию",
      "D. Алгоритм самый быстрый из возможных"
    ],
    "answer": "B",
    "explanation": "O(1) означает константное время — алгоритм работает одинаково быстро независимо от того, 10 элементов в данных или 10 миллионов. Пример: доступ к элементу словаря по ключу."
  },
  {
    "question": "У тебя список из 1000 игроков. Ты ищешь игрока перебором (цикл for). В худшем случае сколько проверок нужно?",
    "options": [
      "A. 1",
      "B. 10",
      "C. 500",
      "D. 1000"
    ],
    "answer": "D",
    "explanation": "Линейный поиск O(n) в худшем случае перебирает все n элементов — когда нужный элемент стоит последним или его нет вообще."
  },
  {
    "question": "Какой из вариантов кода имеет сложность O(n²)?",
    "options": [
      "A. for i in lst: print(i)",
      "B. print(lst[0])",
      "C. for i in lst:\n       for j in lst: print(i, j)",
      "D. if name in my_dict: print('найден')"
    ],
    "answer": "C",
    "explanation": "Два вложенных цикла, каждый из которых проходит по всем n элементам, дают n × n = n² операций — это O(n²)."
  },
  {
    "question": "Что возвращает time.time()?",
    "options": [
      "A. Текущее время в формате ЧЧ:ММ:СС",
      "B. Количество секунд с 1 января 1970 года",
      "C. Время работы программы в миллисекундах",
      "D. Текущую дату и время как строку"
    ],
    "answer": "B",
    "explanation": "time.time() возвращает float — количество секунд, прошедших с 'эпохи Unix' (1 января 1970). Чтобы замерить время, берём разницу двух вызовов: до и после кода."
  }
]
</quiz>

---

## Итог дня

Сегодня ты узнал:
- **Алгоритм** — точная последовательность шагов с гарантированным результатом
- **Big O** — язык для описания того, как растёт время работы при росте данных
- **O(1)** — мгновенно (словарь), **O(n)** — линейно (перебор), **O(n²)** — медленно (два цикла)
- **time.time()** — инструмент для измерения реального времени выполнения

Завтра узнаем, как **искать** в данных по-умному: сравним линейный и бинарный поиск.

---

<!--illustration
file: day_1/day_1_skill_tree.png
alt: Дерево навыков дня 1 — алгоритм, Big O, O(1)/O(n)/O(n²), замер времени
prompt:
Create a Dark RPG UI skill tree infographic for Day 1 summary.

Title: "НАВЫКИ ДНЯ 1" in cream (#e8e0d4). Subtitle: "Сложность алгоритмов" in gray-blue (#8ea4b8).

A branching skill tree with circular nodes connected by organic luminous threads:

Root node (largest, teal glow): scroll icon — "Алгоритм"

Branching from root:
- Node 1 (teal): graph curve icon — "Big O нотация"
  - Child: green orb — "O(1) — мгновенно"
  - Child: teal orb — "O(n) — линейно"
  - Child: indigo orb — "O(n²) — медленно"
- Node 2 (amber): timer icon — "time.time()"

All nodes connected by soft glowing organic vines. Each node has a small label in Russian.

Bottom glass checklist panel:
✓ Алгоритм
✓ Big O
✓ O(1) / O(n) / O(n²)
✓ Замер времени

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

← [Week 7 Practice](/python/week_7/day_6/) | [Day 2 — Поиск →](/python/week_8/day_2/)
