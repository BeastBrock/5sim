import discord
from main import Log
from main import commands
from main import prefix
from main import watermark
from main import colorama

class help_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("help")
    async def help_command(self, ctx):
        Log(ctx.author, 'help')
        invmention = f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| {ctx.author.mention}"
        embed = discord.Embed(title="Command List", description="",color=discord.Colour.dark_gold())
        embed.add_field(name="Check the API", value=f"{prefix}checkapi\n => check the Status a request to the API and sends the result", inline=False)
        embed.add_field(name="Buy phone number", value=f"{prefix}ordernumber\n => buy a temporary phonenumber from 5sim.net", inline=False)
        embed.add_field(name="Check the Order", value=f"{prefix}checkorder\n => get the order status & verification-code", inline=False)
        embed.add_field(name="Finish the Order", value=f"{prefix}finishorder\n => Finish the Order (useful after reciving the SMS to get a few Founds back)", inline=False)
        embed.add_field(name="Cancel the Order", value=f"{prefix}cancelorder\n => Cancel the bought Order (Useful if the Provider sends no SMS)", inline=False)
        embed.add_field(name="Ban the Order", value=f"{prefix}banorder\n => Ban the bought Number and remove it from 5sim (useful if the phonenumber is invalid)", inline=False)
        embed.add_field(name="Crypto Currency", value=f"{prefix}crypto\n => show LTC & BTC in Rubel (Russia currency)", inline=False)
        embed.add_field(name="Payment History", value=f"{prefix}paymentistory\n => shows Infos about the last topup you made on the Site", inline=False)
        embed.add_field(name="User Informations", value=f"{prefix}userinfo\n => get information's about your 5sim account", inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=watermark)
        await ctx.send(invmention, embed=embed)


def setup(bot):
    bot.add_cog(help_command(bot))