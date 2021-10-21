from main import commands
from main import requests
from main import discord
from main import watermark
from main import json


from discord_slash import cog_ext
from Cogs.setapi import api_keys_collection

class Cryptoprice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="crypto", description="Converts 1 Bitcoin & 1 Litecoin in Rubel (Russian Currency)")
    async def cryptoprice(self, ctx):
        Log(ctx.message.author, 'cryptoprice')
        await ctx.defer(hidden=True)

        try:
            result = api_keys_collection.find_one({"_id": ctx.author.id})
            getapi = result.get("API Key")

            headers = {
                "Authorization": "Bearer " + getapi,
                "Content-Type": "application/json",
            }

            response = requests.get("https://5sim.net/v1/user/payment/crypto/rates?currency=RUB", headers=headers)
            bitcoin = response.json()["BTC"]
            litecoin = response.json()["LTC"]
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            if response.status_code == 200:
                embed = discord.Embed(title="Cryptoprice", description="", colour=discord.Colour.green())
                embed.add_field(name="1 Bitcoin converted to Rubel\n (russian currency)", value=bitcoin)
                embed.add_field(name="1 Litecoin converted to Rubel\n  (russian currency)", value=litecoin)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

            if response.status_code == 401:
                embed.add_field(name="[401] Unauthorized", value="Invalid API Key detected => update your API Key please!")
                await ctx.send(embed=embed, hidden=True)

            if response.status_code == 429:
                embed.add_field(name="[429] Unauthorized", value="You are being rate limited => wait minimum 5 seconds!")
                await ctx.send(embed=embed, hidden=True)

        except AttributeError:
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[401] Unauthorized", value="You cant use any command until you have set your API Key using /setapi")
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed, hidden=True)

        except Exception:
            raise Exception

def setup(bot):
    bot.add_cog(Cryptoprice(bot))