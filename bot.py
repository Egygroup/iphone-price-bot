import os
import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import re

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = 'https://www.amazon.eg/%D9%85%D9%88%D8%A8%D8%A7%D9%8A%D9%84-%D8%A2%D9%8A%D9%81%D9%88%D9%86-%D8%A7%D8%A8%D9%84%D8%8C-128-%D8%AC%D9%8A%D8%AC%D8%A7%D8%A8%D8%A7%D9%8A%D8%AA/dp/B0CHX5QVX1/'
TARGET_PRICE = 40000

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def get_price():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        page = requests.get(URL, headers=headers, timeout=20)
        soup = BeautifulSoup(page.content, 'html.parser')

        # أمازون بيحط السعر في أماكن ثابتة
        price_whole = soup.find('span', {'class': 'a-price-whole'})
        if price_whole:
            price_text = price_whole.get_text().replace(',', '').strip()
            return float(price_text)

        # خطة بديلة
        price_offscreen = soup.find('span', {'class': 'a-offscreen'})
        if price_offscreen:
            text = price_offscreen.get_text()
            numbers = re.findall(r'[\d,]+', text.replace(',', ''))
            if numbers:
                return float(numbers[0])
        return None

    except Exception as e:
        print(f'Error: {e}')
        return None

async def main():
    current_price = get_price()
    if current_price:
        if current_price <= TARGET_PRICE:
            message = f'🚨🚨 الحق يا معلم السعر نزل! \n iPhone 15 128GB Black دلوقتي بـ {current_price:,.0f} جنيه \n {URL}'
            await bot.send_message(chat_id=CHAT_ID, text=message)
        else:
            await bot.send_message(chat_id=CHAT_ID, text=f'✅ تم التشغيل - السعر الحالي على أمازون: {current_price:,.0f} جنيه')
    else:
        await bot.send_message(chat_id=CHAT_ID, text='⚠️ مقدرتش أجيب السعر من أمازون')

asyncio.run(main())
