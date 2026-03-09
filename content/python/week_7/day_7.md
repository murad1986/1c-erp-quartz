---
type: lesson
course: "python"
week: 7
day: 7
title: "Лонгрид — Как ООП устроены враги в Dark Souls и предметы в Terraria"
concepts: []
prerequisites: "[\"[week_7/day_6](/python/week_7/day_6/)\"]"
tags: [python, ооп, геймдев, dark souls, terraria, minecraft, лонгрид]
status: draft
---

# Day 7: Лонгрид — Как ООП устроены враги в Dark Souls и предметы в Terraria

> **Сегодня:** никакого нового кода. Только истории о том, как большие игры построены изнутри — и как то, что ты изучил на этой неделе, используется в настоящих игровых движках
> **Время:** ~60 минут

---

Ты провёл неделю, строя классы, иерархии и магические методы. Может казаться, что всё это — учебные упражнения. Что в реальных играх всё устроено как-то по-другому.

На самом деле — нет. То, что ты делал в уроках 1-6, — это именно то, как строятся современные игры. Только масштаб другой.

Сегодня — три истории из реальных игр. После каждой — короткий Python-аналог, чтобы было нагляднее.

---

## Кейс 1: Dark Souls — иерархия врагов

### Как From Software думала о врагах

Когда Hidetaka Miyazaki и его команда делали Dark Souls, перед ними стояла задача: создать десятки уникальных врагов, каждый из которых ведёт себя по-своему. Простые мертвецы, рыцари, демоны, боссы с несколькими фазами, дракон — и всё это должно работать в одной системе.

Наивный подход: написать отдельный код для каждого врага. Zombie.py, Skeleton.py, DemonKing.py. Но тогда общие вещи — HP, получение урона, смерть — придётся писать снова и снова в каждом файле. Если нужно изменить логику смерти — менять во всех 50 файлах.

Решение — ООП. Один базовый класс содержит общее поведение. Конкретные враги наследуют от него и добавляют только своё уникальное.

Упрощённая иерархия Dark Souls выглядит примерно так:

```
BaseEnemy
├── Undead          (деды-мертвецы, простая ИИ)
│   ├── HollowWarrior
│   ├── HollowSoldier
│   └── CrossbowHollow
├── Demon           (огромные, уязвимы к молниям)
│   ├── CapraDemon
│   ├── CentipedeDemon
│   └── ChaosWitch
├── Dragon          (летают, дышат огнём)
│   ├── EvilEye
│   └── SeatheTheScaleless
└── Boss            (фазы, особые атаки, музыка)
    ├── ArtoriasTheAbysswalker
    ├── SifTheGreatGrey
    └── GwynLordOfCinder
```

### Что делает базовый класс

В Python-аналоге базовый враг Dark Souls выглядел бы так:

```python
class BaseEnemy:
    def __init__(self, name, hp, souls_reward, weakness=None):
        self.name = name
        self._max_hp = hp
        self._hp = hp
        self.souls_reward = souls_reward  # душ за убийство
        self.weakness = weakness or []    # к чему уязвим
        self._is_dead = False

    def take_damage(self, amount, damage_type="physical"):
        # Проверяем уязвимость
        multiplier = 1.5 if damage_type in self.weakness else 1.0
        actual_damage = int(amount * multiplier)
        self._hp = max(0, self._hp - actual_damage)

        if self._hp == 0 and not self._is_dead:
            self._is_dead = True
            self.on_death()

        return actual_damage

    def on_death(self):
        """Вызывается один раз при смерти. Подклассы переопределяют."""
        print(f"{self.name} повержен. Получено душ: {self.souls_reward}")

    def is_alive(self):
        return not self._is_dead

    def attack(self, target):
        """Базовая атака. Каждый подкласс переопределяет по-своему."""
        raise NotImplementedError("Каждый враг должен реализовать attack()")
```

### Как это работает для боссов

Артоариас — один из самых известных боссов Dark Souls. Рыцарь, павший в Бездну. Он сражается одной рукой (левая рука отдана его волку Сифу), и когда его HP падает ниже 30% — у него начинается «одержимость», и он бьёт намного агрессивнее.

В Python это выглядело бы так:

```python
class Boss(BaseEnemy):
    def __init__(self, name, hp, souls_reward, phases):
        super().__init__(name, hp, souls_reward)
        self.phases = phases      # список порогов фаз, например [0.5, 0.3]
        self.current_phase = 0
        self._enraged = False

    def take_damage(self, amount, damage_type="physical"):
        actual = super().take_damage(amount, damage_type)
        self._check_phase_transition()
        return actual

    def _check_phase_transition(self):
        hp_ratio = self._hp / self._max_hp
        for i, threshold in enumerate(self.phases):
            if hp_ratio <= threshold and self.current_phase <= i:
                self.current_phase = i + 1
                self.on_phase_change(self.current_phase)

    def on_phase_change(self, phase):
        print(f"\n  [{self.name}] ФАЗА {phase}!")


class ArtoriasTheAbysswalker(Boss):
    def __init__(self):
        super().__init__(
            name="Artorias the Abysswalker",
            hp=3000,
            souls_reward=40000,
            phases=[0.5, 0.3]   # Фаза 2 на 50% HP, фаза 3 на 30%
        )
        self._corruption_active = False

    def on_phase_change(self, phase):
        super().on_phase_change(phase)
        if phase == 2:
            print("  Арториас начинает черпать силу из Бездны...")
        elif phase == 3:
            self._corruption_active = True
            print("  Арториас ОДЕРЖИМ! Его атаки становятся стремительными!")

    def attack(self, target):
        if self._corruption_active:
            # В третьей фазе — комбо из трёх ударов
            return self._corruption_combo(target)
        else:
            return self._standard_attack(target)

    def _standard_attack(self, target):
        damage = 280
        print(f"  Арториас наносит рубящий удар: {damage} урона")
        return damage

    def _corruption_combo(self, target):
        hits = [180, 180, 200]
        total = sum(hits)
        print(f"  Арториас: КОМБО ОДЕРЖИМОСТИ — {len(hits)} удара, итого {total} урона!")
        return total
```

### Что такое полиморфизм в Dark Souls

Вот магия. В игре есть код, который обрабатывает всех врагов одинаково:

```python
def process_combat_round(player, enemy):
    # Этот код не знает, Zombie это или Artorias
    # Он просто вызывает attack() и take_damage()
    # А конкретный класс сам разберётся, что делать

    player_damage = player.get_attack_power()
    enemy.take_damage(player_damage)

    if enemy.is_alive():
        enemy_damage = enemy.attack(player)
        player.take_damage(enemy_damage)
```

Один и тот же `process_combat_round` работает со скелетом и с Артоариасом. Это и есть **полиморфизм** — когда один интерфейс (метод `attack()`) работает по-разному для разных классов.

### Интересный факт

В Dark Souls 1 босс Сиф — это волк, защищающий могилу своего погибшего хозяина Артоариаса. Когда Сифу остаётся мало HP, он начинает прихрамывать и атаковать слабее. Это тоже реализовано через `on_phase_change()` — переход в последнюю фазу меняет анимации и параметры атак. Многие игроки намеренно затягивают этот бой, потому что хромающий Сиф — это очень грустно.

<!--illustration
file: day_7/dark_souls_hierarchy.png
alt: Иерархия врагов Dark Souls — BaseEnemy, Undead, Demon, Dragon, Boss с Арториасом
prompt:
Create a Dark RPG UI infographic showing Dark Souls enemy class hierarchy in Hollow Knight visual style.

Title: "DARK SOULS — ИЕРАРХИЯ ВРАГОВ" in cream (#e8e0d4).

A tree structure with atmospheric Dark Souls aesthetic:

ROOT (top, large teal panel): "BaseEnemy"
- Key attributes: name, _hp, souls_reward, weakness[]
- Key methods: take_damage(amount, type), on_death(), is_alive(), attack()

Four branches (connected by organic glowing vines):
- "Undead" (grey-amber): HollowWarrior, HollowSoldier, CrossbowHollow as small sub-nodes
- "Demon" (orange-amber): CapraDemon, CentipedeDemon as sub-nodes. Note: "уязвим к молниям"
- "Dragon" (indigo): EvilEye, SeatheTheScaleless. Note: "летают, огонь"
- "Boss" (red-amber, largest): ArtoriasTheAbysswalker, SifTheGreatGrey, GwynLordOfCinder

Boss node expanded to show: phases=[0.5, 0.3], on_phase_change() method with glow

Special callout panel: "Артоариас: на 30% HP — одержимость, комбо из 3 ударов" in amber

Bottom: "process_combat_round() работает с ЛЮБЫМ врагом — полиморфизм" in teal.

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

## Кейс 2: Terraria — 5 000+ предметов через наследование

### Задача: 5 000 предметов без безумия

В Terraria более 5 000 предметов. Добавить новый предмет в игру — это несколько строк кода. Как это возможно?

Если бы каждый предмет описывался с нуля — 5 000 файлов, 5 000 раз написанные одни и те же поля: `name`, `weight`, `rarity`, `stack_size`. Баг в одном месте пришлось бы чинить в 5 000 местах.

Реальное решение — иерархия классов. В Terraria (написана на C#, но принцип тот же) есть примерно такая структура:

```
BaseItem
├── Weapon
│   ├── MeleeWeapon     (мечи, копья, йо-йо)
│   │   ├── Sword
│   │   ├── Spear
│   │   └── Yoyo
│   ├── RangedWeapon    (луки, пистолеты, ракетницы)
│   │   ├── Bow
│   │   └── Gun
│   ├── MagicWeapon     (жезлы, книги заклинаний)
│   └── SummonWeapon    (посохи для призыва миньонов)
├── Armor
│   ├── HeadArmor
│   ├── ChestArmor
│   └── LegArmor
├── Accessory           (кольца, зелья постоянного эффекта)
├── Consumable
│   ├── Potion
│   ├── Food
│   └── Ammo
└── Material            (руды, гели, семена — для крафта)
```

### Базовый предмет

```python
class BaseItem:
    def __init__(self, name, rarity, max_stack, sell_price):
        self.name = name
        self.rarity = rarity        # 0 (серый) до 11 (радужный)
        self.max_stack = max_stack  # сколько влезает в один слот
        self.sell_price = sell_price

    def __str__(self):
        rarity_names = {
            0: "Обычный", 1: "Синий", 2: "Зелёный", 3: "Оранжевый",
            4: "Светло-красный", 5: "Розовый", 6: "Жёлтый", 7: "Фиолетовый",
            8: "Синий (тёмный)", 9: "Красный", 10: "Огненный", 11: "Радужный"
        }
        return f"{self.name} [{rarity_names.get(self.rarity, '?')}]"

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r}, rarity={self.rarity!r})"

    def __eq__(self, other):
        if not isinstance(other, BaseItem):
            return NotImplemented
        return self.name == other.name


class Weapon(BaseItem):
    def __init__(self, name, rarity, damage, use_time, knockback, sell_price):
        super().__init__(name, rarity, max_stack=1, sell_price=sell_price)
        self.damage = damage
        self.use_time = use_time      # скорость атаки (меньше = быстрее)
        self.knockback = knockback    # отбрасывание


class MeleeWeapon(Weapon):
    def __init__(self, name, rarity, damage, use_time, knockback,
                 sell_price, reach, swing_arc=180):
        super().__init__(name, rarity, damage, use_time, knockback, sell_price)
        self.reach = reach           # длина оружия
        self.swing_arc = swing_arc   # угол удара в градусах

    def get_dps(self):
        """Damage per second — важная характеристика для сравнения оружий."""
        # use_time в игре = кадры, 60 кадров в секунду
        attacks_per_second = 60 / self.use_time
        return round(self.damage * attacks_per_second, 1)
```

### Terra Blade как объект

Terra Blade — одно из лучших оружий в Terraria. Меч, стреляющий зелёными энергетическими клинками. В системе классов это выглядело бы так:

```python
class TerraBlade(MeleeWeapon):
    """
    Terra Blade — финальный меч в Terraria.
    Крафтится из True Night's Edge + True Excalibur.
    Запускает проектили при каждом взмахе.
    """
    def __init__(self):
        super().__init__(
            name="Terra Blade",
            rarity=8,           # тёмно-синий — очень редкий
            damage=115,
            use_time=16,        # быстрая атака
            knockback=6.5,
            sell_price=200000,  # в медных монетах
            reach=90,
            swing_arc=180
        )
        self.projectile_damage = 95
        self.projectile_speed = 18.0

    def attack(self, player_position, target_direction):
        """Атака с выпуском проектиля."""
        projectile = self._launch_projectile(player_position, target_direction)
        return {
            "melee_damage": self.damage,
            "projectile": projectile
        }

    def _launch_projectile(self, origin, direction):
        return {
            "type": "TerraBeam",
            "damage": self.projectile_damage,
            "speed": self.projectile_speed,
            "origin": origin,
            "direction": direction,
            "piercing": True  # проходит сквозь нескольких врагов
        }

    def get_dps(self):
        base_dps = super().get_dps()
        # Учитываем проектили (каждый взмах = один проектиль)
        projectile_dps = self.projectile_damage * (60 / self.use_time)
        return round(base_dps + projectile_dps, 1)

    def __str__(self):
        return f"{super().__str__()} | Урон: {self.damage} | DPS: {self.get_dps()}"


# Создаём:
blade = TerraBlade()
print(blade)
# Terra Blade [Синий (тёмный)] | Урон: 115 | DPS: 650.6

print(f"Цена: {blade.sell_price // 10000} золотых")
# Цена: 20 золотых
```

### Почему это работает для 5 000+ предметов

Добавить новый меч в Terraria — это написать один класс из 5-10 строк:

```python
class Muramasa(MeleeWeapon):
    def __init__(self):
        super().__init__(
            name="Muramasa",
            rarity=3,
            damage=22,
            use_time=14,     # очень быстрый
            knockback=3.25,
            sell_price=7200,
            reach=60
        )
        self.auto_swing = True  # зажимаешь кнопку — бьёт сам
```

Пять строк — новое оружие. Все базовые механики (инвентарь, крафт, урон, физика) уже реализованы в родительских классах.

### Числа

По данным Terraria Wiki, в игре более **5 400** предметов (версия 1.4). Они распределены примерно по **50** классам предметов. Это значит, в среднем 100+ предметов на один класс. Без ООП этот код поддерживать было бы невозможно.

<!--illustration
file: day_7/terraria_items.png
alt: Дерево классов предметов Terraria — 5400+ предметов через ~50 классов
prompt:
Create a Dark RPG UI infographic showing Terraria item class tree.

Title: "TERRARIA — 5400+ ПРЕДМЕТОВ, ~50 КЛАССОВ" in cream (#e8e0d4).

A wide tree structure:

ROOT (top, teal panel): "BaseItem"
- name, rarity, max_stack, sell_price
- __str__, __repr__, __eq__

Two main branches:
LEFT: "Weapon" → "MeleeWeapon" → "Sword", "Spear", "Yoyo" as leaf nodes
                → "RangedWeapon" → "Bow", "Gun"
                → "MagicWeapon"
                → "SummonWeapon"

RIGHT: "Armor" → "HeadArmor", "ChestArmor", "LegArmor"
       "Consumable" → "Potion", "Ammo"
       "Material" (for crafting)

Special spotlight: "TerraBlade" leaf node at MeleeWeapon level with amber glow:
- rarity=8, damage=115, DPS: 650.6
- Special: projectile_damage=95

Key stat panel: "Добавить новый меч = 5-10 строк кода. Без ООП — тысячи." in amber

Bottom: large number "5 400+" with glow, and "~50 классов" showing the ratio.

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

## Кейс 3: Minecraft — система сущностей

### Entity: все в одной иерархии

Minecraft написан на Java. Но принципы ООП — универсальны, поэтому покажем Python-аналог.

В Minecraft всё, что движется и живёт — это `Entity`. Вот как выглядит иерархия:

```
Entity
└── LivingEntity           (имеет HP, может умереть)
    ├── Player             (игрок)
    └── Mob                (мобы)
        ├── Passive        (не нападают: корова, овца, курица)
        │   ├── Cow
        │   ├── Sheep
        │   └── Chicken
        ├── Neutral        (нейтральны, но злятся при атаке)
        │   ├── Wolf
        │   ├── ZombiePigman
        │   └── Enderman
        └── Hostile        (всегда атакуют игрока)
            ├── Zombie
            ├── Skeleton
            ├── Spider
            └── Creeper    ← вот о нём поговорим отдельно
```

### Python-аналог системы Entity

```python
class Entity:
    """Базовая сущность в мире Minecraft."""
    def __init__(self, entity_id, position):
        self.entity_id = entity_id
        self.position = position   # (x, y, z)
        self._active = True

    def tick(self):
        """Вызывается каждый игровой тик (20 раз в секунду)."""
        pass

    def is_active(self):
        return self._active

    def despawn(self):
        self._active = False


class LivingEntity(Entity):
    def __init__(self, entity_id, position, max_hp):
        super().__init__(entity_id, position)
        self._max_hp = max_hp
        self._hp = max_hp

    def take_damage(self, amount):
        self._hp = max(0, self._hp - amount)
        if self._hp == 0:
            self.on_death()

    def on_death(self):
        self.despawn()

    def is_alive(self):
        return self._hp > 0 and self.is_active()


class Mob(LivingEntity):
    def __init__(self, entity_id, position, max_hp, move_speed):
        super().__init__(entity_id, position, max_hp)
        self.move_speed = move_speed
        self.target = None  # кого преследуем

    def find_target(self, nearby_entities):
        """Ищет цель в радиусе. Переопределяется в подклассах."""
        pass

    def tick(self):
        super().tick()
        if self.target and self.target.is_alive():
            self._move_toward_target()

    def _move_toward_target(self):
        # Упрощённое движение
        pass


class Hostile(Mob):
    """Враждебный моб — всегда атакует игрока при обнаружении."""
    AGGRO_RANGE = 16  # блоков

    def find_target(self, nearby_entities):
        for entity in nearby_entities:
            if isinstance(entity, Player):
                self.target = entity
                return

    def attack(self):
        if self.target and self.is_alive():
            damage = self._calculate_damage()
            self.target.take_damage(damage)

    def _calculate_damage(self):
        return 5  # базовый урон, переопределяется
```

### История Creeper: баг, ставший иконой

Теперь самое интересное. Creeper — самый узнаваемый моб Minecraft. Подходит, шипит, взрывается. Все знают.

Но Creeper появился **случайно**.

В 2009 году Notch (создатель Minecraft, тогда работавший один) пытался написать свинью. В коде модели он перепутал высоту и ширину — свинья получилась вытянутой вертикально. Потом он перепутал логику атаки: вместо того чтобы бежать к игроку и бить, Creeper... взрывался.

Notch решил оставить это как есть. Добавил шипение, зелёный цвет, поведение фиксировал в коде.

В коде это выглядело бы примерно так:

```python
class Creeper(Hostile):
    FUSE_TIME = 30    # тиков до взрыва (1.5 секунды)
    EXPLOSION_POWER = 3

    def __init__(self, entity_id, position):
        super().__init__(entity_id, position, max_hp=20, move_speed=0.25)
        self._fuse_timer = 0
        self._ignited = False
        self._exploded = False

    def tick(self):
        super().tick()

        if self.target and self.is_near_target(radius=3):
            self._start_fuse()

        if self._ignited:
            self._fuse_timer += 1
            if self._fuse_timer >= self.FUSE_TIME:
                self._explode()
        elif self._fuse_timer > 0:
            # Отошли от игрока — фитиль гаснет
            self._fuse_timer = max(0, self._fuse_timer - 1)

    def _start_fuse(self):
        if not self._ignited:
            self._ignited = True
            print(f"Creeper шипит: PSSSSS...")

    def _explode(self):
        if not self._exploded:
            self._exploded = True
            print(f"БАБАХ! Взрыв силой {self.EXPLOSION_POWER} блоков!")
            # В реальном коде: уничтожить блоки вокруг, нанести урон
            self.despawn()

    def is_near_target(self, radius):
        # Упрощённая проверка расстояния
        if not self.target:
            return False
        dx = abs(self.position[0] - self.target.position[0])
        dz = abs(self.position[2] - self.target.position[2])
        return (dx ** 2 + dz ** 2) ** 0.5 <= radius

    # Creeper НЕ переопределяет attack() — он не бьёт руками.
    # Вся его "атака" — взрыв в tick().
```

Обрати внимание: `Creeper` не переопределяет метод `attack()` из `Hostile`. Вместо этого он делает всё своё в `tick()`. Это нормально — ООП не заставляет тебя использовать каждый метод родителя. Ты берёшь то, что нужно, и добавляешь своё.

### Факт о масштабах

В Java-коде Minecraft (версия 1.20) файл `Creeper.java` содержит около 200 строк кода. При этом большая часть логики — движение, обнаружение игрока, получение урона, звуки — унаследована от родительских классов и занимает ноль строк в файле Creeper. Без иерархии классов один Creeper требовал бы тысячи строк.

<!--illustration
file: day_7/minecraft_entity.png
alt: Иерархия Entity в Minecraft — от Entity до Creeper с историей про баг
prompt:
Create a Dark RPG UI infographic showing Minecraft Entity hierarchy with Creeper spotlight.

Title: "MINECRAFT — ИЕРАРХИЯ ENTITY" in cream (#e8e0d4).

LEFT side: a vertical inheritance chain as connected panels:
Entity → LivingEntity → Mob → Hostile → Creeper
Each as a glass panel. Arrows flow downward with organic glow.

Each level shows what it adds:
- Entity: entity_id, position, tick(), despawn()
- LivingEntity: _hp, take_damage(), on_death()
- Mob: move_speed, target, find_target()
- Hostile: AGGRO_RANGE=16, find_target() finds Player
- Creeper: _fuse_timer, _ignited (HIGHLIGHTED in amber)

RIGHT side: Creeper spotlight panel (green tint, iconic creeper face icon):
- tick() method shown with fuse logic:
  if near_target(radius=3): _start_fuse()
  if _ignited: _fuse_timer += 1
  if _fuse_timer >= 30: EXPLODE!
- "PSSSSS... БАБАХ!" text in amber

BOTTOM callout panel (amber warning/story):
"История: Creeper появился из БАГА — Notch перепутал высоту и ширину свиньи. Баг стал иконой."
With a skull/creeper icon and year "2009".

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

## Эпилог: ты теперь думаешь как разработчик игр

Возможно, ты заметил кое-что в трёх кейсах выше.

В Dark Souls, Terraria и Minecraft — разные жанры, разные движки, разные языки (C++, C#, Java). Но структура кода одинакова:
- Есть базовый класс с общим поведением
- Есть подклассы с уникальным поведением
- Один и тот же код обрабатывает все объекты через общий интерфейс

Когда ты писал `Enemy`, `Zombie`, `Boss` на прошлой неделе — ты делал то же самое, что делают профессиональные разработчики в компаниях вроде FromSoftware и Re-Logic.

Масштаб другой. Принцип — тот же.

**Несколько мыслей напоследок:**

Terraria добавляет новый контент патчами. Каждый раз — новые предметы, новые боссы. Благодаря иерархии классов разработчикам не нужно трогать старый код. Они просто добавляют новый подкласс. Старый код продолжает работать.

В Dark Souls 3 есть враги, код которых унаследован напрямую из Dark Souls 1 с небольшими изменениями. Наследование позволяет переиспользовать годами написанный код.

Creeper появился из бага. Код позволил этому багу превратиться в фичу быстро — потому что поведение было изолировано в одном классе. Поменяли логику одного класса — всё работает.

---

**На следующей неделе:** декораторы — та самая магия `@something`, которую ты уже видел над методами. Разберёмся, как это работает изнутри.

---

← [Day 6 — Практика](/python/week_7/day_6/) | [Week 8 — Алгоритмы →](/python/week_8/day_1/)
