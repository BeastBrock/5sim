import cloudscraper
import json
import discord
import os
import sys
import traceback
import asyncio
import datetime
import colorama

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
        watermark = "created by raibonn2nd#3717"

        # headers = {
        #     "Authorization": "Bearer " + self.bot.get_cog("MongoDB").api_key,
        #     "Content-Type": "application/json",
        # }

        discordbot = commands.Bot(command_prefix=prefix, case_insensitive=True, self_bot=False, intents=discord.Intents.all())
        discordbot.remove_command("help")
        slash = SlashCommand(discordbot, sync_commands=True, sync_on_cog_reload=True)


        def Log(user, command):
            timestamp = str(datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S'))
            print(f"{colorama.Fore.RESET}"
                  f"[{colorama.Fore.GREEN}{timestamp}{colorama.Fore.RESET}] "
                  f"USER {colorama.Fore.YELLOW}{str(user)} {colorama.Fore.RESET}USED THE COMMAND {colorama.Fore.YELLOW}{command}")
            with open('[Data]/logs.txt', 'a', encoding='utf-8') as f: f.write(f'[{timestamp}] USER {str(user)} USED THE COMMAND {command}\n')


        # ------------------------ LOAD COGS ------------------------ #
        if __name__ == '__main__':
            for filename in os.listdir("Cogs"):
                if filename.endswith(".py"):
                    try:
                        discordbot.load_extension(f"Cogs.{filename[:-3]}")
                        print(f"{colorama.Fore.RED}[>] {colorama.Fore.GREEN}Cogs.{filename[:-3]} loaded")
                    except Exception as e:
                        print(f'Failed to load extension {filename}', file=sys.stderr)
                        traceback.print_exc()

            print(f"{colorama.Fore.YELLOW}[>] {colorama.Fore.LIGHTCYAN_EX}Discordbot is ready!")
            discordbot.run(token)

finally:
    conf.close()
