---
type: lesson
course: "python"
week: 8
day: 5
title: "Жадные алгоритмы и мемоизация"
concepts: [жадный алгоритм, контрпример к жадному алгоритму, мемоизация, lru_cache]
prerequisites: "[\"[week_8/day_4](/python/week_8/day_4/)\"]"
tags: [python, алгоритмы, greedy, мемоизация, динамическое программирование]
status: draft
---

# Day 5: Жадные алгоритмы и мемоизация

> **Сегодня:** узнаем, когда «брать лучшее прямо сейчас» работает — а когда нет. И как запоминать результаты, чтобы не считать дважды
> **Время:** ~45 минут

---

## Часть 1 — Задача о сдаче монетами

Представь: ты работаешь кассиром. Покупатель дал 100 рублей за товар стоимостью 37 рублей. Надо вернуть **63 рубля**. Монеты: 50, 10, 5, 1.

Как ты думаешь в голове? «Возьму монету в 50 — осталось 13. Возьму 10 — осталось 3. Возьму 1, 1, 1 — готово!» Итого: 5 монет.

Ты только что применил **жадный алгоритм**: на каждом шаге бери наибольшую монету, которая не превышает остаток.

```python
def make_change_greedy(amount, coins):
    """Жадная сдача: всегда берём наибольшую подходящую монету."""
    coins = sorted(coins, reverse=True)  # монеты по убыванию
    result = []
    for coin in coins:
        while amount >= coin:
            result.append(coin)
            amount -= coin
    return result

change = make_change_greedy(63, [50, 10, 5, 1])
print(change)         # → [50, 10, 1, 1, 1]
print(len(change))    # → 5 монет
```

Работает отлично! Но всегда ли?

---

## Часть 2 — Контрпример: когда жадность проигрывает

Представь экзотические монеты: **6, 4, 1 рубль**. Надо дать сдачу **8 рублей**.

Жадный алгоритм:
- Монета 6 — берём. Остаток: 2.
- Монета 4 — не влезает. Пропускаем.
- Монета 1 — берём. Остаток: 1.
- Монета 1 — берём. Остаток: 0.

Итого: **6 + 1 + 1 = 3 монеты**.

А оптимальный ответ: **4 + 4 = 2 монеты**.

```python
change = make_change_greedy(8, [6, 4, 1])
print(change)         # → [6, 1, 1]  — 3 монеты
print(len(change))    # → 3

# Оптимально:
print([4, 4])         # → 2 монеты!
```

Жадный алгоритм **не смотрит вперёд**. Он выбирает лучшее прямо сейчас, не задумываясь о последствиях. Иногда это приводит к неоптимальному результату.

> **Жадный алгоритм** — стратегия, при которой на каждом шаге выбирается локально наилучшее решение, без оглядки на будущее.

<!--illustration
file: day_5/day_5_greedy_coins.png
alt: Жадный алгоритм монет — работает для 50/10/5/1, проигрывает для 6/4/1
prompt:
Create a Dark RPG UI infographic showing greedy coin change — success vs failure.

Title: "ЖАДНЫЙ АЛГОРИТМ: МОНЕТЫ" in cream (#e8e0d4).

Two panels side by side:

LEFT panel ("Работает: монеты 50, 10, 5, 1") — teal, success:
Goal: дать сдачу 63 рубля
Step-by-step with RPG coin icons:
→ 50 (берём) остаток: 13
→ 10 (берём) остаток: 3
→ 1+1+1 (три монеты) остаток: 0
Result coins shown as 5 gold coin icons. Badge: "5 монет ✓ ОПТИМАЛЬНО" in green.

RIGHT panel ("СБОЙ: монеты 6, 4, 1") — amber warning, cracked:
Goal: дать сдачу 8 рублей
Жадный алгоритм:
→ 6 (берём) остаток: 2
→ 1+1 (два по 1) остаток: 0
Result: 3 coin icons in amber. Badge: "3 монеты — НЕ оптимально!" in amber.

Below RIGHT panel: a green correction card:
"Оптимально: 4+4 = 2 монеты!" with two coin icons, check mark.

Bottom center: "Жадный не смотрит вперёд — иногда это его слабость"

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

**Когда жадный работает:** стандартные монеты (1, 5, 10, 50), расписание задач по дедлайну, минимальное остовное дерево.

**Когда жадный не работает:** нестандартные монеты, задача о рюкзаке, большинство задач оптимизации.

<quiz>
question: "Монеты: 7, 3, 1. Нужно дать 9 рублей. Жадный алгоритм выдаёт:"
options:
  - "7+1+1 = 3 монеты (не оптимально)"
  - "3+3+3 = 3 монеты (оптимально)"
  - "7+3 — невозможно, не кратно"
  - "1×9 = 9 монет"
answer: 0
explanation: "Жадный берёт 7 (осталось 2), потом 1+1. Итого 3 монеты. Но оптимально: 3+3+3 тоже 3 монеты. В данном случае результат одинаковый, но жадный нашёл другой путь. Если бы нужно было 6: жадный даст 1×6=6 монет, а оптимально 3+3=2 монеты."
</quiz>

---

## Часть 3 — Мемоизация: запоминаем то, что уже посчитали

Помнишь наивный Фибоначчи из вчерашнего урока? Он был O(2^n) — катастрофически медленный, потому что считал одни и те же числа снова и снова.

Решение: **запоминать результаты**. Это и называется мемоизация.

```python
# Наивный — O(2^n), очень медленно для n > 35
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)
```

**Мемоизация вручную через dict:**

```python
def fib_memo(n, cache={}):
    """Фибоначчи с кешем. cache хранит уже посчитанные результаты."""
    if n in cache:              # уже считали — возвращаем из кеша
        return cache[n]
    if n <= 1:                  # базовый случай
        return n
    result = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    cache[n] = result           # сохраняем в кеш
    return result

print(fib_memo(10))   # → 55
print(fib_memo(50))   # → 12586269025 (мгновенно!)
print(fib_memo(100))  # → 354224848179261915075 (тоже мгновенно)
```

Теперь каждое число Фибоначчи считается **один раз**, результат сохраняется в словаре. Это **O(n)** — линейно.

Как работает кеш:
```
fib_memo(5)
  fib_memo(4) → считаем...
    fib_memo(3) → считаем...
      fib_memo(2) → cache[2] = 1
      fib_memo(1) → 1
    cache[3] = 2
    fib_memo(2) → уже в кеше! → 1
  cache[4] = 3
  fib_memo(3) → уже в кеше! → 2
cache[5] = 5
```

> **Мемоизация** — техника оптимизации: результат функции при первом вызове сохраняется в кеше. При повторном вызове с теми же аргументами возвращается готовый результат без пересчёта.

<!--illustration
file: day_5/day_5_memoization_cache.png
alt: Мемоизация Фибоначчи через dict — вычисленные значения помечены как «из кеша»
prompt:
Create a Dark RPG UI infographic showing Fibonacci with memoization cache.

Title: "МЕМОИЗАЦИЯ: ЗАПОМИНАЕМ РЕЗУЛЬТАТЫ" in cream (#e8e0d4). Subtitle: "fib(5) с кешем" in gray-blue.

A call tree for fib(5), but with cache visualization:

Compute path (colored, active):
fib(5) → fib(4) → fib(3) → fib(2) → fib(1) [base]
Each of these nodes is TEAL — they are computed for the first time.
Next to each: "cache[N] = X" label appears in amber as each result is saved.

Cached calls (grey, crossed with checkmark):
When fib(3) would be called a second time (from fib(4)'s other branch) — it appears as a DIM GREY node with a green checkmark and label "уже в кеше! → 2"
Same for fib(2): grey node, checkmark, "уже в кеше! → 1"

A small cache dictionary shown as a glass panel on the right:
cache = {
  0: 0,
  1: 1,
  2: 1,
  3: 2,
  4: 3,
  5: 5
}
Keys in teal, values in amber.

Badge comparison: "Без кеша: много вызовов | С кешем: каждое число 1 раз"

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

## Часть 4 — Мемоизация для задачи о сдаче

Напишем версию задачи о сдаче с мемоизацией, которая всегда находит оптимальный ответ:

```python
def min_coins(amount, coins, cache={}):
    """Минимальное количество монет для сдачи amount."""
    if amount in cache:         # уже решали эту сумму
        return cache[amount]
    if amount == 0:
        return 0
    if amount < 0:
        return float('inf')     # невозможно

    best = float('inf')
    for coin in coins:
        sub = min_coins(amount - coin, coins, cache)
        if sub + 1 < best:
            best = sub + 1

    cache[amount] = best
    return best

# Стандартные монеты:
print(min_coins(63, [50, 10, 5, 1]))  # → 5

# Экзотические — теперь находим оптимум:
print(min_coins(8, [6, 4, 1]))        # → 2  (4+4)
print(min_coins(11, [6, 4, 1]))       # → 3  (4+4+... нет, 6+4+1=3!)
```

Мемоизация + рекурсия = **динамическое программирование**. Это мощная техника, которую используют в задачах оптимизации по всему миру.

---

## Часть 5 — lru_cache: магический инструмент

Python предоставляет встроенный инструмент для мемоизации — `lru_cache` из модуля `functools`. Это так называемый **декоратор** — специальная метка перед функцией, которая добавляет ей новые возможности.

О декораторах мы поговорим подробнее в следующих уроках. Сейчас просто посмотри, как это выглядит:

```python
from functools import lru_cache

@lru_cache(maxsize=None)  # ← это декоратор, добавляет кеш автоматически
def fib_cached(n):
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

print(fib_cached(100))  # → 354224848179261915075 (мгновенно)
```

`@lru_cache` делает ровно то, что мы делали вручную через `dict` — только автоматически. LRU расшифровывается как «Least Recently Used»: если кеш заполнен, удаляет наименее недавно использованные записи.

**Когда использовать:** `lru_cache` удобен для простых случаев. Ручной `dict`-кеш — когда нужен контроль над тем, что и как сохраняется.

<!--illustration
file: day_5/day_5_lru_cache_magic.png
alt: Декоратор @lru_cache как магическая броня вокруг функции — до и после
prompt:
Create a Dark RPG UI infographic showing @lru_cache decorator as a magic armor wrapping a function.

Title: "@lru_cache — МАГИЧЕСКАЯ ОБЁРТКА" in cream (#e8e0d4).

Two states shown side by side:

LEFT state ("До @lru_cache") — dim, worn:
A function orb labeled "fib_naive(n)" in amber.
Around it: many red arrows showing repeated calls: fib(3)→twice, fib(2)→three times.
Clock icon below: "медленно, пересчитывает всё"
Label: "fib(35) — секунды ожидания"

RIGHT state ("После @lru_cache") — bright, armored:
Same function orb but now surrounded by glowing teal shield/armor layer — the cache.
The armor layer is labeled "@lru_cache" in teal.
Inside the armor: small cache slots showing stored values.
Arrows from repeated calls HIT the shield: "cache hit!" in green, bouncing back instantly.
Clock icon below: "мгновенно"
Label: "fib(100) — мгновенно"

Center: a transformation arrow with the decorator code:
@lru_cache(maxsize=None)
def fib_cached(n):
    ...
In teal monospace with @lru_cache highlighted in amber.

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

> **Игровой контекст:** в Minecraft NPC-персонажи используют алгоритм A* для поиска пути — это оптимизированный жадный алгоритм с эвристикой. В roguelike-играх враги часто используют чистую жадную стратегию: «иди к игроку по кратчайшему пути прямо сейчас» — быстро, но предсказуемо.

---

## Итог дня

| Концепция | Суть |
|-----------|------|
| Жадный алгоритм | На каждом шаге — локально лучший выбор |
| Контрпример | Ситуация, когда жадный даёт неоптимальный результат |
| Мемоизация | Сохраняем результат вычислений в словаре, не считаем дважды |
| `lru_cache` | Встроенный декоратор для автоматической мемоизации |

**Главная идея:** жадный алгоритм прост и быстр, но не всегда оптимален. Мемоизация превращает экспоненциальный алгоритм в линейный — ценой памяти.

---

## Задание 1 — Жадный выбор задач (10 мин)

У тебя есть список задач с дедлайном и наградой. Жадная стратегия: сначала берём задачи с наибольшей наградой. Посчитай общую награду, если можно сделать не более 3 задач.

```python
tasks = [
    {"name": "Убить дракона", "reward": 500},
    {"name": "Найти артефакт", "reward": 300},
    {"name": "Разведать пещеру", "reward": 150},
    {"name": "Починить мост", "reward": 100},
    {"name": "Помочь деревне", "reward": 50},
]

# Что должно работать:
print(greedy_tasks(tasks, max_tasks=3))  # → 950 (500 + 300 + 150)
```

<details>
<summary>Решение</summary>

```python
def greedy_tasks(tasks, max_tasks):
    sorted_tasks = sorted(tasks, key=lambda t: t["reward"], reverse=True)
    chosen = sorted_tasks[:max_tasks]
    total = sum(t["reward"] for t in chosen)
    for t in chosen:
        print(f"  ✓ {t['name']} — {t['reward']} золота")
    return total

tasks = [
    {"name": "Убить дракона", "reward": 500},
    {"name": "Найти артефакт", "reward": 300},
    {"name": "Разведать пещеру", "reward": 150},
    {"name": "Починить мост", "reward": 100},
    {"name": "Помочь деревне", "reward": 50},
]

print(greedy_tasks(tasks, max_tasks=3))  # → 950
```

</details>

---

## Задание 2 — Мемоизация суммы цифр (10 мин)

Возьми рекурсивную функцию `digit_sum(n)` из вчерашнего урока. Добавь мемоизацию через `dict`. Проверь, что при повторных вызовах результат берётся из кеша.

```python
cache = {}

def digit_sum_memo(n, cache):
    # твой код

print(digit_sum_memo(1234, cache))   # → 10
print(digit_sum_memo(1234, cache))   # → 10 (из кеша)
print(digit_sum_memo(9999, cache))   # → 36
print(len(cache))                    # → 2 (два разных числа)
```

<details>
<summary>Решение</summary>

```python
def digit_sum_memo(n, cache):
    if n in cache:
        return cache[n]
    if n < 10:
        return n
    result = n % 10 + digit_sum_memo(n // 10, cache)
    cache[n] = result
    return result

cache = {}
print(digit_sum_memo(1234, cache))  # → 10
print(digit_sum_memo(1234, cache))  # → 10 (из кеша)
print(digit_sum_memo(9999, cache))  # → 36
print(len(cache))                   # → 2
```

</details>

---

## Задание 3 — Поиск пути жадным (15 мин)

Дана матрица с числами — стоимость прохода через клетку. Жадный алгоритм идёт из левого верхнего угла в правый нижний, на каждом шаге выбирая минимальную из двух соседних клеток (вправо или вниз).

```python
grid = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1],
]
# Жадный путь: 1→1→1→1→1 = 5 (вниз, вниз, вправо, вправо)
# (не всегда оптимальный глобально, но наш жадный найдёт какой-то путь)

# Напиши функцию greedy_path(grid) → (стоимость, список шагов)
print(greedy_path(grid))  # → (7, [(0,0), (1,0), (2,0), (2,1), (2,2)])
```

<details>
<summary>Подсказка</summary>

Начни с `(0, 0)`. На каждом шаге смотри на правую клетку и нижнюю. Если обе доступны — бери ту, что меньше. Если только одна — бери её. Стой, когда дошёл до `(n-1, m-1)`.

</details>

<details>
<summary>Решение</summary>

```python
def greedy_path(grid):
    rows = len(grid)
    cols = len(grid[0])
    row, col = 0, 0
    cost = grid[0][0]
    path = [(0, 0)]

    while row < rows - 1 or col < cols - 1:
        can_right = col < cols - 1
        can_down = row < rows - 1

        if can_right and can_down:
            if grid[row][col + 1] <= grid[row + 1][col]:
                col += 1
            else:
                row += 1
        elif can_right:
            col += 1
        else:
            row += 1

        cost += grid[row][col]
        path.append((row, col))

    return cost, path

grid = [
    [1, 3, 1],
    [1, 5, 1],
    [4, 2, 1],
]
print(greedy_path(grid))  # → (7, [(0,0), (1,0), (2,0), (2,1), (2,2)])
```

</details>

---

## Задание 4 — Степень с мемоизацией (12 мин)

Напиши функцию `power_memo(base, exp, cache)` с мемоизацией. Используй умное разбиение: `base^exp = base^(exp//2) * base^(exp//2)` для чётных степеней — это ускоряет вычисление до O(log n).

```python
cache = {}
print(power_memo(2, 10, cache))  # → 1024
print(power_memo(2, 10, cache))  # → 1024 (из кеша)
print(power_memo(3, 8, cache))   # → 6561
```

<details>
<summary>Подсказка</summary>

Если `exp` чётное: `base^exp = (base^(exp//2))^2`. Если нечётное: `base^exp = base * base^(exp-1)`. Базовый случай: `exp == 0 → 1`.

</details>

<details>
<summary>Решение</summary>

```python
def power_memo(base, exp, cache):
    key = (base, exp)
    if key in cache:
        return cache[key]
    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = power_memo(base, exp // 2, cache)
        result = half * half
    else:
        result = base * power_memo(base, exp - 1, cache)
    cache[key] = result
    return result

cache = {}
print(power_memo(2, 10, cache))  # → 1024
print(power_memo(2, 10, cache))  # → 1024 (из кеша)
print(power_memo(3, 8, cache))   # → 6561
```

</details>

---

<!--illustration
file: day_5/day_5_skill_tree.png
alt: Дерево навыков дня 5 — жадный алгоритм, контрпример, мемоизация через dict, @lru_cache
prompt:
Create a Dark RPG UI skill tree infographic for Day 5 summary.

Title: "НАВЫКИ ДНЯ 5" in cream (#e8e0d4). Subtitle: "Жадные алгоритмы и мемоизация" in gray-blue (#8ea4b8).

A branching skill tree:

Root node (teal glow): coins icon — "Стратегии"

Branching:
- Node 1 (amber): greedy/coin icon — "Жадный алгоритм" — "берём лучшее сейчас"
  - Child (amber/red): warning — "Контрпример — жадный может проиграть"
- Node 2 (teal, larger): memory/cache icon — "Мемоизация" — "не считаем дважды"
  - Child (indigo): dict icon — "Вручную через dict"
  - Child (green): star — "@lru_cache — автоматически"

Bottom glass checklist:
✓ Жадный алгоритм
✓ Контрпример
✓ Мемоизация через dict
✓ @lru_cache

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

← [Day 4 — Рекурсия](/python/week_8/day_4/) | [Day 6 — Практика →](/python/week_8/day_6/)
