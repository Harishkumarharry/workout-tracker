import requests
from datetime import datetime
import os

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
SHEET_API_KEY = os.environ["SHEET_API_KEY"]
SHEET_AUTH = os.environ["SHEET_AUTH"]

# Natural Language for exercise API Doc: https://docx.syndigo.com/developers/docs/natural-language-for-exercise
health_tracker_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

# Sheety API Doc: https://sheety.co/docs/authentication.html
sheet_endpoint = f"https://api.sheety.co/{SHEET_API_KEY}/myWorkouts/workouts"

user_query = input("Tell me which exercise you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

params = {
    "query": user_query,
}

response = requests.post(url=health_tracker_endpoint, headers=headers, json=params)
result = response.json()

today_date = datetime.now().strftime("%x")
current_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_input = {
        "workout": {
            "date": today_date,
            "time": current_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheet_headers = {
        "Authorization": SHEET_AUTH,
    }

    sheet_response = requests.post(url=sheet_endpoint, json=sheet_input, headers=sheet_headers)

    print(sheet_response.text)

