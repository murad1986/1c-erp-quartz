---
type: lesson
course: "python"
week: 10
day: 5
title: "День 5 — Горизонты: куда расти дальше"
concepts: [Telegram-бот с telebot, Flask веб-сервер, pygame основы, что изучать дальше]
prerequisites: "[\"[week_10/day_4](/python/week_10/day_4/)\"]"
tags: [python, перспективы, telegram, flask, pygame]
status: draft
---

# День 5 — Горизонты: куда расти дальше

← [День 4 — Финальная архитектура](/python/week_10/day_4/) | [День 6 — Практика →](/python/week_10/day_6/)

---

> **Сегодня:** никакой игры — только разговор о том, что ты теперь можешь сделать и как именно
> **Время:** ~35 минут

---

Ты прошёл 10 недель. Начинал с `print("Hello")` — заканчиваешь полноценной RPG с сохранениями, боссом, модулями и системой уровней. Это не курс по основам — это фундамент. Сегодня посмотрим, что на этом фундаменте можно построить.

Три пути. Каждый реален прямо сейчас.

<!--illustration
file: day_5/day_5_paths.png
alt: Три пути развития квеста — Telegram, Flask, pygame
prompt:
Three diverging paths from a central crossroads, RPG route map.

CENTER: glowing crossroads with quest.py terminal icon and "> " prompt

Three paths:
  LEFT — "TELEGRAM БОТ": phone icon, teal glow, "3-4 часа | Мультиплеер", ★★☆
  CENTER-UP — "FLASK ВЕБ": browser icon, indigo glow, "Браузерная версия | Ссылка", ★★☆
  RIGHT — "PYGAME ГРАФИКА": game window icon, amber glow, "2D игра | Спрайты", ★★★

Dungeon crossroads with bioluminescent path markers.

STYLE — STRICT:
- 640x640 px square. Dark RPG UI infographic.
- Background: smooth gradient #0a0e1a → #111830 → #0d1f24, like Hollow Knight underground caverns. NOT flat black. Faint blueprint grid at 4% opacity. Soft vignette at edges.
- Palette MUTED and atmospheric: teal #4db8c7 primary, indigo #8b6cc1 secondary, amber #d4854a accents, cream #e8e0d4 text, green #7bc88f positive. ALL glows SOFT and DIFFUSED (blur 10-15px, opacity 20-35%), like bioluminescence. NEVER sharp neon.
- RPG ornamental frame with weathered stone corners. Glass-morphism panels. Floating spore particles. Monospace for code. Russian (Cyrillic) text. Three 6x6 swatches at bottom-right: #4db8c7 #8b6cc1 #d4854a.
- MOOD: Hollow Knight City of Tears — contemplative, beautiful, NOT cyberpunk.
-->

---

## Путь 1 — Telegram-бот

Твой квест уже работает через текстовые команды. Telegram-бот — это то же самое, только вместо `input()` — сообщения в чате.

```python
# Установить один раз в терминале:
# pip install pytelegrambotapi

import telebot   # pip install pytelegrambotapi

bot = telebot.TeleBot("ВАШ_ТОКЕН")  # получить у @BotFather в Telegram

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в квест! Введи 'помощь'.")

@bot.message_handler(func=lambda msg: True)
def handle(message):
    user_input = message.text.lower()
    # здесь вызываем parse_command() из нашего quest
    response = process_command(user_input, message.chat.id)
    bot.send_message(message.chat.id, response)

bot.polling()
```

Что нужно адаптировать:
- Вместо `print()` — `return` строку (бот отправит её)
- Вместо глобального `player` — словарь `players[chat_id]` (у каждого пользователя свой игрок)
- Сохранения уже есть — просто сохраняй по `chat_id`

Это **3-4 часа работы**. У тебя уже есть вся логика — нужно только изменить ввод/вывод.

---

## Путь 2 — Веб-версия на Flask

Flask — минималистичный веб-фреймворк. Ты создаёшь страницы на Python, а браузер их отображает.

```python
# pip install flask

from flask import Flask, request, jsonify, session
from quest.commands import process_command
from quest.world import build_world

app = Flask(__name__)
app.secret_key = "supersecret"

@app.route("/")
def index():
    return open("templates/index.html").read()

@app.route("/command", methods=["POST"])
def command():
    data = request.json
    user_input = data.get("command", "")
    # session хранит данные между запросами (как наш player)
    result = process_command(user_input, session)
    return jsonify({"output": result})

if __name__ == "__main__":
    app.run(debug=True)
```

На фронтенде — простая HTML-страница с полем ввода и JavaScript:
```html
<input id="cmd" placeholder="Введи команду...">
<div id="output"></div>
<script>
async function send() {
    const r = await fetch('/command', {
        method: 'POST',
        body: JSON.stringify({command: cmd.value})
    });
    const data = await r.json();
    output.innerHTML += data.output + '<br>';
}
</script>
```

Это уже **браузерная игра**. Дать ссылку другу — и он сыграет без установки Python.

---

## Путь 3 — Графика на pygame

pygame — библиотека для 2D-игр. С ней квест превращается в настоящую игру с окном, спрайтами и музыкой.

```python
# pip install pygame

import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Квест")
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 14, 26))   # наш тёмно-синий фон

    # Рисуем текст
    text = font.render("ТРОННЫЙ ЗАЛ", True, (77, 184, 199))
    screen.blit(text, (50, 50))

    pygame.display.flip()
    clock.tick(60)   # 60 FPS

pygame.quit()
```

Вся твоя игровая логика (`battle`, `describe_room`, `build_world`) остаётся. Меняется только отображение: вместо `print()` — рисование на экране.

---

## Что ещё можно сделать прямо сейчас

Без новых знаний, только с тем что ты уже умеешь:

| Идея | Что нужно | Сложность |
|:-----|:----------|:----------|
| Больше комнат и сюжет | Только Python который ты знаешь | ★☆☆ |
| Второй персонаж — торговец | Новый класс, команда «торговать» | ★☆☆ |
| Система навыков (вор, маг, воин) | Наследование классов | ★★☆ |
| Мультиплеер в одном файле | Два Player, два цикла | ★★☆ |
| Telegram-бот | +50 строк кода | ★★☆ |
| Веб-версия | Flask, HTML, JavaScript | ★★★ |
| Графика | pygame | ★★★ |

---

## Задания

<details>
<summary>Задание 1 — Telegram-бот за один вечер</summary>

1. Создай бота у @BotFather в Telegram (получи токен)
2. Установи `pip install pytelegrambotapi`
3. Напиши минимальный бот: отвечает на `/start` и передаёт текст в `parse_command()`
4. Запусти и поиграй в квест прямо в Telegram

Главная хитрость: замени `print()` на `return` в функциях и собирай вывод в строку через `output += ...`.
</details>

---

<details>
<summary>Задание 2 — Составь свой план развития</summary>

Открой новый файл `roadmap.md` и запиши:

1. **Что хочу сделать в ближайший месяц** (конкретно: добавить X, научиться Y)
2. **Какой проект хочу показать друзьям** (квест? бот? что-то своё?)
3. **Один новый Python-инструмент который изучу** (Flask / pygame / requests / pandas)

Это не домашнее задание — это твой план разработчика.
</details>

---

<quiz>
q: Почему для Telegram-бота нужно хранить игрока в словаре players[chat_id], а не в одной переменной player?
a: В боте одновременно могут играть сотни людей. У каждого — свой chat_id и свой прогресс. Если хранить одного player, все пользователи будут управлять одним персонажем и видеть один прогресс.
a: Telegram API требует словари для работы с данными пользователей.
a: Одна переменная player работает медленнее, чем словарь.
a: Python не поддерживает глобальные переменные в веб-окружении.
correct: 0
explanation: Это фундаментальная проблема многопользовательских систем: состояние должно быть изолировано для каждого пользователя. Словарь {chat_id: player} — простейшее решение. В серьёзных приложениях для этого используют базы данных.
</quiz>

---

## Итог дня

Три реальных пути для твоего квеста:

- **Telegram-бот**: 3-4 часа, игра в мессенджере, мультиплеер из коробки
- **Flask веб-версия**: браузерная игра, можно дать ссылку кому угодно
- **pygame графика**: настоящая 2D-игра с окном и спрайтами

Всё это строится на том, что ты уже знаешь. `import random`, модули, классы, исключения — фундамент готов. Дальше — только практика и любопытство.

← [День 4 — Финальная архитектура](/python/week_10/day_4/) | [День 6 — Практика →](/python/week_10/day_6/)
