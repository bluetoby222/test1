import time
from bs4 import BeautifulSoup
import requests

# 偽裝成一般瀏覽器，避免被 Yahoo 股市阻擋
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

# 要爬的股票（台泥 1101、台積電 2330）
stock = ["1101", "2330"]

for i in range(len(stock)):
  stockid = stock[i]
  url = "https://tw.stock.yahoo.com/quote/" + stockid + ".TW"
  r = requests.get(url, headers=headers)
  soup = BeautifulSoup(r.text, "html.parser")

  # 定位股價（支援多種網頁標籤格式）
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

  # 回報的訊息
  message = "股票 " + stockid + " 即時股價為 " + price

  # 你的 bot token 與個人 chat_id
  token = "9222565753:AAF6mxqt5kKXPxyjYuxUC0hpd0_Qnu7IBkw"
  chat_id = "9232984771"

  # 發送訊息
  send_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
  requests.get(send_url)
  time.sleep(3)
