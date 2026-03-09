---
type: checklist
purpose: Track image generation for VSM course Week 1
created: 2026-02-17
status: pending_generation
---

# 🎨 Image Generation Checklist: Week 1

Этот файл отслеживает статус генерации визуальных материалов для Week 1 курса VSM.

**Источник промптов:** `../visual_prompts.md`
**Стиль:** Technical Blueprint (миллиметровая бумага, инженерный чертёж)
**Цветовая палитра:** Blueprint Blue, Warning Red, Neutral Gray, Flow Green, Caution Yellow

---

## Must-Have Images (Priority 1)

### Day 1: Intro to Lean and VSM

- [ ] **w1d1_timeline_waste.png** (Line ~138)
  - **Prompt location:** visual_prompts.md line 512-543
  - **Content:** Горизонтальный Timeline: синие блоки (VA 5 мин) vs серые блоки (Waste 235 мин)
  - **Где используется:** Day 1, Module 1 после таблицы временных потерь
  - **Status:** ❌ Not generated

- [ ] **process_cycle_efficiency.png** (Line ~138)
  - **Prompt location:** visual_prompts.md line 473-508
  - **Content:** Pie Chart: 2% синий (ценность) vs 98% красный (потери)
  - **Где используется:** Day 1, Module 1 вместе с timeline_waste
  - **Status:** ❌ Not generated

- [ ] **w1d1_ohno_circle.png** (Line ~270)
  - **Prompt location:** visual_prompts.md line 547-575
  - **Content:** Floor plan цеха с кругом мелом, человек в центре, линии взгляда на проблемы
  - **Где используется:** Day 1, Module 2 про метод Тайити Оно
  - **Status:** ❌ Not generated

- [ ] **w1d1_coffee_stream.png** (Line ~467)
  - **Prompt location:** visual_prompts.md line 578-611
  - **Content:** Схема пути кофейного зерна от Бразилии до чашки с временными метками
  - **Где используется:** Day 1, Module 3 Value Stream кофе
  - **Status:** ❌ Not generated

### Day 2: The 8 Wastes

- [ ] **w1d2_pharma_spaghetti.png** (Line ~76)
  - **Prompt location:** visual_prompts.md line 615-646
  - **Content:** Floor plan с красной запутанной линией (550м) vs зелёной прямой (50м)
  - **Где используется:** Day 2, Module 1 pharmaceutical case
  - **Status:** ❌ Not generated

- [ ] **eight_wastes_icons.png** (Line ~316)
  - **Prompt location:** visual_prompts.md line 369-406
  - **Content:** Матрица 4×2 с красными иконками для каждого типа Muda (TIM WOOD U)
  - **Где используется:** Day 2, Module 3 после TIM WOOD U таблицы
  - **Status:** ❌ Not generated

- [ ] **w1d2_overproduction_domino.png** (Line ~360)
  - **Prompt location:** visual_prompts.md line 650-678
  - **Content:** Падающие костяшки домино: Overproduction → остальные Waste → раздавленная прибыль
  - **Где используется:** Day 2, Module 3 цепная реакция потерь
  - **Status:** ❌ Not generated

- [ ] **w1d2_river_inventory.png** (Line ~524)
  - **Prompt location:** visual_prompts.md line 682-709
  - **Content:** Разрез реки: высокий уровень воды (Inventory) скрывает камни (проблемы)
  - **Где используется:** Day 2, Module 4 метафора Ohno про запасы
  - **Status:** ❌ Not generated

### Day 5: Gemba Walk

- [ ] **gemba_walk_diagram.png** (Line ~163)
  - **Prompt location:** visual_prompts.md line 786-853
  - **Content:** Floor plan с Spaghetti линией + Gemba Walk чеклист
  - **Где используется:** Day 5, Module 3 Spaghetti Diagram method
  - **Status:** ❌ Not generated

---

## Should-Have Images (Priority 2)

Эти изображения пока не интегрированы в уроки Week 1, но описаны в visual_prompts.md:

- [ ] **vsm_symbols_reference.png**
  - **Prompt location:** visual_prompts.md line 130-208
  - **Content:** Справочная таблица стандартных VSM символов
  - **Рекомендация:** Добавить в Week 2 Day 1 (VSM Symbols)
  - **Status:** ❌ Not generated

- [ ] **current_state_example.png**
  - **Prompt location:** visual_prompts.md line 213-297
  - **Content:** Полная VSM карта производства кронштейна (3 операции)
  - **Рекомендация:** Добавить в Week 2 Day 2-3 (Current State Mapping)
  - **Status:** ❌ Not generated

- [ ] **timeline_analysis.png**
  - **Prompt location:** visual_prompts.md line 301-365
  - **Content:** Детальная Timeline визуализация с разбором VA vs NVA
  - **Рекомендация:** Можно добавить в Day 1 Module 1 как альтернативу w1d1_timeline_waste
  - **Status:** ❌ Not generated

- [ ] **before_after_vsm.png**
  - **Prompt location:** visual_prompts.md line 410-469
  - **Content:** Dell Manufacturing трансформация: Current State → Future State
  - **Рекомендация:** Добавить в Day 1 Module 6 (Dell case study)
  - **Status:** ❌ Not generated

- [ ] **toc_bottleneck_diagram.png**
  - **Prompt location:** visual_prompts.md line 713-782
  - **Content:** Theory of Constraints + VSM интеграция (Drum-Buffer-Rope)
  - **Рекомендация:** Добавить в Week 3-4 когда проходят Bottlenecks
  - **Status:** ❌ Not generated

---

## Nice-to-Have Images (Priority 3)

Дополнительные изображения для будущих недель:

- [ ] **continuous_flow_diagram.png** (Week 3-4)
- [ ] **pull_system_kanban.png** (Week 3-4)
- [ ] **future_state_principles.png** (Week 5-6)

---

## Generation Workflow

### Шаг 1: Подготовка
1. Открыть `visual_prompts.md`
2. Найти соответствующий промпт (по номеру строки из чеклиста выше)
3. Скопировать полный промпт включая:
   - Style Prefix (базовый стиль)
   - Содержание конкретной иллюстрации
   - Title Block
   - Legend

### Шаг 2: Генерация
**Опция A: DALL-E 3**
```
Prompt structure:
[Style Prefix из visual_prompts.md section 2]
[Content Block из visual_prompts.md для конкретного изображения]
```

**Опция B: Midjourney**
```
/imagine prompt: [то же самое что для DALL-E 3]
--ar 16:9 --v 6
```

### Шаг 3: Сохранение
- Сохранить изображение в `/sessions/vibrant-gifted-mayer/mnt/education/value_stream_mapping/visual_assets/`
- Имя файла должно точно соответствовать указанному в чеклисте
- Формат: PNG, 1920×1080px минимум

### Шаг 4: Валидация
Проверить:
- [ ] Весь текст на русском (кроме терминов VSM, WIP, FIFO, JIT, TOC)
- [ ] Title Block в левом верхнем углу
- [ ] Legend в правом нижнем углу
- [ ] Миллиметровая сетка на фоне видна
- [ ] Цвета соответствуют палитре (Blue/Red/Gray/Green/Yellow)
- [ ] Технический стиль (не декоративный)

### Шаг 5: Интеграция
- Отметить ✅ в чеклисте выше
- Обновить статус файла
- Проверить, что Markdown ссылка в уроке работает

---

## Progress Tracker

**Week 1 Images:**
- Total: 9 images (Must-Have)
- Generated: 0
- In Progress: 0
- Pending: 9
- **Completion: 0%**

**All Weeks Images:**
- Total: 14+ images
- Generated: 0
- **Completion: 0%**

---

## Notes

### Почему изображения пока не сгенерированы?
Промпты подготовлены в `visual_prompts.md`, но требуется:
1. Либо ручная генерация через DALL-E 3 / Midjourney
2. Либо автоматизация через API (если доступно)
3. Либо использование Claude для описания, затем передача в image generation tool

### Когда генерировать?
**Критический приоритет:**
- Week 1 Must-Have images должны быть готовы до начала Week 2
- Особенно важны: eight_wastes_icons.png, w1d1_timeline_waste.png, process_cycle_efficiency.png

**Рекомендуемый порядок генерации:**
1. `eight_wastes_icons.png` (используется в Day 2, ключевая концепция)
2. `process_cycle_efficiency.png` (используется в Day 1, hook)
3. `w1d1_timeline_waste.png` (используется в Day 1, hook)
4. `w1d2_pharma_spaghetti.png` (используется в Day 2, кейс)
5. `w1d1_ohno_circle.png` (Day 1, origin story)
6. `w1d1_coffee_stream.png` (Day 1, example)
7. `w1d2_overproduction_domino.png` (Day 2, visualization)
8. `w1d2_river_inventory.png` (Day 2, metaphor)
9. `gemba_walk_diagram.png` (Day 5, method)

---

**Последнее обновление:** 2026-02-17
**Статус:** Awaiting image generation
**Next Action:** Generate Priority 1 images using visual_prompts.md
