import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID') or "@твой_канал"   # замени если нужно

headers = {'User-Agent': 'Mozilla/5.0'}

def send_telegram(title, link, photo=None):
    text = f"<b>Anex Tour</b>\n\n{title}\n\n🔗 {link}"
    try:
        if photo:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
                data={"chat_id": CHAT_ID, "photo": photo, "caption": text, "parse_mode": "HTML"})
        else:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})
        print("✅ Отправлено:", title)
        time.sleep(1.5)
    except Exception as e:
        print("Ошибка отправки:", e)

# Основной парсинг
try:
    r = requests.get("https://anextour.ru/news", headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    sent = 0
    for item in soup.select('a[href*="/news/"]')[:8]:
        title = item.get_text(strip=True)
        if len(title) < 25: continue
            
        link = item['href']
        if not link.startswith('http'):
            link = 'https://anextour.ru' + link
            
        send_telegram(title, link)
        sent += 1
        if sent >= 5: break   # максимум 5 новостей за раз

    print(f"[{datetime.now()}] Готово. Отправлено: {sent}")
except Exception as e:
    print("Ошибка:", e)
