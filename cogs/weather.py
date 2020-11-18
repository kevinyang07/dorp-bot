from discord import Embed
from discord.ext import commands

from requests import get

import os
import dotenv
from dotenv import load_dotenv

load_dotenv()
weatherapi = os.getenv('weather')

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx,  *, location):
        data = get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&APPID={weatherapi}").json()
        cleared_data = {
            'Location:': data['name'],
            'Weather:': f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
            'Temperature:': f"{int((float(data['main']['temp']) * 1.8) + 32)}°F",
            'Feels like:': f"{int((float(data['main']['feels_like']) * 1.8) + 32)}°F",
            'Maximum Temperature for Today:': f"{int((float(data['main']['temp_max']) * 1.8) + 32)}°F",
            'Minimum Temperature for Today:': f"{int((float(data['main']['temp_min']) * 1.8) + 32)}°F",
        }
        embed = Embed(title=f"Weather in: {cleared_data['Location:']}", color=0x3de4ba)
        for key, value in cleared_data.items():
            embed.add_field(name=key, value=value, inline="True")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Weather(bot))
