import pymongo
import json
import datetime
from main import commands
from main import requests
from main import json
from main import discord
from main import watermark
from main import Log
from main import colorama
from discord_slash import cog_ext


with open("config.json") as conf:
    config = json.load(conf)
    url = config.get("Database url")
    databasename = config.get("Database Name")
    myclient = pymongo.MongoClient(url, ssl=True, ssl_ca_certs="cacert.pem")
    mydb = myclient[databasename]
    dblist = myclient.list_database_names()
    api_keys_collection = mydb["API Keys"]

class mongodb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = None

    @cog_ext.cog_slash(name="setapi")
    async def set_apikey(self, ctx, api_key):
        Log(ctx.author, 'setapi')
        try:
            self.key = api_key
            headers = {
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json",
            }

            response = requests.get("https://5sim.net/v1/user/profile", headers=headers)
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            await ctx.defer(hidden=True)
            if response.status_code == 200:
                time = datetime.datetime.now()
                timeformat = time.strftime("%Y-%m-%d %H:%M:%S")
                mongodb_postdata = {"_id": ctx.author.id, "Username": ctx.author.name + "#" + ctx.author.discriminator, "Date": timeformat, "API Key": api_key}

                if ctx.author.id not in mongodb_postdata:
                    api_keys_collection.insert_one(mongodb_postdata)

                embed = discord.Embed(title="Successfully", description="", colour=discord.Colour.green())
                embed.add_field(name="[200] Request Successful", value="Your API Key has been stored using Advanced Encryption Standard!")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

            if response.status_code == 401:
                embed.add_field(name="[401] Unauthorized", value="Invalid API Key detected\n => you only can set valid ones!")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

            if response.status_code == 429:
                embed.add_field(name="[429] Unauthorized", value="You are being rate limited => wait minimum 5 seconds!")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=watermark)
                await ctx.send(embed=embed, hidden=True)

        except pymongo.errors.DuplicateKeyError:
            embed = discord.Embed(title="Request Error", description="", colour=discord.Colour.red())
            embed.add_field(name="[401] Unauthorized", value="Your API Key is already set so you are not able to set it again!")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=watermark)
            await ctx.send(embed=embed, hidden=True)

def setup(bot):
    bot.add_cog(mongodb(bot))