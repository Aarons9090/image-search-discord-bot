import shutil
import discord
import requests
from bs4 import BeautifulSoup
from dotenv import dotenv_values


config = dotenv_values(".env")

# intents to allow messages
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith("!search"):
        search_param = message.content[7:]

        # Bing image search with param
        url = f"https://www.bing.com/images/search?q={search_param}&form=QBLH&sp=-1&pq=app&sc=10-3&qs=n&cvid=7111DC10866B44CAA36869F45AF74A90&ghsh=0&ghacc=0&first=1&tsc=ImageHoverTitle"
        search_response = requests.get(url, stream=True)

        # parse image link from response
        soup = BeautifulSoup(search_response.content, "html.parser")
        element = str(
            soup.select("#mmComponent_images_2 > ul:nth-child(1) > li:nth-child(1) > div > div.imgpt > a > div > img"))

        # indexing string
        url_start = element.find("https")
        url_end = element[url_start:].find('"')
        image_url = element[url_start: url_start + url_end]

        # download image
        image_response = requests.get(image_url, stream=True)
        with open('img.png', 'wb') as out_file:
            shutil.copyfileobj(image_response.raw, out_file)

        # send image
        with open("img.png", "rb") as f:
            pic = discord.File(f)
            await message.channel.send(file=pic)
        del image_response


client.run(config.get("TOKEN"))
