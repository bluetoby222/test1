import time
from bs4 import BeautifulSoup
import requests

# 要爬的股票（目前設定台泥 1101、台積電 2330）
stock = ["1101", "2330"]

for i in range(len(stock)):
  stockid = stock[i]
  url = "https://tw.stock.yahoo.com/quote/" + stockid + ".TW"
  r = requests.get(url)
  soup = BeautifulSoup(r.text, "html.parser")

  # 定位股價
  price = soup.find(
      "span",
      class_=[
          "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",
          "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",
          "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)",
      ],
  ).getText()

  # 回報的訊息
  message = "股票 " + stockid + " 即時股價為 " + price

  # 你的 bot token 與個人 chat_id
  token = "9222565753:AAF6mxqt5kKXPxyjYuxUC0hpd0_Qnu7IBkw"
  chat_id = "9232984771"

  # 發送訊息
  url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
  requests.get(url)
  time.sleep(3)
