---
type: lesson
course: "[[python_basics/README]]"
week: 8
day: 4
title: "Рекурсия — функция, которая вызывает себя"
concepts: [рекурсия, базовый случай, стек вызовов, когда не использовать рекурсию]
prerequisites: "[\"[[week_8/day_3]]\"]"
tags: [python, алгоритмы, рекурсия, стек, fibonacci]
status: draft
---

# Day 4: Рекурсия — функция, которая вызывает себя

> **Сегодня:** узнаем, как функция может вызывать саму себя — и почему это иногда красиво, а иногда опасно
> **Время:** ~45 минут

---

## Часть 1 — Зеркало напротив зеркала

Представь: ты стоишь между двумя зеркалами, направленными друг на друга. В каждом отражении видно следующее отражение, в том — ещё одно, и так до бесконечности.

Это **бесконечная рекурсия** — функция вызывает себя без конца.

Но если добавить условие «стоп» — например, зеркало постепенно тускнеет, и на 10-м отражении исчезает — получается **конечная рекурсия**. Именно так работает правильный рекурсивный алгоритм.

**Рекурсия** — это когда функция вызывает саму себя внутри своего тела.

```python
def зеркало(n):
    if n == 0:          # условие остановки
        print("Темнота")
        return
    print(f"Отражение {n}")
    зеркало(n - 1)      # вызываем себя с меньшим n

зеркало(3)
# Отражение 3
# Отражение 2
# Отражение 1
# Темнота
```

Каждый шаг приближает нас к концу. Без этого — крах.

---

## Часть 2 — Факториал: итеративно vs рекурсивно

Факториал числа n (пишется n!) — это произведение всех чисел от 1 до n.

```
5! = 5 × 4 × 3 × 2 × 1 = 120
```

**Итеративный подход** — через цикл:

```python
def factorial_loop(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(factorial_loop(5))  # → 120
```

**Рекурсивный подход** — функция вызывает себя:

```python
def factorial(n):
    if n == 0:              # базовый случай
        return 1
    return n * factorial(n - 1)  # рекурсивный вызов

print(factorial(5))  # → 120
```

Почему это работает? Посмотрим на **стек вызовов** — цепочку, которую Python строит:

```
factorial(5)
  └─ 5 * factorial(4)
          └─ 4 * factorial(3)
                  └─ 3 * factorial(2)
                          └─ 2 * factorial(1)
                                  └─ 1 * factorial(0)
                                          └─ 1  ← базовый случай
```

Python запоминает каждый вызов в стеке. Когда доходит до дна (базовый случай), начинает «разматывать» обратно: `1 → 1×1=1 → 2×1=2 → 3×2=6 → 4×6=24 → 5×24=120`.

> **Стек вызовов** — это очередь незавершённых вызовов функции. Каждый новый вызов кладётся сверху. Когда функция завершается — снимается сверху.

<!--illustration
file: day_4/day_4_call_stack.png
alt: Стек вызовов для factorial(4) — накопление и разматывание с возвращёнными значениями
prompt:
Create a Dark RPG UI infographic showing the call stack for factorial(4).

Title: "СТЕК ВЫЗОВОВ: factorial(4)" in cream (#e8e0d4). Subtitle: "как Python запоминает каждый вызов" in gray-blue.

Two phases shown side by side:

LEFT phase ("Стек накапливается") — building up:
A vertical stack of dark glass frames, like Hollow Knight soul vessels stacking:
- Bottom: factorial(0) → 1 (base case, green glow)
- factorial(1) → 1 × factorial(0)
- factorial(2) → 2 × factorial(1)
- factorial(3) → 3 × factorial(2)
- Top: factorial(4) → 4 × factorial(3)
Stack grows UPWARD with each frame layered on previous. Amber glow increases toward top.

Arrow pointing right: "разматываем обратно →"

RIGHT phase ("Стек разматывается") — unwinding:
Same stack collapsing downward with return values flowing back:
- factorial(0) returns 1 (green)
- factorial(1) returns 1×1 = 1
- factorial(2) returns 2×1 = 2
- factorial(3) returns 3×2 = 6
- factorial(4) returns 4×6 = 24 (teal glow at top, final answer)

Bottom result card: "Результат: 24" in green (#7bc88f).

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

## Часть 3 — Базовый случай: без него всё рухнет

**Базовый случай** — это условие, при котором рекурсия останавливается. Это самое важное в рекурсивной функции.

Что будет без него:

```python
def broken(n):
    return n * broken(n - 1)  # нет базового случая!

broken(5)  # RecursionError: maximum recursion depth exceeded
```

Python упадёт с `RecursionError`. Стек вызовов переполнится — функция вызвала себя слишком много раз (по умолчанию лимит ~1000).

**Правило:** каждый рекурсивный вызов должен делать задачу **меньше** и приближать к базовому случаю.

```python
def factorial(n):
    # БАЗОВЫЙ СЛУЧАЙ — обязателен!
    if n == 0:
        return 1
    # Рекурсивный шаг: n уменьшается → движемся к базовому случаю
    return n * factorial(n - 1)
```

<!--illustration
file: day_4/day_4_base_case_danger.png
alt: Рекурсия без базового случая — RecursionError, и с базовым случаем — чистый результат
prompt:
Create a Dark RPG UI infographic showing recursion with vs without base case.

Title: "БАЗОВЫЙ СЛУЧАЙ — ОБЯЗАТЕЛЕН" in cream (#e8e0d4).

Two panels:

LEFT panel ("Без базового случая") — dim, cracked, red-amber tint:
Code at top:
def broken(n):
    return n * broken(n-1)  # нет базового!
in dim monospace with red-amber tint.

Below: a chain of calls going down endlessly:
broken(5) → broken(4) → broken(3) → broken(2) → ... → ∞
Arrow keeps going past panel edge.

Bottom: cracked glass with skull icon and:
"RecursionError: maximum recursion depth exceeded"
in red-amber. Crack effects, danger glow.

RIGHT panel ("С базовым случаем") — clean, teal glow:
Code at top:
def factorial(n):
    if n == 0:      # базовый случай!
        return 1
    return n * factorial(n-1)
"if n == 0" line highlighted in green.

Below: chain of calls that STOPS:
factorial(3) → factorial(2) → factorial(1) → factorial(0) → 1 ✓
A clean stop marker at factorial(0) with green glow.

Bottom: green check panel: "Чисто. Правильно. Работает."

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

## Часть 4 — Сумма цифр числа: рекурсия в красоте

Посмотри, как элегантно рекурсия решает задачу суммы цифр числа.

**Итеративно:**

```python
def digit_sum_loop(n):
    total = 0
    while n > 0:
        total += n % 10   # последняя цифра
        n //= 10          # отбрасываем последнюю цифру
    return total

print(digit_sum_loop(1234))  # → 10
```

**Рекурсивно:**

```python
def digit_sum(n):
    if n < 10:              # однозначное число — базовый случай
        return n
    return n % 10 + digit_sum(n // 10)  # последняя цифра + сумма остальных

print(digit_sum(1234))  # → 10
```

Прочитай вслух: «сумма цифр числа 1234 = последняя цифра (4) + сумма цифр числа 123». Звучит как определение! Рекурсия — это когда решение выражается через себя, но для меньшей задачи.

Трассировка:
```
digit_sum(1234)
  → 4 + digit_sum(123)
         → 3 + digit_sum(12)
                → 2 + digit_sum(1)
                       → 1  ← базовый случай
```

---

## Часть 5 — Фибоначчи: когда рекурсия становится врагом

Числа Фибоначчи: 0, 1, 1, 2, 3, 5, 8, 13, 21...
Каждое число = сумма двух предыдущих.

**Наивная рекурсия:**

```python
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

print(fib_naive(10))  # → 55
print(fib_naive(35))  # → 9227465 (медленно, ждём секунды)
```

Почему медленно? Посмотри на стек для `fib(5)`:

```
fib(5)
├─ fib(4)
│   ├─ fib(3)
│   │   ├─ fib(2) ...
│   │   └─ fib(1)
│   └─ fib(2) ...  ← считается снова!
└─ fib(3)           ← считается снова!
    ├─ fib(2) ...   ← считается снова!
    └─ fib(1)
```

`fib(3)` вычисляется дважды, `fib(2)` — трижды. Это **O(2^n)** — катастрофа.

**Итеративно — O(n):**

```python
def fib_fast(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

print(fib_fast(10))   # → 55
print(fib_fast(100))  # → 354224848179261915075 (мгновенно!)
```

**Вывод:** рекурсия — не всегда лучший инструмент. Фибоначчи — классический пример, где итерация побеждает.

<!--illustration
file: day_4/day_4_recursive_vs_iterative.png
alt: Сравнение рекурсивного Фибоначчи O(2^n) с деревом повторных вызовов и итеративного O(n)
prompt:
Create a Dark RPG UI infographic comparing naive recursive Fibonacci vs iterative Fibonacci.

Title: "ФИБОНАЧЧИ: РЕКУРСИЯ VS ИТЕРАЦИЯ" in cream (#e8e0d4).

LEFT panel ("Рекурсивный O(2^n)") — dim amber, warning:
A tree showing fib(5) recursive calls:
fib(5) branches into fib(4) and fib(3).
fib(4) branches into fib(3) and fib(2).
fib(3) branches twice, etc.
Show duplicated calls in red-amber: fib(3) appears TWICE (circled), fib(2) THREE TIMES.
The tree fans out exponentially, showing the explosion of calls.
Badge: "fib(10) = 177 вызовов" in amber.
Bottom: "Медленно. Перевычисляет снова и снова."

RIGHT panel ("Итеративный O(n)") — teal, clean:
A simple left-to-right sequence:
a=0, b=1 → a=1, b=1 → a=1, b=2 → a=2, b=3 → a=3, b=5 → ...→ 55
Each step is one glass bead on a string. Linear, clean.
Badge: "fib(10) = 9 шагов" in green.
Bottom: "Быстро. Каждое число вычисляется один раз."

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

<quiz>
question: "Что вернёт `fib_naive(6)`? (0,1,1,2,3,5,8...)"
options:
  - "5"
  - "8"
  - "13"
  - "3"
answer: 1
explanation: "fib(6) = fib(5) + fib(4) = 5 + 3 = 8. Последовательность: 0,1,1,2,3,5,8 — шестой элемент (с нуля) равен 8."
</quiz>

---

## Часть 6 — Камень: Python ограничивает рекурсию

Python не даёт рекурсии уйти в бесконечность — стек вызовов ограничен по умолчанию **~1000 уровнями**.

```python
def deep(n):
    return deep(n + 1)

deep(0)  # RecursionError: maximum recursion depth exceeded
```

Можно узнать лимит и даже поменять — но лучше не надо:

```python
import sys
print(sys.getrecursionlimit())  # → 1000 (обычно)
# sys.setrecursionlimit(10000)  # можно, но опасно — крашит интерпретатор
```

**Когда НЕ использовать рекурсию:**
- Задача требует больше ~500-900 уровней вложенности
- Есть повторные вычисления (как в наивном Фибоначчи)
- Производительность критична

**Когда рекурсия хороша:**
- Задача естественно делится на подзадачи того же типа
- Глубина невелика
- Код с рекурсией читается значительно проще

> **Игровой контекст:** в Dwarf Fortress генерация пещер работает рекурсивно: «создай комнату → добавь коридоры → для каждого коридора создай комнату → ...» — это BSP-дерево. В Dark Souls AI поиска пути тоже использует рекурсивный обход графа локаций.

---

## Итог дня

| Концепция | Суть |
|-----------|------|
| Рекурсия | Функция вызывает саму себя |
| Базовый случай | Условие остановки — обязателен! |
| Стек вызовов | Python запоминает каждый незавершённый вызов |
| Когда не использовать | Большая глубина, повторные вычисления, производительность |

**Три закона рекурсии:**
1. У рекурсивной функции есть базовый случай
2. Каждый рекурсивный вызов приближает к базовому случаю
3. Рекурсивный вызов решает задачу меньшего размера

---

## Задание 1 — Степень числа (10 мин)

Напиши рекурсивную функцию `power(base, exp)`, которая вычисляет `base ** exp` без использования оператора `**`.

```python
# Что должно работать:
print(power(2, 10))  # → 1024
print(power(3, 4))   # → 81
print(power(5, 0))   # → 1  (любое число в степени 0 = 1)
```

<details>
<summary>Подсказка</summary>

`2^10 = 2 * 2^9`. Базовый случай: `base^0 = 1`.

</details>

<details>
<summary>Решение</summary>

```python
def power(base, exp):
    if exp == 0:          # базовый случай: x^0 = 1
        return 1
    return base * power(base, exp - 1)  # x^n = x * x^(n-1)

print(power(2, 10))  # → 1024
print(power(3, 4))   # → 81
print(power(5, 0))   # → 1
```

</details>

---

## Задание 2 — Обратный отсчёт (8 мин)

Напиши рекурсивную функцию `countdown(n)`, которая выводит числа от n до 0, а потом «Поехали!».

```python
countdown(5)
# 5
# 4
# 3
# 2
# 1
# 0
# Поехали!
```

<details>
<summary>Решение</summary>

```python
def countdown(n):
    if n < 0:
        print("Поехали!")
        return
    print(n)
    countdown(n - 1)

countdown(5)
```

</details>

---

## Задание 3 — Палиндром рекурсивно (12 мин)

Напиши рекурсивную функцию `is_palindrome(s)`, которая проверяет, является ли строка палиндромом (читается одинаково в обе стороны).

```python
print(is_palindrome("racecar"))  # → True
print(is_palindrome("madam"))    # → True
print(is_palindrome("hello"))    # → False
print(is_palindrome("a"))        # → True
```

<details>
<summary>Подсказка</summary>

Строка — палиндром, если первый и последний символы совпадают, И оставшаяся средняя часть тоже палиндром. Базовый случай: строка длиной 0 или 1 — всегда палиндром.

</details>

<details>
<summary>Решение</summary>

```python
def is_palindrome(s):
    if len(s) <= 1:                   # базовый случай
        return True
    if s[0] != s[-1]:                 # крайние символы не совпадают
        return False
    return is_palindrome(s[1:-1])     # проверяем середину

print(is_palindrome("racecar"))  # → True
print(is_palindrome("madam"))    # → True
print(is_palindrome("hello"))    # → False
print(is_palindrome("a"))        # → True
```

</details>

---

## Задание 4 — Найди максимум (12 мин)

Напиши рекурсивную функцию `find_max(lst)`, которая находит максимальный элемент списка.

```python
print(find_max([3, 1, 7, 2, 9, 4]))  # → 9
print(find_max([42]))                 # → 42
print(find_max([-5, -1, -3]))         # → -1
```

<details>
<summary>Подсказка</summary>

Максимум списка = max(первый элемент, максимум остального списка). Базовый случай: список из одного элемента.

</details>

<details>
<summary>Решение</summary>

```python
def find_max(lst):
    if len(lst) == 1:               # базовый случай
        return lst[0]
    rest_max = find_max(lst[1:])    # максимум оставшейся части
    if lst[0] > rest_max:
        return lst[0]
    return rest_max

print(find_max([3, 1, 7, 2, 9, 4]))  # → 9
print(find_max([42]))                 # → 42
print(find_max([-5, -1, -3]))         # → -1
```

</details>

---

<!--illustration
file: day_4/day_4_skill_tree.png
alt: Дерево навыков дня 4 — рекурсия, базовый случай, стек вызовов, ограничение ~1000
prompt:
Create a Dark RPG UI skill tree infographic for Day 4 summary.

Title: "НАВЫКИ ДНЯ 4" in cream (#e8e0d4). Subtitle: "Рекурсия" in gray-blue (#8ea4b8).

A branching skill tree:

Root node (teal glow): infinity/mirror icon — "Рекурсия"

Branching:
- Node 1 (green): stop-sign icon — "Базовый случай" — "обязателен!"
- Node 2 (teal): stack icon — "Стек вызовов" — "Python запоминает каждый вызов"
- Node 3 (amber): warning icon — "Ограничение ~1000 уровней"

Connecting: organic vines. The base case node is brightest — it's the most critical concept.

Bottom glass checklist:
✓ Рекурсия
✓ Базовый случай
✓ Стек вызовов
✓ Ограничение Python ~1000

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

← [Day 3 — Сортировка](day_3.md) | [Day 5 — Жадные алгоритмы →](day_5.md)
