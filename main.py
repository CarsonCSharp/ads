# Import necessary packages
import os
import sys
import json
import asyncio
import platform
import requests
import websockets
from colorama import init, Fore
from keep_alive import keep_alive

# IMPORTANT: The user account takes 2-4 minutes time to go offline after stopping the code.

# Initialize Colorama for terminal text colors
init(autoreset=True)

# User-defined settings
STATUS = "online"  # Set status as "online", "dnd", or "idle"

# Retrieve Discord token from environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print(f"{Fore.RED}[ERROR]{Fore.RESET} Token not found in environment variables. Please add your token in the Secrets tab.")
    sys.exit()

# Define headers for API requests
headers = {"Authorization": TOKEN, "Content-Type": "application/json"}

# Validate the token with a request to Discord's API
validate_response = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers)
if validate_response.status_code != 200:
    print(f"{Fore.RED}[ERROR]{Fore.RESET} Invalid token. Please check and try again.")
    sys.exit()

# Fetch user info
user_info = validate_response.json()
username = user_info["username"]
discriminator = user_info["discriminator"]
user_id = user_info["id"]

async def connect_discord_gateway(token, status):
    async with websockets.connect("wss://gateway.discord.gg/?v=9&encoding=json") as ws:
        # Receive gateway hello event
        hello_event = json.loads(await ws.recv())
        heartbeat_interval = hello_event["d"]["heartbeat_interval"]

        # Authenticate and set user presence (status)
        auth_payload = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": platform.system(),
                    "$browser": "Chrome",
                    "$device": platform.system(),
                },
                "presence": {
                    "status": status,  # Status here, either "online", "idle", or "dnd"
                    "afk": False,
                    "activities": [],
                },
            },
        }
        await ws.send(json.dumps(auth_payload))

        # Set custom status
        status_payload = {
            "op": 3,
            "d": {
                "since": 0,
                "activities": [
                    {
                        "type": 4,
                        "state": CUSTOM_STATUS,
                        "name": "Custom Status",
                        "id": "custom",
                    }
                ],
                "status": status,
                "afk": False,
            },
        }
        await ws.send(json.dumps(status_payload))

        # Send periodic heartbeat
        heartbeat_payload = {"op": 1, "d": None}
        while True:
            await asyncio.sleep(heartbeat_interval / 1000)
            await ws.send(json.dumps(heartbeat_payload))

async def keep_online():
    # Clear terminal based on OS
    os.system("cls" if platform.system() == "Windows" else "clear")

    # Print user info upon login
    print(f"{Fore.GREEN}[INFO]{Fore.RESET} Logged in as {Fore.CYAN}{username}#{discriminator} {Fore.RESET}({user_id})")

    # Keep the connection alive
    while True:
        await connect_discord_gateway(TOKEN, STATUS)
        await asyncio.sleep(50)

# Start the webserver to keep Replit alive
keep_alive()

# Run the asynchronous event loop
asyncio.run(keep_online())
