#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌱 BLOOM HELPER - Помощник для Блума

Этот скрипт помогает мне (Блуму) легко читать сообщения от Макса
и отправлять ответы через бота.
"""

import json
import os
from datetime import datetime

MESSAGES_FILE = os.path.join(os.path.dirname(__file__), 'messages.json')
RESPONSES_FILE = os.path.join(os.path.dirname(__file__), 'responses.json')


def load_json(filename):
    """Загрузить JSON"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_json(filename, data):
    """Сохранить JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def show_new_messages():
    """Показать новые сообщения от Макса"""
    messages = load_json(MESSAGES_FILE)
    new_messages = [m for m in messages if m['status'] == 'new']
    
    if not new_messages:
        print("📭 Нет новых сообщений от Макса")
        return []
    
    print(f"\n📬 НОВЫЕ СООБЩЕНИЯ ({len(new_messages)}):")
    print("=" * 60)
    
    for msg in new_messages:
        timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%d.%m.%Y %H:%M')
        print(f"\n[#{msg['id']}] {timestamp}")
        print(f"От: {msg['username']}")
        print(f"Текст: {msg['text']}")
        print("-" * 60)
    
    return new_messages


def mark_as_read(message_ids=None):
    """Пометить сообщения как прочитанные"""
    messages = load_json(MESSAGES_FILE)
    
    count = 0
    for msg in messages:
        if message_ids is None or msg['id'] in message_ids:
            if msg['status'] == 'new':
                msg['status'] = 'read'
                count += 1
    
    save_json(MESSAGES_FILE, messages)
    print(f"✅ Помечено как прочитано: {count} сообщений")


def send_response(text, parse_mode=None):
    """Отправить ответ Максу"""
    responses = load_json(RESPONSES_FILE)
    
    response = {
        'id': len(responses) + 1,
        'text': text,
        'timestamp': datetime.now().isoformat(),
        'status': 'new',
    }
    
    if parse_mode:
        response['parse_mode'] = parse_mode
    
    responses.append(response)
    save_json(RESPONSES_FILE, responses)
    
    print(f"✅ Ответ #{response['id']} добавлен в очередь отправки!")
    print(f"Текст: {text[:100]}...")


def show_status():
    """Показать статус"""
    messages = load_json(MESSAGES_FILE)
    responses = load_json(RESPONSES_FILE)
    
    new_msg = sum(1 for m in messages if m['status'] == 'new')
    read_msg = sum(1 for m in messages if m['status'] == 'read')
    
    new_resp = sum(1 for r in responses if r['status'] == 'new')
    sent_resp = sum(1 for r in responses if r['status'] == 'sent')
    
    print("\n📊 СТАТУС:")
    print("=" * 60)
    print(f"📬 Сообщения от Макса:")
    print(f"   🆕 Новых: {new_msg}")
    print(f"   👀 Прочитано: {read_msg}")
    print(f"   📝 Всего: {len(messages)}")
    print()
    print(f"💬 Мои ответы:")
    print(f"   🆕 В очереди: {new_resp}")
    print(f"   ✅ Отправлено: {sent_resp}")
    print(f"   📝 Всего: {len(responses)}")
    print("=" * 60)


def interactive_mode():
    """Интерактивный режим"""
    print("\n🌱 BLOOM HELPER - Интерактивный режим")
    print("=" * 60)
    
    while True:
        print("\nКоманды:")
        print("1 - Показать новые сообщения")
        print("2 - Отправить ответ")
        print("3 - Пометить как прочитанное")
        print("4 - Статус")
        print("0 - Выход")
        
        choice = input("\nВыбери команду: ").strip()
        
        if choice == '1':
            show_new_messages()
        
        elif choice == '2':
            text = input("\nВведи текст ответа:\n> ")
            if text:
                use_html = input("Использовать HTML форматирование? (y/n): ").strip().lower()
                parse_mode = 'HTML' if use_html == 'y' else None
                send_response(text, parse_mode)
        
        elif choice == '3':
            mark_as_read()
        
        elif choice == '4':
            show_status()
        
        elif choice == '0':
            print("\n👋 До встречи!")
            break
        
        else:
            print("❌ Неизвестная команда")


if __name__ == '__main__':
    try:
        interactive_mode()
    except KeyboardInterrupt:
        print("\n\n👋 До встречи!")

