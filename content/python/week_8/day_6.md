---
type: lesson
course: "[[python_basics/README]]"
week: 8
day: 6
title: "Практика — алгоритмические задачи"
concepts: []
prerequisites: "[\"[[week_8/day_5]]\"]"
tags: [python, алгоритмы, практика, анаграммы, сортировка, бинарный поиск]
status: draft
---

# Day 6: Практика — алгоритмические задачи

> **Сегодня:** закрепляем всё, что изучили за неделю — поиск, сортировку, структуры данных
> **Время:** ~60 минут

Сегодня нет теории. Только задачи — от простых к сложным. Каждую попробуй решить самостоятельно, прежде чем смотреть решение.

---

## Задача 1 — Анаграммы (10 мин)

Две строки являются **анаграммами**, если состоят из одинаковых букв в разном порядке.

```
"listen" и "silent" → анаграммы
"hello" и "world"   → не анаграммы
"кот" и "ток"       → анаграммы
```

Напиши функцию `is_anagram(s1, s2) → bool`.

**Требования:**
- Регистр не важен (`"Listen"` и `"Silent"` — анаграммы)
- Пробелы игнорируются

```python
print(is_anagram("listen", "silent"))       # → True
print(is_anagram("hello", "world"))         # → False
print(is_anagram("Astronomer", "Moon starer"))  # → True
print(is_anagram("кот", "ток"))             # → True
```

<details>
<summary>Подсказка — способ 1: через sorted()</summary>

Отсортируй буквы обеих строк и сравни. Анаграммы дадут одинаковые отсортированные строки.

</details>

<details>
<summary>Решение через sorted()</summary>

```python
def is_anagram(s1, s2):
    # Приводим к нижнему регистру, убираем пробелы
    clean1 = s1.lower().replace(" ", "")
    clean2 = s2.lower().replace(" ", "")
    return sorted(clean1) == sorted(clean2)

print(is_anagram("listen", "silent"))           # → True
print(is_anagram("hello", "world"))             # → False
print(is_anagram("Astronomer", "Moon starer"))  # → True
print(is_anagram("кот", "ток"))                 # → True
```

</details>

<!--illustration
file: day_6/day_6_anagram_detection.png
alt: Два подхода к проверке анаграмм — через sorted() и через dict-подсчёт букв
prompt:
Create a Dark RPG UI infographic showing two approaches to anagram detection.

Title: "АНАГРАММЫ: ДВА ПОДХОДА" in cream (#e8e0d4).

Example strings: "listen" and "silent"

LEFT panel ("Через sorted()") — teal:
Step 1: "listen" → lower() → sorted() → ['e','i','l','n','s','t']
Step 2: "silent" → lower() → sorted() → ['e','i','l','n','s','t']
Step 3: == comparison → True ✓ (green glow)

Show the sorted letter sequences as inventory slots with individual letters, both sequences align perfectly.

Code in monospace:
sorted("listen") == sorted("silent")  →  True

RIGHT panel ("Через dict-подсчёт") — indigo:
"listen": {l:1, i:1, s:1, t:1, e:1, n:1} → shown as small count badges on letters.
"silent": same counts.
compare counts → all zeros → True ✓

Code in monospace:
count[ch] += 1 ... count[ch] -= 1
all(v == 0 for v in count.values())  →  True

Bottom: "O(n log n) через sorted() vs O(n) через dict"

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

<details>
<summary>Решение через dict (подсчёт букв)</summary>

```python
def is_anagram(s1, s2):
    clean1 = s1.lower().replace(" ", "")
    clean2 = s2.lower().replace(" ", "")
    if len(clean1) != len(clean2):
        return False

    count = {}
    for ch in clean1:
        count[ch] = count.get(ch, 0) + 1  # считаем буквы первой строки
    for ch in clean2:
        count[ch] = count.get(ch, 0) - 1  # вычитаем буквы второй строки

    return all(v == 0 for v in count.values())  # все счётчики должны быть 0

print(is_anagram("listen", "silent"))           # → True
print(is_anagram("hello", "world"))             # → False
```

</details>

---

## Задача 2 — Поиск дубликатов (10 мин)

Дан список элементов. Найди все элементы, которые встречаются **более одного раза**. Верни их список (порядок не важен).

```python
print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))   # → [2, 3]
print(find_duplicates(["a", "b", "a", "c"]))     # → ["a"]
print(find_duplicates([1, 2, 3]))                # → []
print(find_duplicates([7, 7, 7, 7]))             # → [7]
```

<details>
<summary>Подсказка — способ 1: через set</summary>

Используй два множества: `seen` — то, что уже видели, `duplicates` — то, что встретили второй раз.

</details>

<details>
<summary>Решение через set</summary>

```python
def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))  # → [2, 3]
print(find_duplicates(["a", "b", "a", "c"]))   # → ['a']
print(find_duplicates([1, 2, 3]))              # → []
```

</details>

<details>
<summary>Решение через dict (с подсчётом)</summary>

```python
def find_duplicates(lst):
    count = {}
    for item in lst:
        count[item] = count.get(item, 0) + 1
    return [item for item, n in count.items() if n > 1]

print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))  # → [2, 3]
print(find_duplicates([7, 7, 7, 7]))            # → [7]
```

</details>

---

## Задача 3 — Топ-N популярных (15 мин)

Дан список элементов (например, названия предметов из инвентаря). Найди **N самых часто встречающихся** элементов. Верни список пар `(элемент, количество)`, отсортированный по убыванию частоты.

```python
inventory = [
    "меч", "щит", "зелье", "меч", "лук",
    "зелье", "меч", "щит", "зелье", "зелье"
]

print(top_n(inventory, 2))
# → [("зелье", 4), ("меч", 3)]

print(top_n(inventory, 3))
# → [("зелье", 4), ("меч", 3), ("щит", 2)]
```

<details>
<summary>Подсказка</summary>

Сначала посчитай частоту каждого элемента через `dict`. Потом отсортируй пары `(элемент, частота)` по частоте — используй `sorted()` с `key=`.

</details>

<details>
<summary>Решение</summary>

```python
def top_n(lst, n):
    count = {}
    for item in lst:
        count[item] = count.get(item, 0) + 1

    # Сортируем по количеству по убыванию
    sorted_items = sorted(count.items(), key=lambda pair: pair[1], reverse=True)
    return sorted_items[:n]

inventory = [
    "меч", "щит", "зелье", "меч", "лук",
    "зелье", "меч", "щит", "зелье", "зелье"
]

print(top_n(inventory, 2))  # → [('зелье', 4), ('меч', 3)]
print(top_n(inventory, 3))  # → [('зелье', 4), ('меч', 3), ('щит', 2)]
```

</details>

---

## Задача 4 — Бинарный поиск: первый True (15 мин)

Дан список булевых значений вида `[False, False, False, True, True, True]` — все `False` идут до всех `True`. Найди **индекс первого `True`** с помощью бинарного поиска. Если `True` нет — вернуть `-1`.

Почему бинарный? Линейный поиск — O(n). Бинарный — O(log n). Для списка из миллиона элементов: 1 000 000 шагов vs 20 шагов.

```python
flags = [False, False, False, True, True, True, True]
print(first_true(flags))          # → 3

flags2 = [True, True, True]
print(first_true(flags2))         # → 0

flags3 = [False, False, False]
print(first_true(flags3))         # → -1

flags4 = [False, True]
print(first_true(flags4))         # → 1
```

<details>
<summary>Подсказка</summary>

Классический бинарный поиск: `left=0`, `right=len-1`, `mid=(left+right)//2`. Если `lst[mid]` — True: запомни этот индекс как кандидата и ищи левее (может быть ещё один True раньше). Если False — ищи правее.

</details>

<details>
<summary>Решение</summary>

```python
def first_true(lst):
    left = 0
    right = len(lst) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if lst[mid]:
            result = mid        # нашли True — запоминаем, ищем левее
            right = mid - 1
        else:
            left = mid + 1      # False — ищем правее

    return result

flags = [False, False, False, True, True, True, True]
print(first_true(flags))   # → 3

flags2 = [True, True, True]
print(first_true(flags2))  # → 0

flags3 = [False, False, False]
print(first_true(flags3))  # → -1

flags4 = [False, True]
print(first_true(flags4))  # → 1
```

</details>

---

## Задача 5 — Мини-проект: система рейтинга игроков (20 мин)

Создай систему управления рейтингом игроков. Требования:

1. **Добавление игрока:** `add_player(name, score)` — добавить или обновить очки
2. **Топ-N:** `get_top(n)` — вернуть N лучших игроков (список пар `(имя, очки)`)
3. **Поиск по имени:** `search_player(name)` — бинарный поиск по отсортированному списку имён (O(log n)). Вернуть очки или `None`
4. **Общая статистика:** `stats()` — вывести: количество игроков, средний счёт, макс. счёт

```python
lb = Leaderboard()
lb.add_player("Arthas", 1500)
lb.add_player("Thrall", 2200)
lb.add_player("Sylvanas", 1800)
lb.add_player("Jaina", 3000)
lb.add_player("Arthas", 1700)  # обновляем Артаса

print(lb.get_top(3))
# → [("Jaina", 3000), ("Thrall", 2200), ("Sylvanas", 1800)]

print(lb.search_player("Thrall"))   # → 2200
print(lb.search_player("Garrosh"))  # → None

lb.stats()
# Игроков: 4 | Средний счёт: 2175 | Лучший: Jaina (3000)
```

<details>
<summary>Подсказка по бинарному поиску по имени</summary>

Для бинарного поиска список имён должен быть **отсортирован**. Строки сравниваются лексикографически: `"Arthas" < "Jaina" < "Sylvanas" < "Thrall"`. Алгоритм тот же, что для чисел.

</details>

<details>
<summary>Полное решение</summary>

```python
class Leaderboard:
    def __init__(self):
        self._players = {}  # {name: score}

    def add_player(self, name, score):
        self._players[name] = score
        print(f"  {name}: {score} очков")

    def get_top(self, n):
        sorted_players = sorted(
            self._players.items(),
            key=lambda pair: pair[1],
            reverse=True
        )
        return sorted_players[:n]

    def search_player(self, name):
        """Бинарный поиск по отсортированному списку имён."""
        names = sorted(self._players.keys())
        left, right = 0, len(names) - 1

        while left <= right:
            mid = (left + right) // 2
            if names[mid] == name:
                return self._players[name]
            elif names[mid] < name:
                left = mid + 1
            else:
                right = mid - 1
        return None

    def stats(self):
        if not self._players:
            print("Таблица пуста")
            return
        scores = list(self._players.values())
        avg = sum(scores) // len(scores)
        best_name = max(self._players, key=lambda n: self._players[n])
        best_score = self._players[best_name]
        print(f"Игроков: {len(scores)} | Средний счёт: {avg} | "
              f"Лучший: {best_name} ({best_score})")


# Тест:
lb = Leaderboard()
lb.add_player("Arthas", 1500)
lb.add_player("Thrall", 2200)
lb.add_player("Sylvanas", 1800)
lb.add_player("Jaina", 3000)
lb.add_player("Arthas", 1700)

print(lb.get_top(3))
# → [('Jaina', 3000), ('Thrall', 2200), ('Sylvanas', 1800)]

print(lb.search_player("Thrall"))    # → 2200
print(lb.search_player("Garrosh"))  # → None

lb.stats()
# → Игроков: 4 | Средний счёт: 2175 | Лучший: Jaina (3000)
```

</details>

<!--illustration
file: day_6/day_6_leaderboard_system.png
alt: Архитектура класса Leaderboard — add_player, get_top, search_player, stats
prompt:
Create a Dark RPG UI infographic showing the Leaderboard class architecture.

Title: "LEADERBOARD: АРХИТЕКТУРА" in cream (#e8e0d4).

Central: a large dark glass panel labeled "class Leaderboard" with RPG castle/fortress icon.

Inside, four operation nodes connected by organic glowing lines:

Node 1 (teal): "add_player(name, score)"
→ arrow to dict icon: "_players = {name: score}"
Label: "O(1) — добавить/обновить"

Node 2 (amber): "get_top(n)"
→ arrow to sorted() icon: "sorted() по очкам"
Label: "O(n log n) — топ-N"

Node 3 (indigo): "search_player(name)"
→ arrow to binary search icon: "sorted(names) → bisect"
Label: "O(log n) — бинарный поиск"

Node 4 (green): "stats()"
→ arrow to stats panel: "len, avg, max"
Label: "O(n) — статистика"

Bottom example card:
lb.get_top(3) → [("Jaina", 3000), ("Thrall", 2200), ("Sylvanas", 1800)]

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

## Итог дня

Сегодня ты применил:

| Задача | Инструмент | Сложность |
|--------|-----------|-----------|
| Анаграммы | `sorted()` или `dict` | O(n log n) / O(n) |
| Дубликаты | `set` или `dict` | O(n) |
| Топ-N | `dict` + `sorted()` | O(n log n) |
| Первый True | Бинарный поиск | O(log n) |
| Рейтинг | Всё вместе + ООП | — |

**Алгоритмы — это не магия.** Это просто умные способы организовать перебор. Понимание структур данных (список, множество, словарь) и базовых алгоритмов (поиск, сортировка) решает 90% задач в реальном коде.

---

← [Day 5 — Жадные алгоритмы](day_5.md) | [Day 7 — Лонгрид →](day_7.md)
