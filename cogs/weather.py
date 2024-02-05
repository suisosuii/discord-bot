import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
import discord
from discord.ext import commands
from discord import option
import datetime

#いろいろ初期値設定

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

weather_code = {
    0: "晴れ",
    1: "主に晴れ",
    2: "ときどき曇り",
    3: "曇り",
    45: "霧および着氷霧",
    48: "霧および着氷霧",
    51: "霧雨：弱",
    53: "霧雨：中",
    55: "霧雨：強",
    56: "凍結霧雨：弱",
    57: "凍結霧雨：強",
    61: "雨：弱",
    63: "雨：中",
    65: "雨：強",
    66: "凍結雨：弱",
    67: "凍結雨：強",
    71: "雪：弱",
    73: "雪：中",
    75: "雪：強",
    77: "雪粒",
    80: "にわか雨：弱",
    81: "にわか雨：中",
    82: "にわか雨：激しい",
    85: "にわか雪：弱",
    86: "にわか雪：強",
    95: "雷雨：弱または中",
    96: "雷雨：弱で雹を伴う",
    99: "雷雨：強で雹を伴う"
}
weather_icon ={
    0: "🌞：晴れ",
    1: "🌞：主に晴れ",
    2: "🌤：ときどき曇り",
    3: "☁：曇り",
    45: "🌫：霧および着氷霧",
    48: "🌫および着氷霧",
    51: "🌧：霧雨(弱)",
    53: "🌧：霧雨(中)",
    55: "🌧：霧雨(強)",
    56: "🌧：凍結霧雨(弱)",
    57: "🌧：凍結霧雨(強)",
    61: "🌂：雨(弱)",
    63: "☔：雨(中)",
    65: "☔：雨(強)",
    66: "🌂：凍結雨(弱)",
    67: "☔：凍結雨(強)",
    71: "⛄：雪(弱)",
    73: "⛄：雪(中)",
    75: "⛄：雪(強)",
    77: "⛄：雪(粒)",
    80: "🌂：にわか雨(弱)",
    81: "☔：にわか雨(中)",
    82: "☔：にわか雨(激しい)",
    85: "⛄：にわか雪(弱)",
    86: "⛄：にわか雪(強)",
    95: "⛈：雷雨(弱または中)",
    96: "⛈：雷雨(弱で雹を伴う)",
    99: "⛈：雷雨(強で雹を伴う)"
}
# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 35.9565,
	"longitude": 136.1842,
	"daily": "weather_code"
}

def access_website(day):
    responses = openmeteo.weather_api(url, params=params)
    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s"),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["weather_code"] = daily_weather_code
    return daily_weather_code[day]

#ここからdiscord_botの作成
class weat_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog ready!")
    
    @discord.slash_command(name="weather")
    @option("day", description="何日後の天気情報か。今日なら0。デフォルト1,６日後まで取得可能です")
    async def weather(self, ctx,day: int=1):
        dt = datetime.datetime.today()
        dtFix = dt + datetime.timedelta(days=day)
        embed = discord.Embed(
        title=str(dtFix.month) + "月"+ str(dtFix.day) + "日の気象情報",
        description="場所：鯖江市本町",
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="天気", value=weather_icon[access_website(day)], inline=False)
        embed.add_field(name="最高気温", value="℃", inline=True)
        #空フィールドで位置調整
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="最低気温", value="℃", inline=True)

        embed.set_author(name="reaction bot", icon_url="https://github.com/suisosuii/discord-bot/blob/Embed/cogs/png/deth.png?raw=true")
        embed.set_thumbnail(url="https://github.com/suisosuii/discord-bot/blob/Embed/cogs/png/deth.png?raw=true")
        await ctx.respond(embed=embed) # Send the embed with some text
        # if day == 0:
        #     await ctx.send("今日の鯖江市本町の天気は..." + weather_code.get(access_website(day), access_website(day)) + "デス")
        # else:
        #     await ctx.send(str(day) + "日後の鯖江市本町の天気は..." + weather_code.get(access_website(day), access_website(day)) + "デス")
def setup(bot):
    bot.add_cog(weat_cog(bot))


# daily_dataframe = pd.DataFrame(data = daily_data)
# print(daily_dataframe)

