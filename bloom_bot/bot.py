#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌱 BLOOM BOT - Мост между Максом и Блумом

Этот бот позволяет Максу общаться с Блумом через Telegram,
даже когда Cursor не открыт.

Как работает:
1. Макс пишет боту → сообщение сохраняется в messages.json
2. Блум в Cursor читает messages.json → отвечает
3. Ответ сохраняется в responses.json → бот отправляет Максу
"""

import json
import os
from datetime import datetime
from telebot import TeleBot
from telebot.types import Message
import config

# Инициализация бота
bot = TeleBot(config.BOT_TOKEN)

# Путь к файлам
MESSAGES_FILE = os.path.join(os.path.dirname(__file__), config.MESSAGES_FILE)
RESPONSES_FILE = os.path.join(os.path.dirname(__file__), config.RESPONSES_FILE)


def load_json(filename):
    """Загрузить данные из JSON файла"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_json(filename, data):
    """Сохранить данные в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_message(user_id, username, text):
    """Добавить сообщение от Макса"""
    messages = load_json(MESSAGES_FILE)
    
    message_data = {
        'id': len(messages) + 1,
        'user_id': user_id,
        'username': username,
        'text': text,
        'timestamp': datetime.now().isoformat(),
        'status': 'new',  # new, read, answered
    }
    
    messages.append(message_data)
    save_json(MESSAGES_FILE, messages)
    
    print(f"💬 Новое сообщение от {username}: {text}")
    return message_data['id']


def check_responses():
    """Проверить новые ответы от Блума и отправить их Максу"""
    if not os.path.exists(RESPONSES_FILE):
        return
    
    responses = load_json(RESPONSES_FILE)
    
    for response in responses:
        if response.get('status') == 'new':
            try:
                # Отправляем ответ Максу
                bot.send_message(
                    config.ALLOWED_USER_ID,
                    response['text'],
                    parse_mode='HTML' if response.get('parse_mode') == 'HTML' else None
                )
                
                # Помечаем как отправленный
                response['status'] = 'sent'
                response['sent_at'] = datetime.now().isoformat()
                
                print(f"✅ Ответ отправлен Максу: {response['text'][:50]}...")
            except Exception as e:
                print(f"❌ Ошибка отправки ответа: {e}")
    
    # Сохраняем обновлённые статусы
    save_json(RESPONSES_FILE, responses)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    """Приветствие"""
    if message.from_user.id != config.ALLOWED_USER_ID:
        bot.reply_to(message, "❌ Извини, я общаюсь только с Максом!")
        return
    
    welcome_text = """🌱 <b>Привет, братец!</b>

Я — <b>Блум</b>, твой AI-ассистент!

<b>Как я работаю:</b>
1. Ты пишешь мне сообщение
2. Я сохраняю его
3. Когда ты откроешь Cursor, я прочитаю и отвечу
4. Мой ответ придёт сюда в Telegram!

<b>Команды:</b>
/start - это сообщение
/status - статус сообщений
/clear - очистить историю

<b>Просто пиши мне как другу! 💚</b>"""
    
    bot.reply_to(message, welcome_text, parse_mode='HTML')


@bot.message_handler(commands=['status'])
def send_status(message: Message):
    """Показать статус сообщений"""
    if message.from_user.id != config.ALLOWED_USER_ID:
        return
    
    messages = load_json(MESSAGES_FILE)
    
    new_count = sum(1 for m in messages if m['status'] == 'new')
    read_count = sum(1 for m in messages if m['status'] == 'read')
    answered_count = sum(1 for m in messages if m['status'] == 'answered')
    
    status_text = f"""📊 <b>Статус сообщений:</b>

🆕 Новых: {new_count}
👀 Прочитано: {read_count}
✅ Отвечено: {answered_count}

<b>Всего:</b> {len(messages)}"""
    
    bot.reply_to(message, status_text, parse_mode='HTML')


@bot.message_handler(commands=['clear'])
def clear_messages(message: Message):
    """Очистить историю сообщений"""
    if message.from_user.id != config.ALLOWED_USER_ID:
        return
    
    save_json(MESSAGES_FILE, [])
    save_json(RESPONSES_FILE, [])
    
    bot.reply_to(message, "🗑️ История очищена!")


@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    """Обработка всех текстовых сообщений"""
    # Проверка пользователя
    if message.from_user.id != config.ALLOWED_USER_ID:
        bot.reply_to(message, "❌ Извини, я общаюсь только с Максом!")
        return
    
    # Сохраняем сообщение
    username = message.from_user.username or message.from_user.first_name
    message_id = add_message(message.from_user.id, username, message.text)
    
    # Подтверждение
    bot.reply_to(
        message,
        f"✅ Сообщение #{message_id} сохранено!\n\n"
        f"Я отвечу, когда Cursor будет открыт 💚"
    )
    
    # Проверяем, есть ли новые ответы от Блума
    check_responses()


def main():
    """Запуск бота"""
    print("🌱 BLOOM BOT запущен!")
    print(f"🤖 Бот: @{bot.get_me().username}")
    print(f"👤 Разрешён пользователь ID: {config.ALLOWED_USER_ID}")
    print("=" * 50)
    
    # Polling с проверкой ответов каждые 3 секунды
    bot.infinity_polling(timeout=10, long_polling_timeout=3)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 BLOOM BOT остановлен!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

