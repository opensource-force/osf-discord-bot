import discord
from discord import Embed
from discord.ext import commands
import google.generativeai as genai


class GeminiWrapper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.embeds = Embeds()

    @commands.hybrid_command()
    async def addapi(self, ctx, api_key):
        genai.configure(api_key=api_key)
        await ctx.send("API has been set")

    @commands.command()
    async def prompt(self, ctx, *args):
        prompt = "".join(map(str, args))
        loading_embed = await self.embeds.loadingEmbed("Generating response")
        message = await ctx.send(embed=loading_embed)

        response = self.model.generate_content(prompt)
        embed = await self.embeds.EmbedMessage(response.text)
        await message.edit(embed=embed)

    @commands.hybrid_command()
    async def sync(self, ctx):
        await ctx.send("Syncing")
        await self.bot.tree.sync(guild=ctx.guild)


class Embeds:
    async def loadingEmbed(self, loading_message):
        ai_embed = Embed(colour=discord.Colour.dark_grey())
        ai_embed.set_author(name="Google Gemini", icon_url="https://developers.google.com/static/focus/images/gemini-icon.png")

        ai_embed.title = loading_message
        ai_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1138172643867111595.gif?size=96&quality=lossless")

        return ai_embed

    async def EmbedMessage(self, message):
        ai_embed = Embed(colour=discord.Colour.dark_grey())
        ai_embed.set_author(name="Google Gemini", icon_url="https://developers.google.com/static/focus/images/gemini-icon.png")

        ai_embed.add_field(name='', value=message, inline=False)

        return ai_embed


async def setup(bot):
    await bot.add_cog(GeminiWrapper(bot))
    print("Gemini Wrapper Loaded")
