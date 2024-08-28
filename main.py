import discord
import os
from dotenv import load_dotenv
import db,ai 

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()

intents.typing = False
intents.presences = False

# Create the discord.Client instance
client = discord.Client(intents=intents)

# Main event to run the bot
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

def run_bot():
    client.run(BOT_TOKEN)

if __name__ == '__main__':
    run_bot()

