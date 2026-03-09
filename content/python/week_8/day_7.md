---
type: lesson
course: "python"
week: 8
day: 7
title: "Лонгрид — Алгоритмы вокруг нас: TikTok и GPS"
concepts: []
prerequisites: "[\"[week_8/day_6](/python/week_8/day_6/)\"]"
tags: [python, алгоритмы, tiktok, gps, рекомендации, дейкстра, лонгрид]
status: draft
---

# Day 7: Алгоритмы вокруг нас — TikTok и GPS

> **Сегодня:** никакого нового кода. Только две большие истории о том, как алгоритмы, которые ты изучил, управляют реальным миром
> **Время:** ~60 минут

---

Ты провёл неделю, изучая алгоритмы: Big O, поиск, сортировку, рекурсию, жадные стратегии, мемоизацию. Это было абстрактно. Сегодня — конкретно.

Два самых используемых тобой приложения прямо сейчас: TikTok и карты (Google Maps, Яндекс). Оба работают на алгоритмах. Посмотрим внутрь.

---

## История 1: TikTok — алгоритм, который знает тебя лучше мамы

### Как работает ForYou Page

Ты открываешь TikTok. Первое видео — какой-то ролик. Ты досматриваешь до конца. Второе — скипаешь на третьей секунде. Третье — лайкаешь и смотришь дважды.

TikTok видит всё это. И после 20 минут уже знает, что ты любишь. После часа — знает лучше, чем ты сам.

Многие думают, что ForYou Page строится на лайках. На самом деле лайки — слабый сигнал. TikTok использует гораздо более тонкие данные:

| Сигнал | Вес | Почему |
|--------|-----|--------|
| **Completion rate** (досмотрел ли до конца) | Очень высокий | Трудно обмануть — если досмотрел, значит понравилось |
| **Rewatch** (пересмотрел) | Максимальный | Пересматривают только то, что реально цепляет |
| **Shares** (поделился) | Высокий | Публичное действие — большой сигнал интереса |
| **Comments** | Высокий | Особенно негативные — они тоже удерживают внимание |
| **Лайки** | Средний | Легко нажать случайно |
| **Follows** | Средний | Автор понравился, но не конкретное видео |
| **Скорость скипа** | Отрицательный | Если скипнул на 1-й секунде — видео не понравилось |

TikTok строит для каждого пользователя **вектор интересов** — набор числовых характеристик, описывающих его вкусы. У каждого видео тоже есть вектор. Алгоритм ищет совпадение.

### Коллаборативная фильтрация

Главная магия называется **коллаборативная фильтрация**: «если ты похож на другого пользователя, тебе понравится то, что понравилось ему».

Представь упрощённую таблицу оценок (0 = не смотрел, 1-5 = рейтинг):

```
          Видео A  Видео B  Видео C  Видео D
Алексей:     5        3        0        4
Борис:       4        0        1        5
Виктор:      0        4        5        0
Геннадий:    5        3        0        ?   ← что показать?
```

Геннадий похож на Алексея: оба любят A и B, оба не смотрели C. Алексей оценил D на 4. Значит, D — хороший кандидат для Геннадия.

Вот упрощённая реализация на Python:

```python
def similarity(user1_scores, user2_scores):
    """Косинусное сходство между двумя пользователями."""
    common_videos = [v for v in user1_scores if v in user2_scores]
    if not common_videos:
        return 0

    dot_product = sum(
        user1_scores[v] * user2_scores[v] for v in common_videos
    )
    norm1 = sum(user1_scores[v] ** 2 for v in user1_scores) ** 0.5
    norm2 = sum(user2_scores[v] ** 2 for v in user2_scores) ** 0.5

    if norm1 == 0 or norm2 == 0:
        return 0
    return dot_product / (norm1 * norm2)


def recommend(users, target_user, n=3):
    """Найти похожего пользователя и порекомендовать его видео."""
    target_scores = users[target_user]
    best_match = None
    best_score = -1

    for user, scores in users.items():
        if user == target_user:
            continue
        sim = similarity(target_scores, scores)
        if sim > best_score:
            best_score = sim
            best_match = user

    # Видео, которые похожий пользователь смотрел, а target — нет
    seen = set(target_scores.keys())
    candidates = {
        v: s for v, s in users[best_match].items()
        if v not in seen
    }
    recommendations = sorted(candidates, key=lambda v: candidates[v], reverse=True)
    return recommendations[:n], best_match


# Простая модель:
users = {
    "Алексей":  {"A": 5, "B": 3, "D": 4},
    "Борис":    {"A": 4, "C": 1, "D": 5},
    "Виктор":   {"B": 4, "C": 5},
    "Геннадий": {"A": 5, "B": 3},
}

recs, match = recommend(users, "Геннадий")
print(f"Похожий пользователь: {match}")   # → Алексей
print(f"Рекомендации: {recs}")            # → ['D']
```

Конечно, настоящий TikTok работает с миллиардами пользователей и тысячами параметров. Но принцип тот же.

<!--illustration
file: day_7/day_7_tiktok_algorithm.png
alt: Матрица коллаборативной фильтрации TikTok — пользователи, видео, оценки, рекомендация
prompt:
Create a Dark RPG UI infographic showing TikTok's collaborative filtering as a matrix.

Title: "TIKTOK: КОЛЛАБОРАТИВНАЯ ФИЛЬТРАЦИЯ" in cream (#e8e0d4). Subtitle: "похожие пользователи → похожие вкусы" in gray-blue.

Central: a grid/matrix:
- Y-axis (rows): user names — "Алексей", "Борис", "Виктор", "Геннадий"
- X-axis (columns): "Видео A", "Видео B", "Видео C", "Видео D"

Cells filled with colored scores (0-5):
- Алексей: A=5(green), B=3(teal), -(grey), D=4(amber)
- Борис: A=4(green), -(grey), C=1(dim), D=5(green)
- Виктор: -(grey), B=4(teal), C=5(green), -(grey)
- Геннадий: A=5(green), B=3(teal), -(grey), D=?(amber question mark)

"Геннадий" row glows slightly. A similarity bracket connects "Геннадий" and "Алексей" rows on the left side with label "похожи!".

A recommendation arrow: from "Алексей's D=4" → to Геннадий's D cell → "покажем Геннадию Видео D!"
Arrow in teal, glowing.

Bottom info card: "log₂(схожесть) → рекомендация"

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

### Факт, который заставит задуматься

В 2021 году исследователи MIT обнаружили: алгоритм TikTok способен определить политические взгляды пользователя с точностью выше 70% — просто по паттернам просмотра, без единого политического видео в истории. Аналогично — сексуальная ориентация, состояние здоровья, финансовое положение.

Ты никогда не говоришь TikTok: «Я интересуюсь этим». Ты просто смотришь. А алгоритм слушает.

### A/B тестирование: как TikTok знает, что новый алгоритм лучше

Когда инженеры TikTok меняют алгоритм, они не выкатывают изменения сразу всем. Они делают **A/B тест**:

- Группа A (50% пользователей): старый алгоритм
- Группа B (50% пользователей): новый алгоритм

Через неделю смотрят на метрики: среднее время в приложении, количество открытых видео, retention (вернулись ли завтра). Если у группы B метрики лучше — новый алгоритм побеждает.

Это не магия. Это статистика + огромное количество данных. Каждый день TikTok запускает сотни таких тестов одновременно.

---

## История 2: GPS — как телефон знает кратчайший путь

### Граф дорог

Когда ты просишь Google Maps проложить маршрут из точки A в точку B, у алгоритма есть карта — но не в виде картинки. В виде **графа**.

- **Вершины** = перекрёстки и точки (твой дом, кафе, школа)
- **Рёбра** = дороги между ними
- **Вес ребра** = время или расстояние до следующей точки

```
     [А] ──5── [Б] ──3── [В]
      |                   |
      8                   2
      |                   |
     [Г] ──────6────── [Д]
```

Задача: найти кратчайший путь от А до Д.

На глаз: А→Б→В→Д = 5+3+2 = 10. Или А→Г→Д = 8+6 = 14. Первый короче. Но в реальности граф из миллионов вершин — на глаз не решишь.

### Алгоритм Дейкстры простыми словами

Эдсгер Дейкстра придумал этот алгоритм в 1956 году — за 20 минут, сидя в кафе. Без бумаги и карандаша, «в уме».

Идея — жадная:
1. Начинаем от старта. Расстояние до него = 0, до всех остальных = бесконечность.
2. Берём непосещённую вершину с наименьшим известным расстоянием.
3. Для каждого соседа: если путь через текущую вершину короче известного — обновляем.
4. Помечаем вершину как посещённую. Повторяем.

```python
def dijkstra(graph, start):
    """
    graph = {"А": {"Б": 5, "Г": 8}, "Б": {"В": 3}, ...}
    Возвращает словарь кратчайших расстояний от start до всех вершин.
    """
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    visited = set()

    while True:
        # Берём непосещённую вершину с минимальным расстоянием
        current = None
        for node in distances:
            if node not in visited:
                if current is None or distances[node] < distances[current]:
                    current = node

        if current is None:             # все посещены
            break
        if distances[current] == float("inf"):  # недостижимые вершины
            break

        visited.add(current)

        for neighbor, weight in graph[current].items():
            new_dist = distances[current] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                print(f"  Обновляем {neighbor}: {new_dist}")

    return distances


# Граф из примера выше:
graph = {
    "А": {"Б": 5, "Г": 8},
    "Б": {"А": 5, "В": 3},
    "В": {"Б": 3, "Д": 2},
    "Г": {"А": 8, "Д": 6},
    "Д": {"В": 2, "Г": 6},
}

distances = dijkstra(graph, "А")
print(distances)
# → {'А': 0, 'Б': 5, 'В': 8, 'Г': 8, 'Д': 10}
# Кратчайший путь А→Д: 10 (через А→Б→В→Д)
```

<!--illustration
file: day_7/day_7_dijkstra_graph.png
alt: Алгоритм Дейкстры на графе из 5 вершин — кратчайший путь А→Д выделен цветом
prompt:
Create a Dark RPG UI infographic showing Dijkstra's algorithm on a city graph.

Title: "АЛГОРИТМ ДЕЙКСТРЫ: КРАТЧАЙШИЙ ПУТЬ" in cream (#e8e0d4). Subtitle: "жадная стратегия для поиска пути" in gray-blue.

A graph with 5 nodes (А, Б, В, Г, Д) arranged naturally (not in a straight line):
- Weighted edges shown as glowing lines with weight labels: А-Б=5, А-Г=8, Б-В=3, В-Д=2, Г-Д=6
- Node А: start node, bright teal glow, labeled "СТАРТ"
- Node Д: destination, soft amber glow, labeled "ЦЕЛЬ"

Visited nodes (А, Б, В, Г): shown as dimmed/greyed out orbs — already processed.
Final shortest path А→Б→В→Д highlighted in bright teal: the path glows and the weights sum: 5+3+2=10.

Distance labels shown next to each node (final shortest distances):
А: 0, Б: 5, В: 8, Г: 8, Д: 10

The longer path А→Г→Д=14 shown as dim red-amber — not the shortest, crossed out.

Bottom glass card: "Кратчайший путь А→Д: 10 (через Б и В)"

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

Трассировка работы алгоритма для нашего графа:

```
Старт: А = 0, остальные = ∞

Шаг 1: Берём А (расстояние 0)
  Обновляем Б: 0+5 = 5
  Обновляем Г: 0+8 = 8

Шаг 2: Берём Б (расстояние 5, наименьшее из непосещённых)
  Обновляем В: 5+3 = 8

Шаг 3: Берём В и Г (оба 8, выберем В)
  Обновляем Д: 8+2 = 10

Шаг 4: Берём Г (расстояние 8)
  Можно обновить Д через Г: 8+6 = 14 > 10. Не обновляем.

Шаг 5: Берём Д (расстояние 10). Готово!
```

### Почему GPS сложнее

Реальная карта Google Maps — это граф из **миллиардов вершин**. Дейкстра на нём был бы слишком медленным. Поэтому GPS-приложения используют **A\*** (читается «A star») — улучшенный алгоритм с эвристикой.

Эвристика — это умная подсказка. В A\* она говорит: «не ходи в стороны от цели, ищи в направлении пункта назначения». Это сильно сокращает число вершин для проверки.

Кроме того, Google Maps учитывает:
- **Пробки в реальном времени** — веса рёбер меняются каждую минуту
- **Тип дороги** — шоссе vs просёлочная дорога
- **Режим движения** — пешком, машина, велосипед
- **Запрещённые повороты** — нельзя повернуть налево в конкретном месте

> **Факт:** Google Maps пересчитывает 25 миллионов маршрутов в секунду. Для этого используются не просто алгоритмы, но и специальное железо — кластеры серверов, распределённые вычисления, предварительно сжатые иерархии дорог.

---

## Эпилог: алгоритмы везде

TikTok и GPS — только два примера. Вот несколько других мест, где живут знакомые тебе алгоритмы:

**Spotify — «Похожие треки»**
Та же коллаборативная фильтрация, что и TikTok. Плюс анализ самого аудио: темп, тональность, энергия. Если ты слушаешь много быстрых треков в миноре — система предложит похожие, даже незнакомых исполнителей.

**Netflix — Рекомендации**
Netflix тратит $1 миллиард в год на алгоритм рекомендаций. Они выяснили, что пользователь принимает решение «смотреть или нет» за **90 секунд**. Если за это время ничего не зацепило — уходит. Алгоритм должен показать правильный контент мгновенно.

**Антиспам-фильтры в почте**
Gmail использует **наивный байесовский классификатор** — алгоритм, который учится на примерах спама. Он смотрит: если в письме есть слово «выиграй», с какой вероятностью это спам? Учитывает тысячи таких слов одновременно и выдаёт вероятность. Это математика, не эвристика.

**HTTPS и банковские переводы**
Каждый раз, когда ты видишь замочек в браузере, работает **RSA-шифрование**. В основе — простое математическое наблюдение: перемножить два больших простых числа легко (миллисекунды), но разложить результат на множители почти невозможно (миллиарды лет). Безопасность твоих паролей держится на этой асимметрии.

**Поиск в Google**
PageRank — алгоритм Ларри Пейджа (он же основатель Google) — ранжирует страницы по количеству ссылок на них. По сути это нахождение собственного вектора огромной матрицы. Математика линейной алгебры на миллиардах вершин.

---

## Что ты теперь знаешь

Неделю назад алгоритмы были для тебя абстракцией. Теперь ты знаешь:

- **Big O** — как оценить скорость алгоритма, не запуская его
- **Линейный и бинарный поиск** — и почему O(log n) побеждает O(n) на больших данных
- **Пузырьковая и сортировка выбором** — как работают «наивные» алгоритмы и зачем знать их внутренности
- **Рекурсия** — как функция может решать задачу, вызывая саму себя, и почему нужен базовый случай
- **Жадные алгоритмы** — локально лучший выбор не всегда даёт глобально лучший результат
- **Мемоизация** — не считай дважды, сохраняй результаты

Это не просто теория. TikTok, который ты открываешь каждый день, работает на тех же принципах. GPS, который ведёт тебя домой — тоже.

Алгоритмы — это язык, на котором говорит мир.

<!--illustration
file: day_7/day_7_algorithms_everywhere.png
alt: Коллаж — алгоритмы в повседневной жизни: Spotify, Netflix, антиспам, HTTPS, Google Maps, TikTok
prompt:
Create a Dark RPG UI infographic showing algorithms in everyday life as a collage of panels.

Title: "АЛГОРИТМЫ ВОКРУГ НАС" in cream (#e8e0d4).

Six small glass panels arranged in a 2×3 grid, each showing one real-world algorithm:

Panel 1 (teal): Spotify icon silhouette + "Похожие треки"
Label: "Коллаборативная фильтрация"

Panel 2 (indigo): Netflix screen icon + "Рекомендации"
Label: "Матричная факторизация"

Panel 3 (amber): Email envelope with shield + "Антиспам"
Label: "Наивный Байес"

Panel 4 (teal): Lock/shield icon + "HTTPS шифрование"
Label: "RSA — простые числа"

Panel 5 (green): Map pin icon + "Google Maps"
Label: "Алгоритм A*"

Panel 6 (indigo): TikTok video icon + "ForYou Page"
Label: "Глубокое обучение"

Each panel: dark glass card, small icon (white silhouette), title in cream, algorithm name in teal/amber monospace.

Connecting organic light threads between all panels — showing the interconnected nature of algorithms.

Bottom center: "Алгоритмы — это язык, на котором говорит мир"

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

← [Day 6 — Практика](/python/week_8/day_6/) | [Week 9 — Текстовый квест →](/python/week_9/day_1/)
