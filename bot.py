import os, re, asyncio, telegram
from playwright.async_api import async_playwright

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = 'https://www.amazon.eg/-/en/dp/B0CHX5QVX1/'

bot = telegram.Bot(token=TOKEN)

async def get_price():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            locale='en-EG'
        )
        page = await context.new_page()
        await page.goto(URL, wait_until='domcontentloaded', timeout=60000)
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(8000)

        # 1- جرب كل الاماكن المحتملة للسعر
        selectors = [
            'span.a-price-whole',
            'span.a-offscreen',
            '#corePriceDisplay_desktop_feature_div span.a-price-whole',
            'span.a-price span.a-offscreen'
        ]

        for sel in selectors:
            try:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    txt = await loc.inner_text(timeout=2000)
                    # طلع الرقم بس من النص
                    nums = re.findall(r'[\d,]+', txt)
                    if nums:
                        val = float(nums[0].replace(',', ''))
                        if val > 5000: # تأكيد انه سعر موبايل
                            await browser.close()
                            return val
            except:
                continue

        # 2- لو فشل، دور في نص الصفحة كله على كلمة جنيه او EGP
        body_text = await page.locator('body').inner_text()
        await browser.close()

        # ابعتلي اول 300 حرف من الصفحة في التليجرام عشان اعرف امازون بيعرض ايه
        print(body_text[:1000])
        return body_text # هنرجع النص للتجربة

async def main():
    result = await get_price()
    if isinstance(result, (int, float)):
        await bot.send_message(chat_id=CHAT_ID, text=f'✅ السعر الحالي: {result:,.0f} جنيه')
    elif isinstance(result, str):
        # ده معناه انه ملقاش السعر، فهيبعتلك هو شايف ايه عشان نصلحه
        preview = result[:500].replace('\n',' ')
        await bot.send_message(chat_id=CHAT_ID, text=f'⚠️ ملقتش السعر بس الصفحة فيها:\n{preview}...')
    else:
        await bot.send_message(chat_id=CHAT_ID, text='⚠️ الصفحة فاضية')

asyncio.run(main())
