import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio

client = commands.Bot(command_prefix="--", case_insensitive = True, intents = discord.Intents.all(), activity=discord.Activity(type=discord.ActivityType.playing, name="Made by Barkie & Shturman"))

discord.utils.setup_logging()

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start("PUT BOT TOKEN HERE") #PUT UR BOT TOKEN HERE

asyncio.run(main())