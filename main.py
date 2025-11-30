import requests
import time
import os
import random
from threading import Thread
from flask import Flask

# ==================================================
# 🔥 কনফিগারেশন (তোর সব ডাটা বসানো আছে)
# ==================================================
BOT_TOKEN = "7977850182:AAEgmnEdHZPEs-YS42hhrzw3tF_-LngCflk"

# ১. আইডি (বট যাতে মেসেজ পড়তে পারে)
PUBLIC_CHANNEL_ID = "-1002911849698"
PRIVATE_CHANNEL_ID = "-1003486334687"
REQUEST_GROUP_ID = "-1003427836950"

# ২. লিংক (ইউজার যাতে ক্লিক করে জয়েন হতে পারে)
PUBLIC_CHANNEL_LINK = "https://t.me/moviezone404"
PRIVATE_CHANNEL_LINK = "https://t.me/+Tb4T5tGLUmM0NDdl"
GROUP_INVITE_LINK = "https://t.me/moviezone_discuss" # তোর গ্রুপের ইউজারনেম লিংক

WEBSITE_URL = "https://moviezone400.blogspot.com"

# 💰 ইনকাম লিংকস
ADSTERRA_WATCH_LINK = "https://adaptationprodigalevil.com/h630vnjy?key=b7952d4f76fc115b1fb537b22edc4e58"
SPECIAL_GIFT_LINK = "https://adaptationprodigalevil.com/m25582sc?key=7292af8cf8be69c6ee2c76c251029629"

TMDB_API_KEY = "5355a8dc72dfddec6e4f7586a0b3a653"
IGNORE_WORDS = ['hi', 'hello', 'hlw', 'hlo', 'hey', 'admin', 'kemon', 'asen', 'koi', 'help', 'link', 'start', '/start', 'thanks', 'ok']

# ==================================================
# 🛠️ হেল্পার ফাংশন
# ==================================================
def send_telegram_message(chat_id, text, buttons=None, reply_to_message_id=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "reply_markup": buttons, "reply_to_message_id": reply_to_message_id}
    try: requests.post(url, json=payload)
    except: pass

def send_telegram_photo(chat_id, photo_url, caption, buttons):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": photo_url, "caption": caption, "parse_mode": "HTML", "reply_markup": buttons}
    try: return requests.post(url, json=payload).json()
    except: return {}

def send_reaction(chat_id, message_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMessageReaction"
    emojis = ["🔥", "❤️", "👍", "🤩", "⚡"]
    payload = {"chat_id": chat_id, "message_id": message_id, "reaction": [{"type": "emoji", "emoji": random.choice(emojis)}]}
    try: requests.post(url, json=payload)
    except: pass

def check_group_updates(offset):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}"
    try: return requests.get(url).json()
    except: return {}

def get_last_page():
    if os.path.exists("last_page.txt"):
        with open("last_page.txt", "r") as f: 
            try: return int(f.read().strip())
            except: return 1
    return 1

def save_last_page(page):
    with open("last_page.txt", "w") as f: f.write(str(page))

# ==================================================
# 🌐 সার্ভার কিপার
# ==================================================
app = Flask('')
@app.route('/')
def home(): return "MovieZone Google Hack Engine Running! 🔥"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): t = Thread(target=run); t.start()

# ==================================================
# 🚀 মেইন ইঞ্জিন
# ==================================================
def process_movies(page_num):
    print(f"📂 Scanning Page: {page_num}...")
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&page={page_num}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200: return False

        movies = response.json().get('results', [])
        if not movies: return False

        posted_movies = []
        if os.path.exists("posted.txt"):
            with open("posted.txt", "r") as f: posted_movies = f.read().splitlines()

        for movie in movies:
            movie_id = str(movie['id'])
            if movie_id in posted_movies: continue

            title = movie['title']
            overview = movie['overview'][:180] + "..." if movie.get('overview') else "Must Watch!"
            rating = movie.get('vote_average', 0)
            poster = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None
            
            if not poster: continue

            # 🔴 GOOGLE DRIVE HACK LINK (SolidTorrents বাদ)
            google_hack_link = f"https://www.google.com/search?q={title.replace(' ', '+')}+Google+Drive+Download+720p"

            # Public Post
            pub_cap = f"<b>🎬 {title}</b>\n\n⭐️ Rating: {rating:.1f}/10\n\n<b>🔥 Watch Full HD Free on Website! 👇</b>"
            pub_btn = {"inline_keyboard": [
                [{"text": "🎬 Watch Online (Server 1)", "url": f"{WEBSITE_URL}/?id={movie_id}"}],
                [{"text": "📥 Download (File Store)", "url": PRIVATE_CHANNEL_LINK}],
                [{"text": "💬 Join Discussion Group", "url": GROUP_INVITE_LINK}]
            ]}
            res = send_telegram_photo(PUBLIC_CHANNEL_ID, poster, pub_cap, pub_btn)
            if res.get("ok"): send_reaction(PUBLIC_CHANNEL_ID, res['result']['message_id'])

            # Private Post (Money + Value)
            priv_cap = f"<b>🎬 {title} (File Store)</b>\n\n✅ <b>Direct Download Links Available!</b>\n\n👇 Select Option Below:"
            priv_btn = {"inline_keyboard": [
                # বাটন ১: গুগল ড্রাইভ হ্যাক (সবচেয়ে ফাস্ট)
                [{"text": "📥 Download via Google Drive", "url": google_hack_link}],
                # বাটন ২: Adsterra (টাকা)
                [{"text": "🎬 Watch Online (Server 2)", "url": ADSTERRA_WATCH_LINK}],
                # বাটন ৩: Adsterra (বোনাস টাকা)
                [{"text": "🎁 Special Gift (Bonus)", "url": SPECIAL_GIFT_LINK}],
                # বাটন ৪: গ্রুপ লিংক
                [{"text": "💬 Request More Movies", "url": GROUP_INVITE_LINK}]
            ]}
            res = send_telegram_photo(PRIVATE_CHANNEL_ID, poster, priv_cap, priv_btn)
            if res.get("ok"): send_reaction(PRIVATE_CHANNEL_ID, res['result']['message_id'])

            with open("posted.txt", "a") as f: f.write(f"{movie_id}\n")
            print(f"✅ Posted: {title}")
            time.sleep(20)

        return True
    except Exception as e:
        print(f"⚠️ Page Error: {e}")
        return True 

def main():
    print("🚀 Engine Started...")
    last_update_id = 0
    current_page = get_last_page()
    
    while True:
        try:
            # --- PART 1: মুভি আপলোড ---
            has_more = process_movies(current_page)
            
            if has_more:
                current_page += 1
                save_last_page(current_page)
                if current_page % 10 == 0: process_movies(1) 
            else:
                current_page = 1
                save_last_page(1)
                time.sleep(3600)

            # --- PART 2: গ্রুপ রিকোয়েস্ট হ্যান্ডলার ---
            updates = check_group_updates(last_update_id + 1)
            if updates.get("ok"):
                for update in updates["result"]:
                    last_update_id = update["update_id"]
                    
                    # গ্রুপ মেসেজ চেক
                    if "message" in update and "chat" in update["message"] and str(update["message"]["chat"]["id"]) == REQUEST_GROUP_ID:
                        text = update["message"].get("text", "").lower().strip()
                        msg_id = update["message"]["message_id"]
                        
                        # স্মার্ট ফিল্টার
                        if text and len(text) > 2 and not any(word == text for word in IGNORE_WORDS):
                            reply_text = f"✅ <b>Request Received!</b>\n\nWe are checking our database for <b>{update['message'].get('text')}</b>.\nIt will be uploaded very soon! Stay tuned. 👇"
                            reply_btn = {"inline_keyboard": [
                                [{"text": "📢 Join Public Channel", "url": PUBLIC_CHANNEL_LINK}],
                                [{"text": "🔐 Join Private Channel", "url": PRIVATE_CHANNEL_LINK}]
                            ]}
                            send_telegram_message(REQUEST_GROUP_ID, reply_text, reply_btn, msg_id)

            time.sleep(2)

        except Exception as e:
            print(f"❌ Critical Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    keep_alive()
    main()
