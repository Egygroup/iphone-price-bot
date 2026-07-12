import os
import requests
from bs4 import BeautifulSoup
import telegram
import asyncio

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = 'https://www.noon.com/egypt-ar/iphone-15-128gb-black-5g-middle-east-version/N53432547A/p/'
TARGET_PRICE = 40000

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def get_price():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'} 
        page = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, 'html.parser')
        price_tag = soup.find('div', {'class': 'priceNow'})
        if price_tag:
            price_text = price_tag.text.replace('جنيه', '').replace(',', '').strip()
            return float(price_text)
    except Exception as e:
        print(f'Error: {e}')
    return None

async def main():
    current_price = get_price()
    if current_price and current_price <= TARGET_PRICE:
        message = f'🚨 الحق السعر نزل! \n iPhone 15 دلوقتي بـ {current_price} جنيه \n {URL}'
        await bot.send_message(chat_id=CHAT_ID, text=message)
    else:
        await bot.send_message(chat_id=CHAT_ID, text=f'تم التشغيل ✅ السعر الحالي: {current_price} جنيه')

asyncio.run(main())
