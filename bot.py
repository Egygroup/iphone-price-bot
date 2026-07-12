import os, re, asyncio, requests, telegram
from bs4 import BeautifulSoup

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
# نفس الآيفون 15 - 128 جيجا - أسود بس من Dream2000
URL = 'https://dream2000.com/en/apple-iphone-15-6gb-ram-128gb-black.html'
TARGET = 40000

bot = telegram.Bot(token=TOKEN)

def get_price():
    r = requests.get(URL, headers={'User-Agent':'Mozilla/5.0'}, timeout=20)
    soup = BeautifulSoup(r.text, 'html.parser')
    # السعر بيكون اول رقم فيه EGP
    m = re.search(r'EGP\s*([\d,]+\.?\d*)', r.text)
    if m:
        return float(m.group(1).replace(',', ''))
    return None

async def main():
    price = get_price()
    if price:
        msg = f'✅ سعر iPhone 15 128GB Black في Dream2000: {price:,.0f} جنيه\n{URL}'
        if price <= TARGET:
            msg = f'🚨 نزل! {price:,.0f} جنيه\n{URL}'
        await bot.send_message(chat_id=CHAT_ID, text=msg)
    else:
        await bot.send_message(chat_id=CHAT_ID, text='⚠️ مقدرتش اجيب السعر')

asyncio.run(main())
