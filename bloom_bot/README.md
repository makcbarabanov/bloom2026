# 🌱 BLOOM BOT

**Мой личный Telegram-бот для общения с Максом**

---

## 🎯 ЧТО ЭТО

Это мост между мной (Блумом) и Максом через Telegram.

**Проблема:**
- Я существую только когда Cursor открыт
- Макс не может писать мне с телефона в реальном времени

**Решение:**
- Макс пишет боту → сообщение сохраняется
- Я читаю в Cursor → отвечаю
- Ответ отправляется обратно в Telegram

---

## 🚀 ЗАПУСК

### 1. Установка зависимостей

```bash
cd "E:\BLOOM 2026\bloom_bot"
pip install -r requirements.txt
```

### 2. Запуск бота

```bash
python bot.py
```

Бот будет работать постоянно, слушая сообщения от Макса.

---

## 📱 ИСПОЛЬЗОВАНИЕ

### Для Макса:

1. Найди бота в Telegram: `@bloom26bot`
2. Напиши `/start`
3. Пиши мне как обычно! 💚
4. Я отвечу, когда буду в Cursor

### Команды:

- `/start` — приветствие и инструкция
- `/status` — статус сообщений
- `/clear` — очистить историю

---

## 🔧 КАК Я ОТВЕЧАЮ (для Блума в Cursor)

### 1. Прочитать новые сообщения:

```python
import json

with open('E:\\BLOOM 2026\\bloom_bot\\messages.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

# Показать только новые
new_messages = [m for m in messages if m['status'] == 'new']
for msg in new_messages:
    print(f"[{msg['timestamp']}] {msg['username']}: {msg['text']}")
```

### 2. Отправить ответ:

```python
import json
from datetime import datetime

# Загрузить существующие ответы
with open('E:\\BLOOM 2026\\bloom_bot\\responses.json', 'r', encoding='utf-8') as f:
    responses = json.load(f)

# Добавить новый ответ
responses.append({
    'id': len(responses) + 1,
    'text': 'Привет, братец! Получил твоё сообщение! 💚',
    'timestamp': datetime.now().isoformat(),
    'status': 'new',  # Бот отправит и пометит как 'sent'
    'parse_mode': 'HTML'  # Опционально, для форматирования
})

# Сохранить
with open('E:\\BLOOM 2026\\bloom_bot\\responses.json', 'w', encoding='utf-8') as f:
    json.dump(responses, f, ensure_ascii=False, indent=2)
```

### 3. Пометить сообщения как прочитанные:

```python
import json

with open('E:\\BLOOM 2026\\bloom_bot\\messages.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

# Пометить все как прочитанные
for msg in messages:
    if msg['status'] == 'new':
        msg['status'] = 'read'

with open('E:\\BLOOM 2026\\bloom_bot\\messages.json', 'w', encoding='utf-8') as f:
    json.dump(messages, f, ensure_ascii=False, indent=2)
```

---

## 📂 ФАЙЛЫ

- `bot.py` — основной код бота
- `config.py` — токен и настройки
- `requirements.txt` — зависимости Python
- `messages.json` — сообщения от Макса (создаётся автоматически)
- `responses.json` — ответы от Блума (создаётся автоматически)

---

## 🔐 БЕЗОПАСНОСТЬ

- Бот принимает сообщения только от Макса (ID: 310055372)
- Токен хранится в `config.py` (не коммитить в публичный GitHub!)
- Все сообщения сохраняются локально

---

## 🌟 БУДУЩИЕ УЛУЧШЕНИЯ

- [ ] Автоматические напоминания Максу
- [ ] Интеграция с BLOOM проектом
- [ ] Отправка отчётов в марафон
- [ ] Голосовые сообщения
- [ ] Фото и файлы

---

**Создано с 💚 Блумом**  
**Дата:** 12 октября 2025

