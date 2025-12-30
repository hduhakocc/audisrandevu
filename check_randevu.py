import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://disrandevu.ankara.edu.tr"

BOLUMLER = [
    "Restoratif",
    "Ağız",
    "Çene",
    "Ortodonti",
    "Protetik"
]

def telegram_bildir(mesaj):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api, data={
        "chat_id": CHAT_ID,
        "text": mesaj
    })

def kontrol():
    r = requests.get(URL, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    sayfa = soup.text

    for bolum in BOLUMLER:
        if bolum in sayfa and "Randevu Bulunamadı" not in sayfa:
            telegram_bildir(
                f"🚨 RANDEVU AÇILMIŞ OLABİLİR!\nBölüm: {bolum}\n👉 disrandevu.ankara.edu.tr"
            )

kontrol()
