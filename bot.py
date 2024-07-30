from collections.abc import Iterable

import discord
from aiohttp import ClientSession
from discord.ext import commands

from config import Config


class CustomBot(commands.Bot):
    def __init__(
        self,
        *args,
        config: Config | None = None,
        initial_extensions: Iterable[str],
        **kwargs,
    ):

        super().__init__(*args, **kwargs)
        self.config = config
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:
        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those
        # extensions.

        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
                print(f"Loaded {extension}")
            except Exception as ex:
                print(f"Failed to load {extension}: {ex}")

        # In overriding setup hook,
        # we can do things that require a bot prior to starting to process events from the websocket.
        # In this case, we are using this to ensure that once we are connected, we sync for the testing guild.
        # You should not do this for every guild or for global sync, those should only be synced when changes happen.

        if self.config.resolve("discord",
                               "force_sync_with"):
            guild = discord.Object(self.config.resolve("discord",
                                                       "force_sync_with"))
            # We'll copy in the global commands to test with:
            self.tree.copy_global_to(guild=guild)
            # followed by syncing to the testing guild.
            await self.tree.sync(guild=guild)


        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.


