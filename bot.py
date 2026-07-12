import os
import re
import asyncio
import telegram
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = 'https://www.amazon.eg/-/en/dp/B0CHX5QVX1/'
TARGET_PRICE = 40000

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def get_price():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        page.goto(URL, timeout=60000)
        page.wait_for_timeout(7000) # نستنى الصفحة تحمل
        
        # جرب نجيب السعر من المكان المخصص ليه
        try:
            price_text = page.locator('span.a-price-whole').first.inner_text(timeout=5000)
            return float(price_text.replace(',', '').strip())
        except:
            pass
        
        # لو فشل، ندور في كود الصفحة كله
        content = page.content()
        m = re.search(r'(\d{2,3},\d{3})', content)
        if m:
            val = float(m.group(1).replace(',', ''))
            if val > 10000: # عشان نتأكد انه سعر موبايل مش حاجة تانية
                return val
        return None

async def main():
    price = get_price()
    if price:
        if price <= TARGET_PRICE:
            await bot.send_message(chat_id=CHAT_ID, text=f'🚨 الحق نزل! iPhone 15 بـ {price:,.0f} جنيه\n{URL}')
        else:
            await bot.send_message(chat_id=CHAT_ID, text=f'✅ السعر الحالي: {price:,.0f} جنيه')
    else:
        await bot.send_message(chat_id=CHAT_ID, text='⚠️ الصفحة فتحت بس ملقتش السعر، جرب تاني')

asyncio.run(main())
