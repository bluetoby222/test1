import os
import time
from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

stock = ["1101", "2330", "1102"]

# 從 GitHub Secrets 安全讀取密碼，程式碼裡不留真實資料
token = os.environ["TELEGRAM_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]

for i in range(len(stock)):
  stockid = stock[i]
  url = "https://tw.stock.yahoo.com/quote/" + stockid + ".TW"
  r = requests.get(url, headers=headers)
  soup = BeautifulSoup(r.text, "html.parser")

  price_tag = soup.find(
      "span",
      class_=[
          "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",
          "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",
          "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)",
      ],
  )
  if price_tag is None:
    price_tag = soup.select_one('span[class*="Fz(32px)"][class*="Fw(b)"]')

  price = price_tag.getText() if price_tag else "暫時無法取得"
  message = "股票 " + stockid + " 即時股價為 " + price

  api_url = f"https://api.telegram.org/bot{token}/sendMessage"
  res = requests.get(api_url, params={"chat_id": chat_id, "text": message})
  print(stockid, "Telegram回應:", res.text)
  time.sleep(3)
