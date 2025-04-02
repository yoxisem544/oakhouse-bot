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

def fetch_vacancy_room(url: str):
    # 爬取 OakHouse 頁面
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 無頭模式，不顯示瀏覽器
        page = browser.new_page()
        page.goto(url)

        # 等待資料加載，直到指定的元素出現
        print("開始讀取 URL")
        page.wait_for_selector("#room")
        print("等待元素出現")

        # 抓取頁面 HTML
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        print("HTML GET!")

        # 取得名字
        name = soup.find(class_="p-description__name")

        # 抓取 id="room"
        element = soup.find(id="room")
        vacancy_rooms = element.find_all("article", attrs={"data-status": "vacancy"})
        result_rooms = []
        for room in vacancy_rooms:
            room_number = room.find(class_="p-room__caset__number")
            room_number_plus_date = room_number.text.replace(" ", "").replace("\n", "")
            print(room_number_plus_date)
            result_rooms.append(room_number_plus_date)

        # 抓取總空房
        total_room_element = element.find(class_="p-filter__result ext-room").find(class_="p-filter__max").text.strip()
        print("== total_room_element")
        print(total_room_element)

        browser.close()
        return name, total_room_element, result_rooms

fetch_vacancy_room("https://www.oakhouse.jp/cn/house/1074#room")
fetch_vacancy_room("https://www.oakhouse.jp/cn/house/1169#room")


# 構建訊息
# message = "📢 OAKHouse 最新狀態\n" + "\n".join(rooms) if rooms else "目前沒有空房"
# 發送到 Telegram
# send_telegram_message(TELEGRAM_BOT_TOKEN, CHAT_ID, message)