
import datetime
from logging import fatal
import discord
import requests
import os
import bs4
import dotenv
from discord.ext import commands
from pycoingecko import CoinGeckoAPI
from requests.models import Response


client = commands.Bot(command_prefix="!")
client.remove_command('help')
dotenv.load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TD_KEY = os.getenv('TD_KEY')


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


def get_stock_price(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TD_KEY}"
    response = requests.get(url).json()
    price = response['price']
    return price


def get_exchange(amount):
    url = f"https://api.twelvedata.com/currency_conversion?symbol=USD/EUR&amount={amount}&apikey={TD_KEY}"
    response = requests.get(url).json()
    price = response['amount']
    return response


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    lookup_url = "https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup"
    embed = discord.Embed(
        colour=discord.Color.greyple()
    )
    embed.set_author(name="Help")
    embed.add_field(name="!coin <name> <currency>",
                    value="Returns the current price of the coin", inline=False)
    embed.add_field(
        name="!enterprise <name> <amount>",
        value=f"You can check the name of the stock on {lookup_url}")
    await ctx.send(embed=embed)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Watching CoinGecko"))
    print('Logged in as')
    print(client.user.name)
    print('------')


@client.command()
async def key(ctx, arg):
    api_key = arg


@client.command()
async def enterprise(ctx, name, amount):
    usd_price = get_stock_price(name) * amount
    eur_price = get_exchange(amount)
    embed_coin = discord.Embed(
        title=f"{name.upper()}", colour=discord.Color.green())
    embed_coin.add_field(name="Price",
                         value=f"{eur_price} " + "€", inline=True)
    await ctx.send(embed=embed_coin)


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
