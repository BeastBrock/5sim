import discord
from main import commands
from main import MP_Error
from main import MRA_Error
from main import watermark
from main import requests

from discord_slash import cog_ext
from Cogs.setapi import api_keys_collection

class ban_activation_number(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="banorder", description="ban a ordered number (useful if the number is invalid)")
    async def ban_order(self, ctx, order_id):
        try:
            await ctx.defer(hidden=True)
            result = api_keys_collection.find_one({"_id": ctx.author.id})
            getapi = result.get("API Key")

            headers = {
                "Authorization": "Bearer " + getapi,
                "Content-Type": "application/json",
            }

            ban_response = requests.get(f"https://5sim.net/v1/user/ban/{order_id}", headers=headers)
            if ban_response.status_code == 200:
                embed = discord.Embed(title="Successfully", description="", colour=discord.Colour.green())

                embed.add_field(name="[200] Order Status", value="The Order has been **banned** successfully!")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

        except AttributeError:
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[401] Unauthorized", value="You cant use any command until you have set your API Key using /setapi")
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed, hidden=True)

        except Exception:
            raise Exception

    @ban_order.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MP_Error):
            pass

        elif isinstance(error, MRA_Error):
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[400] Missing Argument", value="`Order ID` is a required Argument that is Missing!")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed, hidden=True)


def setup(bot):
    bot.add_cog(ban_activation_number(bot))