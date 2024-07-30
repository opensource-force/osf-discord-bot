import asyncio
import logging
import logging.handlers
from collections.abc import Generator
from datetime import datetime
from pathlib import Path

import discord
from discord.ext import commands

from bot import CustomBot

from ruamel.yaml import YAML

from config import Config


logging.basicConfig(level=logging.INFO)


def extensions() -> Generator[str, None, None]:
    files = Path("cogs").rglob("*.py")
    for file in files:
        yield (file
               .as_posix()[:-3]
               .replace("/", "."))


def get_config() -> Config:
    with (open("configs/config.yaml", "r") as f,
          open("configs/secrets.yaml", "r") as f2):
        yaml = YAML(typ='safe')
        return Config(yaml.load(f), yaml.load(f2))


intents = discord.Intents.all()

bot = CustomBot(
    commands.when_mentioned,
    config=get_config(),
    initial_extensions=extensions(),
    intents=intents
)


@bot.event
async def on_ready():
    print('---------------------------')
    print(datetime.now())
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('---------------------------')

    await bot.change_presence(status=discord.Status.online,
                              activity=discord.CustomActivity(
                                  bot.config.resolve("discord",
                                                     "activity_text",
                                                     default="Watching over the community")
                              ))


# Adapted from https://github.com/Rapptz/discord.py/blob/v2.4.0/examples/advanced_startup.py
async def main():
    # 1. logging

    # for this example, we're going to set up a rotating file logger.
    # for more info on setting up logging,
    # see https://discordpy.readthedocs.io/en/latest/logging.html and https://docs.python.org/3/howto/logging.html

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Alternatively, you could use:
    # discord.utils.setup_logging(handler=handler, root=False)

    # One of the reasons to take over more of the process though
    # is to ensure use with other libraries or tools which also require their own cleanup.

    # 2. We become responsible for starting the bot.

    async with bot:
        await bot.start(bot.config["discord"]["token"])


# For most use cases, after defining what needs to run, we can just tell asyncio to run it:
if __name__ == '__main__':
    asyncio.run(main())
