import os
import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import re

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = 'https://www.amazon.eg/s?k=iPhone+15+128GB+Black&crid=16MMQWNIW1GA5&sprefix=iphone+15+128gb+black%2Caps%2C418&ref=nb_sb_noss_1'
TARGET_PRICE = 40000

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def get_price():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        page = requests.get(URL, headers=headers, timeout=20)
        soup = BeautifulSoup(page.content, 'html.parser')

        # بيدور على سعر أول منتج في نتائج البحث
        price_whole = soup.find('span', {'class': 'a-price-whole'})
        if price_whole:
            price_text = price_whole.get_text().replace(',', '').replace('.', '')
            return float(price_text)

        # طريقة تانية لو الأولى فشلت
        price_spans = soup.find_all('span', {'class': 'a-offscreen'})
        for span in price_spans:
            text = span.get_text()
            if 'EGP' in text or 'جنيه' in text:
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
            message = f'🚨 الحق السعر نزل على أمازون! \n iPhone 15 دلوقتي بـ {current_price:,.0f} جنيه \n {URL}'
            await bot.send_message(chat_id=CHAT_ID, text=message)
        else:
            await bot.send_message(chat_id=CHAT_ID, text=f'✅ سعر أمازون الحالي: {current_price:,.0f} جنيه')
    else:
        await bot.send_message(chat_id=CHAT_ID, text='⚠️ مقدرتش أجيب السعر من أمازون. اتأكد من اللينك')

asyncio.run(main())
