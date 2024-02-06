import discord
from discord.ext import commands
from discord import option
import asyncio

# ファイルを書き込みモードで開く（'a'）
def write(meigen, person):
    with open("./cogs/meigen/" + person +".txt", 'a') as f:
        f.write(str(line_count("./cogs/meigen/" + person +".txt")) +":"+meigen + "\n")


# ファイルを読み込みモードで開く（'r'）して内容を表示
def read(person):
    try:
        with open("./cogs/meigen/" + person +".txt", 'r') as f:
            return f.read()
    except PermissionError:
        return "エラー：ファイルの読み込み権限がありません。"

def line_count(path):
    try:
        with open(path, 'r') as f:
            return sum(1 for line in f)
    except FileNotFoundError:
        return 1

class fom_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog ready!")
    
    @discord.slash_command(name="famous_w", description="名言をファイルに書き込むよ")
    async def famous_w(self, ctx, member: discord.Member, meigen: str):
        write(meigen,member.name)
        await ctx.respond("保存しました。\n"+ member.name + " : " + meigen)

    
    @discord.slash_command(name="famous_r", description="名言を読み込むよ")
    async def famous_r(self, ctx, member: discord.Member):
        await ctx.respond(member.name+"の名言集\n"+read(member.name))
    
def setup(bot):
    bot.add_cog(fom_cog(bot))