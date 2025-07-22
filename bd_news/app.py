from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import threading

app = Flask(__name__)

# ক্যাশে সংরক্ষণের জন্য গ্লোবাল ভেরিয়েবল
cached_headlines = []
last_scraped = datetime.min


def fetch_headlines():
    print("🔄 হেডলাইন স্ক্র্যাপ চলছে...")
    url = 'https://www.prothomalo.com/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all('h3')

    extracted = []

    for h in headlines:
        a_tag = h.find('a')
        if a_tag and a_tag.text.strip():
            title = a_tag.text.strip()
            link = a_tag['href']
            if not link.startswith('http'):
                link = 'https://www.prothomalo.com' + link
            extracted.append({'title': title, 'url': link})

    return extracted


def update_cache():
    global cached_headlines, last_scraped
    now = datetime.now()
    if now - last_scraped > timedelta(hours=1):
        cached_headlines = fetch_headlines()
        last_scraped = now
    else:
        print("✅ ক্যাশড হেডলাইন দেখানো হচ্ছে।")


@app.route('/')
def home():
    update_cache()
    return render_template('index.html', headlines=cached_headlines)


# Flask সার্ভার চালু হওয়ার পর প্রতি ঘণ্টায় ব্যাকগ্রাউন্ডে অটো-স্ক্র্যাপিং চালানো (ঐচ্ছিক)
def auto_scraper_loop():
    while True:
        update_cache()
        threading.Event().wait(3600)  # প্রতি ১ ঘন্টা (3600 সেকেন্ড)


if __name__ == '__main__':
    threading.Thread(target=auto_scraper_loop, daemon=True).start()
    app.run(debug=True)
