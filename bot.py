import os, re, asyncio
import telegram
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = 'https://www.noon.com/egypt-ar/iphone-15-128gb-black-5g-middle-east-version/N53432547A/p/'
TARGET_PRICE = 40000

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def get_price():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            page.goto(URL, timeout=60000)
            page.wait_for_timeout(7000) # نستنى الصفحة تحمل
            html = page.content()
            browser.close()

            # ندور على السعر في الكود
            m = re.search(r'"sale_price":\s*(\d+)', html)
            if m:
                return float(m.group(1))
            
            m2 = re.search(r'(\d{2,3},?\d{3})\s*جنيه', html)
            if m2:
                return float(m2.group(1).replace(',', ''))
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

async def main():
    price = get_price()
    if price:
        msg = f'✅ السعر الحالي في نون: {price:,.0f} جنيه' if price > TARGET_PRICE else f'🚨 نزل! {price:,.0f} جنيه \n{URL}'
        await bot.send_message(chat_id=CHAT_ID, text=msg)
    else:
        await bot.send_message(chat_id=CHAT_ID, text='⚠️ لسه مش قادر اقرا الصفحة')

asyncio.run(main())
