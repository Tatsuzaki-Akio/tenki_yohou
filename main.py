import customtkinter as ctk
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ja"
        res = requests.get(url)
        data = res.json()

        if data["cod"] != 200:
            return {"error": "都市名が見つかりません。"}

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        return {"weather": weather, "temp": temp, "humidity": humidity}

    except Exception as e:
        return {"error": f"エラーが発生しました: {e}"}


def get_tomorrow_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja"
        res = requests.get(url)
        data = res.json()

        if data["cod"] != "200":
            return {"error": f"データが見つかりません"}

        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")

        forecast_list = data["list"]
        tomorrow_data = [
            item for item in forecast_list if tomorrow_str in item["dt_txt"]
        ]

        for item in tomorrow_data:
            if "12:00:00" in item["dt_txt"]:
                weather = item["weather"][0]["description"]
                temp = item["main"]["temp"]
                humidity = item["main"]["humidity"]
                return {"weather": weather, "temp": temp, "humidity": humidity}

        return {"error:明日の天気が見つかりません"}

    except Exception as e:
        return {"error": f"エラーが発生しました:{e}"}


def show_weather():
    city = entry.get()
    if not city:
        result_label.configure(text="都市名を入力してください")
        return

    result = get_weather(city)
    tomorrow_result = get_tomorrow_weather(city)

    if "error" in result:
        result_label.configure(text=result["error"])
        return

    now_text = (
        "＜現在の天気＞\n"
        f"天気:{result['weather']}\n"
        f"気温:{result['temp']}℃\n"
        f"湿度:{result['humidity']}%\n"
    )

    if "error" in tomorrow_result:
        tomorrow_text = tomorrow_result["error"]

    else:
        tomorrow_text = (
            "＜明日の天気＞\n"
            f"天気:{result['weather']}\n"
            f"気温:{result['temp']}℃\n"
            f"湿度:{result['humidity']}%"
        )

    result_label.configure(text=now_text + tomorrow_text)


ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("天気予報アプリ")
root.geometry("300x300")

title_label = ctk.CTkLabel(root, text="天気予報アプリ")
title_label.pack(pady=10)

entry = ctk.CTkEntry(root, placeholder_text="都市名を入力（例：Tokyo）", width=200)
entry.pack(pady=10)

btn = ctk.CTkButton(root, text="検索", command=show_weather)
btn.pack(pady=10)

result_label = ctk.CTkLabel(root, text="")
result_label.pack(pady=20)

root.mainloop()
