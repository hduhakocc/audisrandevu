import requests
from bs4 import BeautifulSoup
import os
import hashlib

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://disrandevu.ankara.edu.tr"

BOLUMLER = [
    "Restoratif",
    "Ağız, Diş, Çene Cerrahisi",
    "Ortodonti",
    "Protetik"
]

STATE_FILE = "last_state.txt"


def telegram_bildir(mesaj):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api, data={
        "chat_id": CHAT_ID,
        "text": mesaj,
        "disable_notification": False
    })


def get_page_state(text):
    """
    Sayfanın durumunu özetleyen bir hash üretir
    Aynı durum = aynı hash
    """
    relevant = []
    for bolum in BOLUMLER:
        if bolum in text:
            relevant.append(bolum)

    joined = "|".join(sorted(relevant))
    return hashlib.sha256(joined.encode()).hexdigest()


def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return None


def save_state(state):
    with open(STATE_FILE, "w") as f:
        f.write(state)


def kontrol():
    r = requests.get(URL, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    page_text = soup.text

    if "Randevu Bulunamadı" in page_text:
        return  # Hiçbir şey yok → sessiz

    current_state = get_page_state(page_text)
    last_state = load_last_state()

    if current_state != last_state:
        telegram_bildir(
            "🚨 RANDEVU DURUMU DEĞİŞTİ!\n"
            "📍 Periodontoloji hariç bir bölümde randevu açılmış olabilir.\n"
            "👉 https://disrandevu.ankara.edu.tr"
        )
        save_state(current_state)


kontrol()
