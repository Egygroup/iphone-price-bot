import os, re, asyncio, urllib.parse, requests, telegram
from bs4 import BeautifulSoup

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
AMAZON_URL = 'https://www.amazon.eg/dp/B0CHX5QVX1/'

bot = telegram.Bot(token=TOKEN)

def get_price():
    try:
        # ده بروكسي مجاني هيجيب صفحة أمازون من سيرفر تاني مش محظور
        proxy_url = "https://api.allorigins.win/raw?url=" + urllib.parse.quote_plus(AMAZON_URL)
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(proxy_url, headers=headers, timeout=30)
        print(f"Proxy status: {r.status_code}, length: {len(r.text)}")

        soup = BeautifulSoup(r.text, 'html.parser')
        
        # ندور على السعر بكل الطرق
        el = soup.select_one('span.a-price-whole')
        if el:
            return el.get_text().strip()
        
        m = re.search(r'(\d{1,3}(?:,\d{3})+)\s*جنيه', r.text)
        if m:
            return m.group(1)

        off = soup.select_one('span.a-offscreen')
        if off:
            return off.get_text().strip()
            
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

async def main():
    price = get_price()
    if price:
        await bot.send_message(chat_id=CHAT_ID, text=f'✅ اشتغل! السعر الحالي من أمازون: {price}')
    else:
        await bot.send_message(chat_id=CHAT_ID, text='⚠️ لسه أمازون قافش، هجرب مصدر تاني')

asyncio.run(main())
