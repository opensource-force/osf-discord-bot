import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from db import *

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    channel = bot.get_channel(CHANNEL_ID)
    
    if channel:
        print("The osf bot is now up and running")
    else:
        print(f"Channel with ID {CHANNEL_ID} not found.")

@bot.command(name='submit')
async def submit(ctx, name: str = None, link: str = None, *, description: str = None):
    if not name or not description:
        await ctx.send("**Error:** `name`, `link`, and `description` are required to submit a project. Please use the command in the following format:\n"
               "`!submit name=\"Your Project Name\" link=\"Link to the project\" description=\"Project Description\"`")
    else:
        await ctx.send("Adding your project to the database")

        name = name.replace('name=', '').strip()
        description = description.replace('description=', '').strip()
        link = link.replace('link=', '').strip()

        add_project(name,description,link)

        await ctx.send(f"**Project Submitted!**\n"
                   f"**Name:** {name}\n"
                   f"**Description:** {description}\n"
                   f"**Link:** {link}\n"
                   f"Thank you for submitting your project! Your contribution helps others discover new opportunities. The project has been successfully added to the database.")

@bot.command(name='find')
async def search(ctx, *, description : str = None):
    if not description:
        await ctx.send("**Error:** A `description` is required to find a project which is suitable for you. Please use the command in the following format:\n"
                       "`!find description=\"Project Description\"`")
    else:
        await ctx.send("Finding the best project for you from the database")

        project_data = get_project_data(description)

        await ctx.send("\n\n---\n\n".join(project_data))

if __name__ == '__main__':
    bot.run(BOT_TOKEN)

