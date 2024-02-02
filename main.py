import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
# import asyncio


#from cogs.music import music_cog
#from cogs.util import util_cog
from cogs.reaction import rec_cog
from cogs.mention import men_cog


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        guild_ids = [int(g) for g in os.environ["GUILD_ID"].split(',')]  # 文字列からintに変換
        await self.tree.sync(guild=None)
        for guild_id in guild_ids:
            try:
                guild = self.get_guild(guild_id)
                await self.tree.sync(guild=guild)
            except discord.errors.Forbidden:
                print(f"Guild {guild_id} is not found.")


load_dotenv()

bot = MyBot()


bot.add_cog(rec_cog(bot))
bot.add_cog(men_cog(bot))
keep_alive()
bot.run(os.environ["TOKEN"] or "")

