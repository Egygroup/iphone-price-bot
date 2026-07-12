import os, re, asyncio, urllib.parse, requests, telegram

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
# هنحاول Dream2000 الأول وبعده RayaShop
URLS = [
    "https://dream2000.com/en/apple-iphone-15-6gb-ram-128gb-black.html",
    "https://www.rayashop.com"
]

bot = telegram.Bot(token=TOKEN)

def get_price_from(url):
    try:
        # بروكسي مجاني بيجيب الصفحة من سيرفر تاني مش محظور
        proxy = "https://api.allorigins.win/raw?url=" + urllib.parse.quote_plus(url)
        r = requests.get(proxy, timeout=30, headers={'User-Agent':'Mozilla/5.0'})
        print(f"Trying {url} -> {r.status_code} len={len(r.text)}")
        # دور على اول سعر شبه EGP 49,999 او EGP45,555
        m = re.search(r'EGP\s*([\d,]+\.?\d*)', r.text)
        if m:
            return float(m.group(1).replace(',', ''))
        m2 = re.search(r'([\d,]{2,})\.?\d*\s*EGP', r.text)
        if m2:
            return float(m2.group(1).replace(',', ''))
        return None
    except Exception as e:
        print(f"Error {url}: {e}")
        return None

async def main():
    price = None
    used_url = ""
    for u in URLS:
        price = get_price_from(u)
        if price:
            used_url = u
            break

    if price:
        await bot.send_message(chat_id=CHAT_ID, text=f'✅ اشتغل أخيراً! السعر: {price:,.0f} جنيه\nمن: {used_url}')
    else:
        await bot.send_message(chat_id=CHAT_ID, text='⚠️ لسه البروكسي مش راجع، افتح Logs في Actions وشوف سطر len=')

asyncio.run(main())
