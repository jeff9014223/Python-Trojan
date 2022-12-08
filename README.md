# Python-RAT

An Python Remote Administration Tool that works on Discord.
Supports multiple exploitation commands.

# Features

    !help - Help command
    !ping - Ping command
    !cd <path> - Change directory
    !ls - List directory
    !download - Download file
    !upload - Upload file
    !shell <ps> - Execute shell command
    !run - Run an file
    !exit - Exit the session
    !screenshot - Take a screenshot
    !record <seconds> - Record the screen
    !tokens - Get all discord tokens

# Setup

Create an .env file in the main directory and paste your discord-token and guild id in like this:

```conf
TOKEN=your discord token here
GUILD_ID=your guild id of your command server
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
pyinstaller --onefile --add-data=".env" main.py 
```