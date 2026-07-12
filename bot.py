import os
import re
import asyncio
import telegram
from playwright.async_api import async_playwright

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = 'https://www.amazon.eg/-/en/dp/B0CHX5QVX1/'
TARGET_PRICE = 40000

bot = telegram.Bot(token=TOKEN)

async def get_price():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        await page.goto(URL, timeout=60000)
        await page.wait_for_timeout(7000)
        
        try:
            text = await page.locator('span.a-price-whole').first.inner_text(timeout=5000)
            await browser.close()
            return float(text.replace(',', '').strip())
        except:
            content = await page.content()
            await browser.close()
            m = re.search(r'(\d{2,3},\d{3})', content)
            if m:
                return float(m.group(1).replace(',', ''))
            return None

async def main():
    price = await get_price()
    if price:
        if price <= TARGET_PRICE:
            await bot.send_message(chat_id=CHAT_ID, text=f'🚨 الحق نزل! {price:,.0f} جنيه\n{URL}')
        else:
            await bot.send_message(chat_id=CHAT_ID, text=f'✅ السعر الحالي: {price:,.0f} جنيه')
    else:
        await bot.send_message(chat_id=CHAT_ID, text='⚠️ فتحت الصفحة بس ملقتش السعر')

asyncio.run(main())
