# Python-Trojan

A Python Remote Administration Tool that works on Discord.
Supports multiple exploitation commands.

# Discord Tokens

Due to a client update by Discord in 2022, most Token Grabbers are no longer effective.
However, this tool is designed to crack Discord's updated encryption.

# Browser Passwords

This tool is capable of extracting passwords from contemporary web browsers.

# Preview

![alt text](https://media.discordapp.net/attachments/1034059578708594690/1051309462473953310/image.png)

# Features

    help - Help command
    ping - Ping command
    cwd - Get current working directory
    cd <path> - Change directory
    ls - List directory
    download <file> - Download file
    upload <link> - Upload file
    shell <ps> - Execute shell command
    run <file> - Run an file
    exit - Exit the session
    screenshot - Take a screenshot
    tokens - Get all discord tokens
    shutdown - Shutdown the computer
    restart - Restart the computer
    passwords - Extracts all browser passwords
    history - Extracts all browser history

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
DM me on ``!Jeff$#1337`` for help. Example shown below.

```json
{
    "token": "Your discord bot token",
    "guild_id": "The guild id of the C2 server"
}
```

# Compiling to an Executable (.exe)

To compile this tool to an executable please install an Python compiler like nuitka, pyinstaller or pyarmor pack.
Here is an example of compiling with Pyinstaller

```bash
pip install pyinstaller
```

```bash
pyinstaller --onefile --windowed --clean --add-data="config.json;." main.py 
```

# Contributing

Contributions to this Python Trojan project are welcome and encouraged! Here are some guidelines for contributing:

1. Fork the repository and create a new branch for your contribution.
2. Make your changes or additions to the codebase.
3. Test your changes to ensure they work as expected.
4. Update the README with any relevant changes or additions, including documentation on new features or functionality.
5. Submit a pull request with your changes, describing the purpose and scope of your contribution.

When contributing to this project, please keep in mind the following:

- Follow the Python coding style guidelines and best practices.
- Avoid introducing any malicious or harmful code.
- Be respectful and considerate towards other contributors and maintainers.
- Provide clear and detailed descriptions of your changes or additions in your pull request.

By contributing to this project, you are acknowledging and agreeing that your contributions will be licensed under the same license as the original project.

Thank you for considering contributing to this Python Trojan project! Your contributions are valuable and appreciated.

# License

Python-Trojan is released under the GPL-3 License. See `LICENSE` for more information.
