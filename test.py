import customtkinter as ctk
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")


def get_tomorrow_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja"
        print("送信URL:", url)
        res = requests.get(url)
        data = res.json()

        print(data)

    except Exception as e:
        print(e)


city = input("都市を入力")
print(get_tomorrow_weather(city))
