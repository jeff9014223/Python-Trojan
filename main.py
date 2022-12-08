import os, websocket, threading, requests

SESSION_ID = os.urandom(8).hex()
TOKEN = os.getenv("TOKEN")
API_URL = "http://discord.com/api"
WS_URL = "wss://gateway.discord.gg"

session = requests.Session()
session.headers.update({
    "Authorization": f"Bot {TOKEN}"
})
new_channel_id = session.post(f"")