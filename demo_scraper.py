"""
Telegram B2B Parser (DEMO VERSION)
Ищет публичные группы и каналы по ключевым словам.

Розроблено: VGRB Expert Solutions
Більше IT-рішень та ботів: https://www.crm-saas-bot.cx.ua/
"""
import os
import csv
import asyncio
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import Channel, Chat, User
from telethon.errors import SessionPasswordNeededError

# ================================
# ⚙️ НАСТРОЙКИ (Введіть свої дані)
# ================================
API_ID = 'YOUR_API_ID'        # Замени на свой API ID от my.telegram.org
API_HASH = 'YOUR_API_HASH'    # Замени на свой API HASH
PHONE = '+380XXXXXXXXX'       # Номер телефона

# Ключевые слова для поиска (beauty-ниша)
SEARCH_KEYWORDS = [
    'салон красоты', 'барбершоп', 'маникюр', 'косметолог',
    'спа', 'парикмахерская', 'брови', 'beauty'
]

# Файл для сохранения результатов
OUTPUT_FILE = 'beauty_groups_demo.csv'

# ================================
# 🛑 ОГРАНИЧЕНИЯ ДЕМО-ВЕРСИИ
# ================================
MAX_DEMO_RESULTS = 50  # Лимит найденных групп для бесплатной версии
DELAY_BETWEEN_REQUESTS = 2

# ================================
# 🚀 ПАРСЕР
# ================================
async def main():
    print("==================================================")
    print("🤖 VGRB Telegram Parser (DEMO VERSION)")
    print("🔗 Замовити повну версію або CRM-бота: https://www.crm-saas-bot.cx.ua/")
    print("==================================================\n")
    
    print("🔐 Инициализация клиента...")
    client = TelegramClient('demo_parser_session', API_ID, API_HASH)
    
    await client.connect()
    
    if not await client.is_user_authorized():
        print("📱 Требуется авторизация...")
        await client.send_code_request(PHONE)
        try:
            code = input("Введите код из Telegram: ")
            await client.sign_in(phone=PHONE, code=code)
        except SessionPasswordNeededError:
            password = input("Введите 2FA пароль: ")
            await client.sign_in(password=password)
    
    print("✅ Авторизация успешна!\n")
    
    all_groups = {}
    
    print(f"🔍 Начинаю поиск (Лимит демо-версии: {MAX_DEMO_RESULTS} результатов)...\n")
    
    for idx, keyword in enumerate(SEARCH_KEYWORDS, 1):
        if len(all_groups) >= MAX_DEMO_RESULTS:
            break
            
        print(f"[{idx}/{len(SEARCH_KEYWORDS)}] Поиск: '{keyword}'")
        
        try:
            async for dialog in client.iter_dialogs(limit=20, ignore_migrated=True):
                if len(all_groups) >= MAX_DEMO_RESULTS:
                    break
                    
                if isinstance(dialog.entity, (Channel, Chat)):
                    if keyword.lower() in dialog.title.lower():
                        group_info = {
                            'id': dialog.id,
                            'title': dialog.title,
                            'username': getattr(dialog.entity, 'username', None),
                            'participants_count': getattr(dialog.entity, 'participants_count', 0),
                            'type': 'channel' if isinstance(dialog.entity, Channel) else 'group',
                            'search_keyword': keyword,
                        }
                        
                        if dialog.id not in all_groups:
                            all_groups[dialog.id] = group_info
                            print(f"  ✅ Найдено: {dialog.title} ({group_info['participants_count']} участников)")
            
            await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
            
        except Exception as e:
            print(f"  ❌ Ошибка при поиске '{keyword}': {e}")
            continue
            
    print("\n==================================================")
    print(f"🛑 Достигнут лимит ДЕМО-ВЕРСИИ ({len(all_groups)}/{MAX_DEMO_RESULTS}).")
    print("💡 Щоб зняти ліміти та отримати розширений парсер (пошук по глобальній базі, парсинг учасників, авторозсилка) — переходьте на сайт:")
    print("👉 https://www.crm-saas-bot.cx.ua/")
    print("==================================================")
    
    if all_groups:
        save_to_csv(list(all_groups.values()))
        print(f"✅ Результаты сохранены в {OUTPUT_FILE}")
    
    await client.disconnect()

def save_to_csv(groups):
    if not groups:
        return
    
    fieldnames = ['id', 'title', 'username', 'participants_count', 'type', 'search_keyword']
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(groups)

if __name__ == '__main__':
    asyncio.run(main())