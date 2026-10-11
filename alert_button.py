import time
import RPi.GPIO as GPIO
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={"chat_id": CHAT_ID, "text": "Someone pressed the Alert Button!"},
        timeout=10
    )

    print("Telegram response:", response.text)
    response.raise_for_status()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Alert button monitoring system is now active. Press Ctrl+C to stop.")

button_pressed = False

try:
    while True:
        if GPIO.input(7) == GPIO.HIGH and not button_pressed:
            message = "Someone pressed the alert button!"
            print(message)
            send_telegram_message(message)
            button_pressed = True

        elif GPIO.input(7) == GPIO.LOW:
            button_pressed = False

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
    GPIO.cleanup()
