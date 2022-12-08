import os, websocket, asyncio, requests, json
from dotenv import load_dotenv

load_dotenv()

SESSION_ID = os.urandom(8).hex()
TOKEN = os.getenv("TOKEN")
API_URL = "https://discord.com/api"
WS_URL = "wss://gateway.discord.gg"
GUILD_ID = os.getenv("GUILD_ID")

async def on_message(ws, message):
    print(message)

async def send_heartbeat(ws, interval):
    while True:
        ws.send(json.dumps({
            "op": 1,
            "d": None
        }))
        await asyncio.sleep(interval)

async def main():
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bot {TOKEN}"
    })
    channel_id = session.post(f"{API_URL}/guilds/{GUILD_ID}/channels", json={
        "name": SESSION_ID,
        "type": 0
    }).json()["id"]
    ws = websocket.create_connection(f"{WS_URL}/?v=6&encoding=json")
    ws.send(json.dumps({
        "op": 2,
        "d": {
            "token": TOKEN,
            "properties": {
                "$os": "linux",
                "$browser": "python",
                "$device": SESSION_ID
            }
        }
    }))

asyncio.run(main())