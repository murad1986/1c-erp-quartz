---
type: longread
course: "python"
week: 6
day: 7
title: "Лонгрид: Когда программа молчит об ошибках"
concepts: []
prerequisites: "[\"[week_6/day_6](/python/week_6/day_6/)\"]"
tags: [python, ошибки, история, безопасность, лонгрид]
status: draft
---

# День 7: Когда программа молчит об ошибках

*Время чтения: ~60 минут*

Ты уже умеешь обрабатывать ошибки. Но зачем это вообще нужно — по-настоящему?

Не "потому что хорошая практика". Не "потому что так правильно". А потому что когда программа **молчит об ошибках** — люди умирают, ракеты промахиваются, и миллионы разработчиков теряют доступ к Stack Overflow.

Три реальных истории. Три разных цены молчания.

---

## Кейс 1: Therac-25 — медицинская машина, которая убивала

### Контекст

1985–1987 годы. Канада и США. Аппарат лучевой терапии **Therac-25** — один из самых современных на тот момент. Лечит рак, облучая опухоль высокоточным пучком радиации.

Предыдущие модели — Therac-20 и Therac-6 — имели аппаратные блокировки: физические реле и переключатели, которые не давали машине работать в неверном режиме. Therac-25 был "улучшен": аппаратные блокировки убрали, всё перенесли в программное обеспечение.

Программисты были уверены в своём коде. Зря.

### Что происходило

Оператор мог переключить машину из режима рентгеновских снимков в режим лечения, пока система ещё инициализировалась. В этом маленьком временном окне — доли секунды — переменная, которая управляла мощностью пучка, не успевала обновиться.

Результат: пациент получал дозу радиации в **100 раз выше** терапевтической. Не 10% сверх нормы. Не в два раза. В сто раз.

Что видел оператор на экране? **"MALFUNCTION 54".**

Не "КРИТИЧЕСКАЯ ОШИБКА: ПУЧОК НЕ ОТКАЛИБРОВАН". Не "ПРЕВЫШЕНИЕ МОЩНОСТИ В 100 РАЗ". Просто код: 54. Инструкция оператора говорила что MALFUNCTION коды — обычное дело, нужно нажать "продолжить".

Операторы нажимали продолжить. Снова. И снова.

Несколько пациентов получили тяжелейшие лучевые ожоги. Минимум трое погибли. Один пациент, Рей Кокс, получил дозу эквивалентную тому, что Хиросима и Нагасаки дали на расстоянии нескольких сотен метров от эпицентра.

### Технический разбор

Проблема называется **race condition** — состояние гонки. Два процесса (ввод оператора и инициализация мощности) работали параллельно, и результат зависел от того, кто успеет первым.

Переменная `beam_power` (условно) могла остаться с предыдущим значением:

```python
# Упрощённая модель того что происходило:

beam_power = None  # переменная не обновлена — инициализация не завершена

def set_mode(mode):
    # Нет проверки: а готова ли система?
    if mode == "xray":
        beam_power = "LOW"
    elif mode == "treatment":
        beam_power = "HIGH"

def fire_beam():
    # Нет проверки: а что сейчас в beam_power?
    activate_beam(beam_power)  # может быть None или старым значением
```

На Python это бросило бы ошибку. В реальной программе на ассемблере — тихо стреляло полной мощностью.

### Что можно было сделать

```python
def fire_beam(beam_power):
    if beam_power is None:
        raise SystemError("Критическая ошибка: мощность пучка не определена")
    if beam_power > MAX_SAFE_POWER:
        raise SystemError(
            f"ОПАСНОСТЬ: мощность {beam_power} превышает максимум {MAX_SAFE_POWER}"
        )
    # Только теперь — активация
    activate_beam(beam_power)
```

И сообщение оператору должно было быть не "MALFUNCTION 54", а "ЛЕЧЕНИЕ ПРЕРВАНО: МОЩНОСТЬ НЕ ОТКАЛИБРОВАНА. ТРЕБУЕТСЯ ПЕРЕЗАПУСК."

**Урок:** проверяй граничные состояния. Всегда. Особенно там, где ошибка стоит дорого. И давай понятные сообщения — не коды, а слова.

<!--illustration
file: day_7/therac25_timeline.png
alt: Хронология Therac-25 — 1985-1987, race condition, 6 случаев передозировки, что можно было сделать
prompt:
Create a Dark RPG UI infographic showing the Therac-25 accident timeline.

Title: "THERAC-25: 1985–1987" in cream (#e8e0d4). Subtitle: "медицинская машина, которая убивала" in dim amber.

A horizontal timeline with key events:

1985 — "Therac-25 введён в эксплуатацию"
  - Icon: medical device silhouette
  - Note: "Аппаратные блокировки заменены программными"

1986 — First accident dot (dim amber)
  - "Первые сообщения о проблемах"
  - Patient icon with warning

1986-1987 — Multiple accident markers (progressively more amber/red):
  - "6 случаев передозировки радиации"
  - "Минимум 3 погибших"
  - Patient silhouettes

RACE CONDITION diagram (center panel):
  beam_power = None   ← не обновлена
  def fire_beam():
      activate_beam(beam_power)   ← тихо стреляет полной мощностью
  - "100x доза — тихо, без предупреждения"

MALFUNCTION 54 panel (amber, dim):
  "Что видел оператор: MALFUNCTION 54"
  vs
  "Что должен был видеть: ЛЕЧЕНИЕ ПРЕРВАНО: МОЩНОСТЬ НЕ ОТКАЛИБРОВАНА"

1987 — "FIX: аппаратные блокировки возвращены"
  - Check icon

Bottom lesson: "Граничные состояния. Всегда. Особенно там где «этого не должно случиться»."

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

## Кейс 2: Ракета Patriot — 0.34 секунды, которые стоили 28 жизней

### Контекст

1991 год, Война в Заливе. Саудовская Аравия, Дахран. Система противоракетной обороны **MIM-104 Patriot** должна была перехватывать иракские ракеты Scud.

25 февраля 1991 года иракская ракета Scud попала в казарму американских войск. Погибли 28 военнослужащих, 98 ранены. Система Patriot не сработала. Почему?

### Ошибка в дробном числе

В компьютере времени нет — есть целые числа. Чтобы работать со временем, система умножала секунды на 10 и хранила как целое. Одна десятая секунды — это "1". Полсекунды — "5".

Проблема: 1/10 **нельзя точно записать в двоичной системе счисления**.

Ты видел это в Python:

```python
print(0.1 + 0.2)
# → 0.30000000000000004

print(0.1 + 0.2 == 0.3)
# → False
```

Это не баг Python. Это математика. Число 1/10 в двоичной системе — бесконечная дробь, как 1/3 в десятичной. Компьютер обрезает её до конечного числа знаков. Возникает крошечная погрешность.

Система Patriot хранила время как целое число в единицах 1/10 секунды. При переводе обратно в секунды — умножала на 0.1. Каждую десятую секунды накапливалась ошибка: примерно **0.000000095 секунды**.

Мелочь. Но система работала **100 часов непрерывно**.

100 часов × 3600 секунд × 10 десятых × 0.000000095 = **0.3433 секунды** накопленной ошибки.

Ракета Scud летела со скоростью **1676 метров в секунду**.

0.3433 × 1676 = **575 метров** ошибки позиционирования.

Система Patriot искала ракету в 575 метрах от того места, где она реально находилась. Не нашла. Решила что цели нет. Выключила перехватчик.

### Технический разбор

```python
# Как накапливается ошибка:
error_per_step = 0.1 - (1 / 10)   # крошечная, но не ноль

steps = 100 * 3600 * 10           # 100 часов работы
total_error = error_per_step * steps

print(f"Ошибка за шаг: {error_per_step}")
# → Ошибка за шаг: -2.7755575615628914e-18

print(f"Накопленная ошибка: {total_error:.6f} секунд")
# Небольшое число, но при скорости ракеты — сотни метров

speed_of_scud = 1676  # метров в секунду
position_error = abs(total_error) * speed_of_scud
print(f"Ошибка позиционирования: {position_error:.1f} метров")
```

Программисты знали про неточность — в документации была ссылка на неё. Но не было кода, который накопленную ошибку **обнаруживал бы и исправлял**.

### Что можно было сделать

Инженеры армии США нашли проблему **за два дня до** атаки на Дахран. Исправление было уже в пути — патч не успел прийти вовремя. Но системы Patriot в Израиле получили патч и работали корректно.

Правильная логика: при долгой работе — периодически сбрасывать накопленное время или использовать целочисленную арифметику для хранения временных меток вместо десятичных дробей.

```python
# Плохо: накапливать float
elapsed = 0.0
while True:
    elapsed += 0.1   # ошибка растёт

# Лучше: хранить целые числа, делить только при отображении
elapsed_tenths = 0
while True:
    elapsed_tenths += 1
    elapsed_seconds = elapsed_tenths / 10   # только для вывода
```

**Урок:** `0.1 + 0.2 != 0.3` — это не абстрактный факт из учебника. Маленькая ошибка, умноженная на большой масштаб — большая катастрофа. Всегда думай о накоплении погрешностей в долгоработающих системах.

<!--illustration
file: day_7/patriot_float_error.png
alt: Ракета Patriot — накопление ошибки float за 100 часов привело к промаху в 575 метров
prompt:
Create a Dark RPG UI infographic showing floating point accumulation error in the Patriot missile system.

Title: "PATRIOT: 0.34 СЕКУНДЫ = 575 МЕТРОВ" in cream (#e8e0d4).

Top panel — the accumulation chain:

STEP 1 (small, teal):
  1/10 в двоичной = бесконечная дробь
  0.1 → 0.1000000000000000055511...
  "Крошечная погрешность за шаг"

STEP 2 (medium, amber):
  100 часов × 3600 × 10 = 3,600,000 шагов
  Накопленная ошибка: 0.3433 секунды
  "Мелочь × большое число = катастрофа"

STEP 3 (large, red-amber):
  Ракета Scud: 1676 м/с
  0.3433 × 1676 = 575 метров ошибки
  Patriot искал ракету в 575м от реальной позиции
  "Цель не найдена → перехватчик отключён"

Python code panel (center):
  print(0.1 + 0.2)
  # → 0.30000000000000004
  print(0.1 + 0.2 == 0.3)
  # → False

Visual: trajectory showing Scud missile actual path vs where Patriot was looking — gap of 575m labeled in amber.

Fix panel (teal):
  # Хранить целые числа, делить только при выводе
  elapsed_tenths += 1
  elapsed_seconds = elapsed_tenths / 10

Bottom: "25 февраля 1991 года. 28 погибших. Причина — float."

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

## Кейс 3: Stack Overflow 2019 — 35 минут тишины для миллионов разработчиков

### Контекст

2019 год. Stack Overflow — самый посещаемый ресурс для программистов в мире. Десятки миллионов разработчиков открывают его ежедневно — буквально по несколько раз в час.

11 июля 2019 года сайт был **полностью недоступен 35 минут**.

Для большинства пользователей это просто раздражение. Для компаний, где разработчики в разгаре спринта — реальная потеря. Для самой Stack Overflow — репутационный удар и подробный постмортем (разбор аварии), который они опубликовали открыто.

### Что произошло

Команда разрабатывала новую функцию. В процессе добавили проверку данных в базе — SQL-запрос, который выполнялся каждый раз при HTTP-запросе к сайту.

Запрос работал нормально на тестовых данных. На production-данных — завис. Один запрос, зависший на несколько секунд, на сайте с миллионами запросов в минуту моментально создал очередь из тысяч зависших потоков.

Команда это заметила и попыталась откатить изменение. Но при откате что-то пошло не так с кэшем. Система начала обновлять кэш — и каждая попытка обновления кидала исключение. Код обработки этого исключения... пытался снова обновить кэш. И снова ловил исключение. И снова пытался.

```python
# Упрощённая модель того что случилось:

def update_cache():
    try:
        result = fetch_from_database()   # зависает или падает
        cache.set("key", result)
    except Exception:
        update_cache()   # ← РЕКУРСИЯ! Каждая ошибка вызывает новую попытку

# При каждом HTTP-запросе вызывался update_cache()
# Каждый вызов → ошибка → новый вызов → новая ошибка → ...
```

Это называется **бесконечный цикл ретрая** (retry loop). Программа честно старалась исправить ситуацию — и тем самым делала её хуже.

### Технический разбор

Две проблемы сложились вместе:

**Проблема 1: `except Exception` вместо конкретного типа**

```python
# Плохо: ловим всё подряд
try:
    result = fetch_data()
except Exception:
    retry()   # что бы ни произошло — пробуем снова

# Хорошо: ловим только то, от чего умеем оправляться
try:
    result = fetch_data()
except ConnectionError:
    retry()   # сеть упала — имеет смысл попробовать снова
except DatabaseError:
    log_and_fail()   # база данных сломана — повтор не поможет
```

**Проблема 2: retry без лимита**

```python
# Плохо — ретри без лимита, если fetch_data всегда падает — бесконечный цикл
while True:
    try:
        result = fetch_data()
        break
    except Exception:
        continue

# Хорошо — максимум 3 попытки, потом сдаёмся
for attempt in range(3):
    try:
        result = fetch_data()
        break
    except Exception as e:
        if attempt == 2:
            raise   # три попытки — сдаёмся, пробрасываем исключение
        print(f"Попытка {attempt + 1} не удалась: {e}")
```

Stack Overflow публично опубликовал постмортем — разбор того что пошло не так и как они это исправили. Это культура в серьёзных компаниях: не скрывать аварии, а учиться на них.

**Урок:** `except Exception` без конкретного типа + retry без лимита — опасная комбинация. Отдельно они безвредны. Вместе — могут положить целый сайт.

---

## Что это значит для тебя

Три истории, три разных масштаба, три разных причины. Но общая нить одна: программа **молчала**.

Therac-25 не кричал "ОПАСНОСТЬ" — говорил "MALFUNCTION 54". Patriot не сигнализировал о накопленной погрешности — тихо считал неправильные координаты. Код Stack Overflow не сдавался — продолжал пытаться, делая хуже.

**Из Therac-25:** всегда проверяй граничные значения. Особенно там где "этого не должно случиться". Именно там и случается. И давай понятные сообщения — не коды, а слова.

```python
# Плохо
if status == 54:
    show("MALFUNCTION 54")

# Хорошо
if power > MAX_SAFE_POWER:
    emergency_stop()
    show(f"ОСТАНОВКА: мощность {power} превышает безопасный максимум {MAX_SAFE_POWER}")
```

**Из Patriot:** `float` неточен. Это не баг — это математика. Когда точность критична — используй целые числа или специальные библиотеки (`decimal`). Думай о накоплении погрешностей в долгоработающих программах.

```python
from decimal import Decimal

# Для финансовых расчётов или критически точных вычислений:
price = Decimal("0.1") + Decimal("0.2")
print(price)          # → 0.3  (точно!)
print(price == Decimal("0.3"))  # → True
```

**Из Stack Overflow:** конкретные типы исключений — это не педантизм. Это разница между "понимаю что пошло не так и как это исправить" и "что-то пошло не так, пробуем снова". Retry с лимитом — всегда.

<!--illustration
file: day_7/silent_errors_lesson.png
alt: 3 правила от катастроф — из Therac-25, Patriot и Stack Overflow
prompt:
Create a Dark RPG UI infographic summarizing the three lessons from catastrophic software failures.

Title: "3 ПРАВИЛА ОТ КАТАСТРОФ" in cream (#e8e0d4). Subtitle: "из Therac-25, Patriot, Stack Overflow" in gray-blue.

Three large glass-morphism panels arranged vertically, each representing one lesson:

PANEL 1 (teal) — from Therac-25:
  Icon: open eye / watchful shield
  Heading: "1. Проверяй граничные значения"
  Lesson: "Особенно там где «этого не должно случиться» — именно там и случается"
  Code comparison:
    ✗ show("MALFUNCTION 54")
    ✓ if power > MAX_SAFE_POWER: emergency_stop()

PANEL 2 (amber) — from Patriot:
  Icon: decimal/precision symbol
  Heading: "2. Никогда не глоти ошибки молча"
  Lesson: "0.1 + 0.2 ≠ 0.3 — это математика. Маленькая ошибка × большой масштаб = катастрофа"
  Code comparison:
    ✗ elapsed += 0.1  (накопление)
    ✓ elapsed_tenths += 1  (целые числа)

PANEL 3 (indigo) — from Stack Overflow:
  Icon: specific target / precision arrow
  Heading: "3. Лови конкретные исключения, не все подряд"
  Lesson: "except Exception + retry без лимита = опасная комбинация"
  Code comparison:
    ✗ except Exception: retry()
    ✓ except ConnectionError: retry()
    ✓ except DatabaseError: log_and_fail()

Bottom strip: "try/except — это не только удобство. Это безопасность."
Three source badges: Therac-25 | Patriot | Stack Overflow

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

## Факт-бомба: ошибки как вектор атаки

Необработанные исключения — не только неудобство. Это **дыра в безопасности**.

Когда программа падает с полным traceback — она показывает структуру кода:
- Имена файлов и функций
- Структуру базы данных (если ошибка SQL)
- Используемые библиотеки и их версии
- Пути к файлам на сервере

Злоумышленники целенаправленно вызывают ошибки — вводят странные данные, посылают неожиданные запросы — чтобы получить эту информацию и найти уязвимости.

По данным исследований, среднее время между обнаружением уязвимости и её эксплуатацией — около **15 дней**. Это значит что у тебя меньше двух недель с момента появления бага до того как им воспользуются.

```python
# Плохо на production-сервере:
try:
    result = process_request(data)
except Exception as e:
    print(f"Ошибка: {e}")   # показывает детали атакующему
    import traceback
    traceback.print_exc()   # показывает структуру кода атакующему

# Хорошо:
try:
    result = process_request(data)
except Exception as e:
    log_error(e)                         # пишем детали в лог (только для нас)
    show_user("Что-то пошло не так.")    # показываем пользователю минимум
```

`try/except` — это не только удобство и стабильность. Это безопасность.

---

## Эпилог

Therac-25 изменил подход к разработке медицинского ПО — появились строгие требования к тестированию граничных состояний и к сообщениям об ошибках.

Катастрофа с Patriot ускорила разработку стандартов представления числе с плавающей точкой в критических системах.

Stack Overflow публично описал свою аварию и ввёл обязательные постмортемы для любого инцидента — сегодня это стандартная практика в технологических компаниях.

Каждая из этих историй сделала программирование чуть лучше. Цена была высокой. Твоя задача — учиться на чужих ошибках, а не повторять их.

На следующей неделе — объектно-ориентированное программирование. `class`, `__init__`, методы — то самое, к чему мы подбирались через `class GameError(Exception): pass`.

---

← [День 6](/python/week_6/day_6/) | [Неделя 7 →](/python/week_7/day_1/)
