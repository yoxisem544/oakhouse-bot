import os
import requests
import asyncio
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from telegram import Bot

# 讀取 Telegram Bot Token（從 GitHub Secrets 獲取）
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TO_LIYING_CHAT_ID")  # 你的 Telegram 群組或個人 ID

# 檢查環境變數是否正確
if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
    print("❌ 環境變數沒有正確讀取！")
    print(f"TELEGRAM_BOT_TOKEN: {repr(TELEGRAM_BOT_TOKEN)}")  # 看看是不是 None
    print(f"TO_LIYING_CHAT_ID: {repr(CHAT_ID)}")
    raise ValueError("請設置環境變數 TELEGRAM_BOT_TOKEN 和 TO_LIYING_CHAT_ID")
else:
    print("✅ 環境變數讀取成功！")

# 發送到 Telegram 方法
def send_telegram_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)

    async def send():
        await bot.send_message(chat_id=chat_id, text=message)

    asyncio.run(send())

# 爬取 OakHouse 頁面
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # 無頭模式，不顯示瀏覽器
    page = browser.new_page()
    URL = "https://www.oakhouse.jp/cn/house/1074#room"
    page.goto(URL)

    # 等待資料加載，直到指定的元素出現
    page.wait_for_selector("#room.p-room.c-selection")

    # 抓取頁面 HTML
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    # 抓取 id="room" 且 class="p-room c-selection" 的元素
    element = soup.find(id="room", class_="p-room c-selection")

    if element:
        print(element.text)
    else:
        print("找不到指定的元素")

    browser.close()

if response.status_code != 200:
    raise RuntimeError(f"爬取失敗，狀態碼 {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

# 抓取 id="room" 且 class="p-room c-selection" 的元素
available_room_section = soup.find(id="room", class_="p-room c-selection")
print(available_room_section)

# 構建訊息
message = "📢 OAKHouse 最新狀態\n" + "\n".join(rooms) if rooms else "目前沒有空房"
# 發送到 Telegram
send_telegram_message(TELEGRAM_BOT_TOKEN, CHAT_ID, message)