import os
import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import re

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = 'https://www.noon.com/egypt-ar/iphone-15-128gb-black-5g-middle-east-version/N53432547A/p/'
TARGET_PRICE = 40000

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def get_price():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'ar,en;q=0.9'
        }
        page = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(page.content, 'html.parser')
        price = None

        # بيدور على أي نص فيه "جنيه" وياخد الرقم
        for tag in soup.find_all(string=re.compile('جنيه')):
            numbers = re.findall(r'[\d,]+', tag.replace(',', ''))
            if numbers:
                price = float(numbers[0])
                break

        # لو ملقاش، بيدور في كود الصفحة نفسه
        if not price:
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and '"price"' in script.string:
                    match = re.search(r'"price":\s*(\d+)', script.string)
                    if match:
                        price = float(match.group(1))
                        break
        return price

    except Exception as e:
        print(f'Error: {e}')
        return None

async def main():
    current_price = get_price()
    if current_price:
        if current_price <= TARGET_PRICE:
            message = f'🚨 الحق السعر نزل! \n iPhone 15 دلوقتي بـ {current_price:,.0f} جنيه \n {URL}'
            await bot.send_message(chat_id=CHAT_ID, text=message)
        else:
            await bot.send_message(chat_id=CHAT_ID, text=f'✅ السعر الحالي: {current_price:,.0f} جنيه')
    else:
        await bot.send_message(chat_id=CHAT_ID, text='⚠️ مقدرتش أجيب السعر دلوقتي. هجرب تاني كمان ساعة')

asyncio.run(main())
