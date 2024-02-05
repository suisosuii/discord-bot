import discord
from discord.ext import commands
from discord import option
import asyncio

class men_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog ready!")
    
    @discord.slash_command(name="hundred", description="指定の人、指定した回数メンションできるよ。たたき起こせ")
    async def hundred(self, ctx, subject: discord.Member=None, times: int=1):
        user = ctx.author
        nickname = user.nick if user.nick else user.name
        messages_to_delete = []
        if(nickname == "緊急地震速報"):
            await ctx.respond("権限が足りないですよ")
        else:
            if times > 0:
                for num in range(times):
                    message = await ctx.send(f'{subject.mention if subject else ""}')
                    messages_to_delete.append(message)

        for message in messages_to_delete:
            await message.delete()
        await ctx.respond(nickname + "に命令されました", delete_after=10)
    
def setup(bot):
    bot.add_cog(men_cog(bot))
