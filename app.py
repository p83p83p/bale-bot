from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("MySheet").sheet1

@app.route("/", methods=["GET"])
def home():
    return "Bale bot is running ✅"

@app.route("/bale-webhook", methods=["POST"])
def bale_webhook():
    data = request.get_json()
    try:
        message = data.get("message", {})
        text = message.get("text", "")
        user = message.get("from", {}).get("first_name", "ناشناس")

        if text:
            sheet.append_row([user, text])
            print(f"ذخیره شد: {user} - {text}")

        return jsonify({"ok": True})
    except Exception as e:
        print("خطا:", e)
        return jsonify({"ok": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
