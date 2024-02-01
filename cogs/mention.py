import discord
from discord.ext import commands
import asyncio

class men_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog ready!")
    
    @discord.slash_command(name="hundred")
    async def hundred(self, ctx, subject: discord.Member=None, times: int=1):
        user = ctx.author
        nickname = user.nick if user.nick else user.name
        messages_to_delete = []
        if(nickname == "緊急地震速報"):
            await ctx.send("おわったああああ")
            return
        elif(nickname == "八方ブス"):
            await ctx.send("ゲーセン連れてって")
            return
        elif(nickname == "PAYDAYぶどう"):
            await ctx.send("詐欺に気を付けようね")
            return
        elif(nickname == "SMILE-UP."):
            await ctx.send("ずんだもん = SMILE-UP.")
            return
        else:
            if times > 0:
                for num in range(times):
                    message = await ctx.send(f'{subject.mention if subject else ""}')
                    messages_to_delete.append(message)

        for message in messages_to_delete:
            await message.delete()
        await ctx.send(nickname + "に命令されました", delete_after=10)
    
def setup(bot):
    bot.add_cog(men_cog(bot))
