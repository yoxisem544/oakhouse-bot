import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# 讀取 Telegram Bot Token（從 GitHub Secrets 獲取）
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TO_LIYING_CHAT_ID")  # 你的 Telegram 群組或個人 ID

# 檢查環境變數是否正確
if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("請設置環境變數 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID")

# 爬取 OakHouse 頁面
URL = "https://www.oakhouse.jp/cn/house/1074#room"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)

if response.status_code != 200:
    raise RuntimeError(f"爬取失敗，狀態碼 {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

# 解析房間資訊（這部分需要根據 HTML 結構調整）
rooms = []
for room_div in soup.select(".room-list .room-item"):
    room_num = room_div.select_one(".room-number").text.strip()
    room_type = room_div.select_one(".room-type").text.strip()
    availability = room_div.select_one(".availability-date").text.strip()

    if "空房" in availability:
        rooms.append(f"{room_num} {room_type} / 空房日：{availability}")

# 構建訊息
message = "📢 OAKHouse 最新狀態\n" + "\n".join(rooms) if rooms else "目前沒有空房"

# 發送到 Telegram
bot = Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHAT_ID, text=message)
print("訊息已發送至 Telegram")