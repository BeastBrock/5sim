from main import commands
from main import requests
from main import json
from main import discord
from main import watermark

from discord_slash import cog_ext
from Cogs.setapi import api_keys_collection

class payment_history(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="paymenthistory", description="shows Informations about the last 5sim topup you made")
    async def payment_history(self, ctx):
        try:
            await ctx.defer(hidden=True)
            result = api_keys_collection.find_one({"_id": ctx.author.id})
            getapi = result.get("API Key")

            headers = {
                "Authorization": "Bearer " + getapi,
                "Content-Type": "application/json",
            }

            response = requests.get("https://5sim.net/v1/user/payments", headers=headers)
            data_id = response.json()["Data"][0]["ID"]
            data_type = response.json()["Data"][0]["TypeName"]
            data_provider = response.json()["Data"][0]["ProviderName"]
            data_amount = response.json()["Data"][0]["Amount"]
            data_founds = response.json()["Data"][0]["Balance"]
            data_date = response.json()["Data"][0]["CreatedAt"]
            data_total = response.json()["Total"]
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())

            if response.status_code == 200:
                embed = discord.Embed(title="Successfully", description="", colour=discord.Colour.green())
                embed.add_field(name="Payment history ID", value=data_id)
                embed.add_field(name="Payment history provider", value=data_provider)
                embed.add_field(name="Payment history type", value=data_type)
                embed.add_field(name="Payment history amount", value=data_amount)
                embed.add_field(name="Payment history founds", value=data_founds)
                embed.add_field(name="Payment history date", value=data_date)
                embed.add_field(name="Payment history total transactions", value=data_total)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

            if response.status_code == 401:
                embed.add_field(name="[401] Unauthorized", value="Invalid API Key detected => update your API Key please!")
                embed.set_footer(text=watermark)
                await ctx.send( embed=embed, hidden=True)

            if response.status_code == 429:
                embed.add_field(name="[429] Unauthorized", value="You are being rate limited => wait minimum 5 seconds!")
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

        except AttributeError:
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[401] Unauthorized", value="You cant use any command until you have set your API Key using /setapi")
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed, hidden=True)

        except Exception:
            raise Exception


def setup(bot):
    bot.add_cog(payment_history(bot))