import cloudscraper
import json
import discord
import os
import sys
import traceback
import asyncio
import time

from colorama import Fore
from discord.ext import commands
from discord.ext.commands import MissingPermissions as MP_Error
from discord.ext.commands import MissingRequiredArgument as MRA_Error
from discord_slash import SlashCommand, SlashContext


try:
    with open("config.json") as conf:
        config = json.load(conf)
        requests = cloudscraper.create_scraper()
        prefix = config.get("Discordbot Prefix")
        token = config.get("Discordbot Token")
        watermark = "created by ★MoneyDrop★#2921"

        # headers = {
        #     "Authorization": "Bearer " + self.bot.get_cog("MongoDB").api_key,
        #     "Content-Type": "application/json",
        # }

        discordbot = commands.Bot(command_prefix=prefix, case_insensitive=True, self_bot=False, intents=discord.Intents.all())
        discordbot.remove_command("help")
        # guild_slash_ids = [850380692583481365]
        slash = SlashCommand(discordbot, sync_commands=True, sync_on_cog_reload=True)

        # ------------------------ LOAD COGS ------------------------ #
        if __name__ == '__main__':
            for filename in os.listdir("Cogs"):
                if filename.endswith(".py"):
                    try:
                        discordbot.load_extension(f"Cogs.{filename[:-3]}")
                        print(f"{Fore.RED}[>] {Fore.GREEN}Cogs.{filename[:-3]} loaded")
                    except Exception as e:
                        print(f'Failed to load extension {filename}', file=sys.stderr)
                        traceback.print_exc()

            print(f"{Fore.YELLOW}[>] {Fore.LIGHTCYAN_EX}Discordbot is ready!")
            discordbot.run(token)
        config.close()

except Exception: raise Exception
