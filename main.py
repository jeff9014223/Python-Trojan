import os, websocket, threading

session_id = os.urandom(32).hex()
discord_token = ""