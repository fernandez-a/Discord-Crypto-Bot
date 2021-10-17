
from inspect import signature
import json
from re import I
from discord.errors import InvalidArgument
from discord.http import json_or_text
from discord.utils import parse_time
import requests
import bs4
from pycoingecko import CoinGeckoAPI


def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


r = CoinGeckoAPI().get_price(ids='bitcoin', vs_currencies='eur',
                             include_market_cap='true', include_24hr_vol='true', include_24hr_change='true')

currency = 'eur'
clave = r['bitcoin']
id = list(r.keys())[0]
volume = clave[f"{currency}_market_cap"]
cg = CoinGeckoAPI()
s = requests.get("https://www.coingecko.com")

soup = bs4.BeautifulSoup(s.text, "html.parser")

image = soup.find("img", {"alt": "bitcoin (BTC)"})

s = cg.get_coins_list()


btc = next(item for item in s if item["id"] == "bitcoin")


def get_lista():
    cg = CoinGeckoAPI()
    lista = cg.get_coins_list()
    return lista


def get_image(symbol):
    sl = symbol['symbol'].upper()
    s = requests.get("https://www.coingecko.com")
    soup = bs4.BeautifulSoup(s.text, "html.parser")
    image = soup.find("img", {"alt": {f"bitcoin ({btc.upper()})"}})["data-src"]
    print(image)


lista = get_lista()
print(lista)
