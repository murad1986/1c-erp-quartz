---
type: flashcards
week: 1
day: 2
title: "Flashcards: 8 типов Waste (TIM WOOD U)"
concepts_count: 15
review_schedule: [1, 3, 7, 14]  # дни после изучения
tags: [waste, muda, tim-wood-u, cost-analysis, lean]
---

# 🃏 Flashcards: Day 2 — 8 видов потерь (Muda)

> **Инструкция по использованию:**
> 1. Прочитайте вопрос (Q)
> 2. Попытайтесь ответить (не подглядывая в Answer)
> 3. Раскройте ответ и проверьте себя
> 4. Отметьте результат: ✅ (знаю твёрдо), 🤔 (частично), ❌ (не знаю)
> 5. Повторите карточки через 1, 3, 7, 14 дней

---

## Concept 1: TIM WOOD U Мнемоника

**Q:** Что означает каждая буква в TIM WOOD U?

<details>
<summary>💡 Hint</summary>
Начинается с Transportation, Inventory, Motion...
</details>

**A:**

**TIM WOOD U** — это 8 типов Waste (Muda):

- **T**ransportation (Транспортировка)
- **I**nventory (Запасы)
- **M**otion (Движение людей)
- **W**aiting (Ожидание)
- **O**verproduction (Перепроизводство)
- **O**verprocessing (Избыточная обработка)
- **D**efects (Дефекты)
- **U**nutilized Talent (Нереализованный потенциал)

**Key Phrase:** "TIM WOOD не использует таланты" (U в конце)

---

## Concept 2: Transportation vs Motion

**Q:** В чём разница между Transportation Waste и Motion Waste?

**A:**

| | Transportation | Motion |
|:---|:---|:---|
| **Что движется** | Материалы, продукты, информация | Люди |
| **Пример (Manufacturing)** | Деталь везут из Building A в Building B | Оператор ходит 5 метров за каждым инструментом |
| **Пример (Office)** | Email с 15 пересылками между отделами | Сотрудник переключается между 8 вкладками браузера |
| **Измерение** | Distance × Frequency | Time на движение / Total Time |

**Мнемоника:**
- **T**ransportation = **T**hings move
- **M**otion = **M**e (people) move

---

## Concept 3: Inventory Holding Cost

**Q:** Что входит в Inventory Holding Cost и сколько это обычно составляет в год?

**A:**

**Формула:**
```
Holding Cost = Inventory Value × Holding Cost %
```

**Компоненты Holding Cost (обычно 20-30%/год):**

1. **Warehouse rent** — 6-8%
2. **Insurance** — 2-3%
3. **Obsolescence** (устаревание) — 5-10%
4. **Shrinkage/theft** — 2-4%
5. **Opportunity cost** (WACC) — 8-12%

**Пример:**
```
Average Inventory = $2M
Holding Cost = 25%/год
Annual Cost = $2M × 25% = $500,000/год
```

**Key Insight:** Inventory — это не актив, это **замороженные деньги + риск**.

---

## Concept 4: Overproduction — Мать всех Waste

**Q:** Почему Overproduction считается худшим из всех Waste?

**A:**

**Потому что Overproduction порождает все остальные 7 типов Waste:**

```
Производим больше, чем нужно
   ↓
Inventory (нужно где-то хранить излишки)
   ↓
Transportation (везём на склад)
   ↓
Motion (ищем место для хранения)
   ↓
Waiting (следующая операция не готова)
   ↓
Defects (долгое хранение → порча, устаревание)
   ↓
Overprocessing (исправление дефектов)
   ↓
Unutilized Talent (все заняты тушением пожаров, нет времени на улучшения)
```

**Taiichi Ohno:**
> "Overproduction is the worst waste because it hides all other wastes."

---

## Concept 5: Process Cycle Efficiency (PCE)

**Q:** Как посчитать Process Cycle Efficiency и что считается хорошим показателем?

**A:**

**Формула:**
```
PCE = Value-Added Time / Total Lead Time × 100%
```

**Пример (из урока — Pharma):**
```
Value-Added Time = 4.5 часа
Total Lead Time = 18 дней × 24 часа = 432 часа

PCE = 4.5 / 432 = 1.04%
```

**Типичные значения:**

| Процесс | PCE без Lean | PCE с Lean |
|:---|---:|---:|
| Manufacturing (traditional) | 2-5% | 25-40% |
| Office/Services | 1-3% | 15-30% |
| Healthcare | 5-10% | 30-50% |

**Интерпретация:**
- PCE = 1% → **99% времени продукт ждёт**
- PCE = 30% → **70% времени ждёт** (уже хорошо для многих процессов)

**Key Insight:** В большинстве процессов 90-95% времени — это Waste (Waiting, Transportation, Inventory).

---

## Concept 6: Waiting Cost

**Q:** Как посчитать стоимость Waiting для машины/оборудования?

**A:**

**Формула:**
```
Waiting Cost = Idle Time × (Equipment Cost/час + Labor Cost/час)
```

**Пример:**
```
Machine downtime: 2 часа/день (из 8)
Machine hourly cost: $150/час (depreciation + maintenance)
Operator hourly cost: $25/час

Daily Cost = 2 × ($150 + $25) = $350/день
Annual Cost = $350 × 250 working days = $87,500/год
```

**Типичные причины Waiting:**
- Unbalanced line (одна операция — bottleneck)
- Changeover time слишком долгий
- Waiting for materials/approvals
- Equipment breakdown

**Решение:** Balance line, reduce changeover, implement TPM (Total Productive Maintenance)

---

## Concept 7: Defects — Правило 1-10-100

**Q:** Что означает правило "1-10-100" для дефектов?

**A:**

**Правило 1-10-100:**
Стоимость исправления дефекта растёт **экспоненциально** в зависимости от того, когда он обнаружен:

| Когда обнаружен | Cost to Fix | Множитель |
|:---|---:|:---:|
| **На операции (сразу)** | $1 | 1× |
| **В конце процесса (inspection)** | $10 | 10× |
| **У клиента (after delivery)** | $100+ | 100×+ |

**Почему растёт:**
- На операции: просто переделать деталь
- В конце: нужно разобрать продукт, найти проблему, переделать, собрать заново
- У клиента: возврат + warranty + потеря репутации + риск litigation

**Вывод:** **Лучше предотвратить, чем исправлять** → встроенное качество (Jidoka, Poka-Yoke)

---

## Concept 8: Unutilized Talent Waste

**Q:** Почему Unutilized Talent был добавлен как 8-й тип Waste (изначально было 7)?

**A:**

**История:**
- **1960s-70s:** Taiichi Ohno сформулировал 7 видов Muda (TIM WOOD)
- **1990s-2000s:** Jeffrey Liker и другие Western Lean practitioners добавили 8-й тип

**Почему добавили:**

Оригинальные 7 Waste фокусировались на **процессе** (materials, machines, time).

Но в **knowledge economy** самый дорогой ресурс — это **люди**.

**Примеры Unutilized Talent:**
- Оператор знает, как улучшить процесс, но его не спрашивают
- Senior Engineer тратит 60% времени на рутину (мог бы делать innovations)
- Менеджер 80% времени в meetings вместо стратегии

**Цена:**
```
Senior Engineer ($150K/год)
Time on low-value tasks: 50%
Opportunity Cost = $150K × 50% = $75K/год потерянного потенциала
```

**Key Insight:** В современном мире Unutilized Talent часто дороже, чем все остальные 7 Waste вместе взятые.

---

## Concept 9: Overprocessing

**Q:** Как определить, является ли операция Overprocessing?

**A:**

**Метод: Value Analysis**

Задайте вопрос:
> **"Готов ли клиент платить за эту операцию?"**

**Если НЕТ, то это либо:**

1. **Overprocessing** — можно упростить/убрать
   - Полировка детали, которая будет окрашена
   - Formatting internal email как презентация
   - 100% inspection, когда достаточно sampling

2. **Business-Value-Added (BVA)** — нужно для бизнеса, но не для клиента
   - Compliance (регуляторные требования)
   - Бухгалтерский учёт
   - Safety procedures

**BVA ≠ Waste**, но его нужно минимизировать.

**Пример:**
```
Current: 100% visual inspection (2 min/unit, $1/unit)
Alternative: 10% sampling (0.2 min/unit, $0.10/unit)
Defect detection: 95% → 93% (acceptable)

Overprocessing Cost = ($1 - $0.10) × 100K units = $90K/год
```

---

## Concept 10: Transportation Cost Formula

**Q:** Как посчитать стоимость Transportation Waste?

**A:**

**Формула:**
```
Transportation Cost = Distance × Frequency × Cost per unit distance
```

**Пример:**
```
Product перемещается:
- Distance: 200 метров/move
- Frequency: 50 moves/день
- Cost: $0.50/метр (forklift operator time + fuel + equipment)

Daily Cost = 200 × 50 × $0.50 = $5,000/день
Annual Cost = $5K × 250 days = $1,250,000/год
```

**Инструмент для визуализации:** **Spaghetti Diagram**
- Рисуем план цеха/офиса
- Отслеживаем путь продукта стрелками
- Измеряем total distance

**Типичные причины:**
- Layout по функциональному признаку (все прессы в одном месте), а не по flow
- Централизованный склад далеко от линий
- Batch processing

**Решение:** Cellular manufacturing, Point-of-Use Storage

---

## Concept 11: Inventory Turns

**Q:** Что такое Inventory Turns и как их считать?

**A:**

**Формула:**
```
Inventory Turns = COGS (Cost of Goods Sold) / Average Inventory
```

**Пример:**
```
COGS = $50M/год
Average Inventory = $5M

Inventory Turns = $50M / $5M = 10 turns/год
Days of Inventory = 365 / 10 = 36.5 дней
```

**Типичные значения:**

| Индустрия | Inventory Turns/год |
|:---|---:|
| Manufacturing (best-in-class Lean) | 20-40 |
| Manufacturing (traditional) | 6-12 |
| Retail | 8-12 |
| Pharma | 3-5 |
| Food (perishable) | 50-100 |

**Интерпретация:**
- High turns = деньги быстро возвращаются, меньше риска
- Low turns = деньги заморожены, высокие Holding Costs

**Key Insight:** Toyota = 30-40 turns, General Motors = 8-10 turns → одна из причин конкурентного преимущества Toyota

---

## Concept 12: Motion Waste измерение

**Q:** Как измерить Motion Waste для операторов/офисных работников?

**A:**

**Методы измерения:**

### 1. Time-Motion Study (для Manufacturing)
```
Наблюдение с секундомером:
- Value-Added Time: 65%
- Motion (walking, reaching, searching): 25%
- Waiting: 10%

Motion Cost = 25% × $25/час × 8 hours × 250 days = $12,500/год (1 оператор)
```

### 2. Pedometer / Step Counter
```
Оператор проходит 3 км/смену
Annual: 3 км × 250 days = 750 км
```

### 3. Screen Recording (для Knowledge Work)
```
Developer переключается между приложениями:
- Switches: 120 раз/день
- Time per switch: 15 секунд (refocus)
- Daily loss: 120 × 15 сек = 30 минут/день = 6.25% productivity loss
```

**Решение:**
- 5S (инструменты в зоне досягаемости)
- Ergonomic workstation design
- Автоматизация рутинных переключений

---

## Concept 13: Overproduction Cost

**Q:** Как посчитать стоимость Overproduction?

**A:**

**Формула:**
```
Overproduction Cost = Excess Units × (Production Cost + Holding Cost)
```

**Пример:**
```
Takt Time (customer demand): 1 unit/4 минуты = 120 units/день
Actual production: 150 units/день
Overproduction: 30 units/день

Annual excess: 30 × 250 = 7,500 units
Production cost: $80/unit
Excess value: 7,500 × $80 = $600,000

Holding Cost (25%/год): $600K × 25% = $150,000/год
Total Overproduction Cost: $150K/год
```

**Почему это происходит:**
- "Keep people busy" mentality
- Большие batches (чтобы минимизировать changeover)
- Неправильные incentives (бонусы за volume, а не за value delivered)
- Страх простоя оборудования

**Решение:** Производить по Takt Time, уменьшить batch size, align incentives

---

## Concept 14: Cost of Poor Quality (COPQ)

**Q:** Что входит в Cost of Poor Quality и как его считать?

**A:**

**COPQ компоненты:**

```
COPQ = Scrap + Rework + Inspection + Warranty + Lost Sales
```

**Пример (10,000 units/месяц, defect rate 2.5%):**

```
Defects: 250 units

1. Scrap (20% нельзя исправить):
   50 units × $80 = $4,000

2. Rework (80%):
   200 units × $30 = $6,000

3. Extra Inspection:
   $2,000

4. Warranty Claims:
   $3,000

5. Lost Sales (клиент ушёл):
   $10,000

Monthly COPQ = $25,000
Annual COPQ = $300,000
```

**Типичные значения COPQ:**
- Manufacturing (traditional): 15-25% от Sales
- Manufacturing (Lean/Six Sigma): 3-8% от Sales

**Решение:** Jidoka (встроенное качество), Poka-Yoke (защита от ошибок), Root Cause Analysis (5 Why)

---

## Concept 15: Muda Hunting Checklist

**Q:** Какие вопросы нужно задать для каждого типа Waste при проведении Muda Hunting?

**A:**

**Systematic Muda Hunting Checklist:**

| Waste | Ключевой вопрос | Что измерить |
|:---|:---|:---|
| **Transportation** | Сколько раз и как далеко движется продукт? | Distance × Frequency |
| **Inventory** | Сколько дней/недель запасов между операциями? | Inventory Value, Turns |
| **Motion** | Сколько км проходит оператор? Сколько раз переключается? | Time on Motion / Total Time |
| **Waiting** | Сколько % времени люди/машины ждут? | Uptime vs Downtime |
| **Overproduction** | Производим больше/раньше, чем нужно клиенту? | Production vs Takt Time |
| **Overprocessing** | Готов ли клиент платить за эту операцию? | Unnecessary steps |
| **Defects** | Сколько % брака? Когда обнаруживаются дефекты? | Defect Rate, FPY, COPQ |
| **Unutilized Talent** | Сколько % времени на low-value tasks? | Skills Utilization Rate |

**Практика:**
1. Пройти Gemba Walk
2. Заполнить чеклист для вашего процесса
3. Посчитать Top 3 Waste в деньгах ($/год)
4. Предложить quick wins для устранения

---

## 📊 Tracking Progress

**Review Schedule:**

| Review | Date | Status |
|:---|:---|:---|
| **Day 1** (initial learning) | ________ | ⬜ |
| **Day 3** (first review) | ________ | ⬜ |
| **Day 7** (second review) | ________ | ⬜ |
| **Day 14** (third review) | ________ | ⬜ |

**Self-Assessment после каждого review:**

Сколько concepts из 15 вы ответили правильно без подсказок?
- 13-15 ✅ Отлично
- 10-12 🤔 Хорошо, но нужно повторить слабые места
- < 10 ❌ Пересмотрите урок Day 2

---

## 🔗 Связанные материалы

- [[Week 1 - Day 2 - The 8 Wastes]] — Полный урок
- [[Week 1 - Day 3 - Mura and Muri]] — Следующий урок
- [[promise_registry]] — Обещания курса
- [[day_1_flashcards]] — Flashcards Day 1

---

**Версия:** 1.0
**Создано:** 2026-02-17
**Концепций:** 15
**Estimated Review Time:** 20-25 минут
