import os, re, asyncio, telegram
from playwright.async_api import async_playwright

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = 'https://dream2000.com/en/apple-iphone-15-6gb-ram-128gb-black.html'

bot = telegram.Bot(token=TOKEN)

async def get_price():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        await page.goto(URL, wait_until='networkidle', timeout=60000)
        await page.wait_for_timeout(5000)

        text = await page.locator('body').inner_text()
        print(text[:1000]) # هيظهر في اللوج

        # دور على EGPxx,xxx
        m = re.search(r'EGP\s*([\d,]+\.?\d*)', text)
        if m:
            await browser.close()
            return float(m.group(1).replace(',', ''))

        await browser.close()
        return None

async def main():
    price = await get_price()
    if price:
        await bot.send_message(chat_id=CHAT_ID, text=f'✅ اشتغل! Dream2000: {price:,.0f} جنيه\n{URL}')
    else:
        await bot.send_message(chat_id=CHAT_ID, text='⚠️ لسه مش لاقي السعر')

asyncio.run(main())
