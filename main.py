
import datetime
import discord
import requests
import os
import bs4
import dotenv
from discord.ext import commands
from pycoingecko import CoinGeckoAPI


client = commands.Bot(command_prefix="!")
client.remove_command('help')
dotenv.load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


def get_image(symbol, coin):
    sl = symbol.upper()
    s = requests.get("https://www.coingecko.com")
    soup = bs4.BeautifulSoup(s.text, "html.parser")
    image = soup.find("img", {"alt": {f"{coin} ({sl})"}})["data-src"]
    return image


def get_crypto_price(name, currency):
    r = CoinGeckoAPI().get_price(ids=name, vs_currencies=currency,
                                 include_market_cap='true', include_24hr_vol='true', include_24hr_change='true')
    return r


def get_lista():
    cg = CoinGeckoAPI()
    lista = cg.get_coins_list()
    return lista


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour=discord.Color.greyple()
    )
    embed.set_author(name="Help")
    embed.add_field(name="!coin <name> <currency>",
                    value="Returns the current price of the coin")

    await ctx.send(embed=embed)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Watching CoinGecko"))
    # here you can change the discord bot presence text
    print('Logged in as')
    print(client.user.name)
    print('------')
    # a few extra informations


@client.command()
async def key(ctx, arg):
    api_key = arg
    # !key gets removed to store the string for your key. Now you can make the request with it.


@client.command()
async def hola(ctx):
    await ctx.send("Hola, recuerda Pacho es el mejor")


@client.command()
async def coin(ctx, name, currency):
    list = get_lista()
    dict_id = next(item for item in list if item["id"] == f"{name}")
    symbol = dict_id['symbol']
    image = get_image(symbol, name)
    r = get_crypto_price(name, currency)
    clave = r[f'{name}']
    price = clave[f"{currency}"]
    market_cap = clave[f"{currency}_market_cap"]
    volume = clave[f"{currency}_24h_vol"]
    change = clave[f"{currency}_24h_change"]
    embed_coin = discord.Embed(
        title=f"{name.upper()}", colour=discord.Color.orange())
    embed_coin.timestamp = datetime.datetime.utcnow()
    embed_coin.set_thumbnail(url=image)
    embed_coin.add_field(name="Price",
                         value=f"{price}", inline=True)
    embed_coin.add_field(name="24H Change",
                         value=f"{change}", inline=True)
    embed_coin.add_field(name="Market Cap",
                         value=f"{market_cap}", inline=False)
    embed_coin.add_field(name="24H Volume",
                         value=f"{volume}", inline=False)
    await ctx.send(embed=embed_coin)


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


client.run(DISCORD_TOKEN)
# runs your discord bot
