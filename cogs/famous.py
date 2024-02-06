import discord
from discord.ext import commands
from discord import option
import asyncio

# ファイルを書き込みモードで開く（'a'）
def write(meigen, person):
    with open("./cogs/meigen/" + person +".txt", 'a') as f:
        f.write(str(line_count("./cogs/meigen/" + person +".txt")) +":"+meigen + "\n")

# ファイルを書き込みモードで開く（'a'）
def create(person):
    with open("./cogs/meigen/" + person +".txt", 'w') as f:
        f.write("")

def read_line(person,line):
    try:
        with open("./cogs/meigen/" + person +".txt", 'r') as f:
            lines = f.readlines()
            if line <= len(lines):
                return lines[line - 1].strip()  # リストは0から始まるため、1を引く
            else:
                return "エラー：指定された行は存在しません。"
    except PermissionError:
        return "エラー：ファイルの読み込み権限がありません。"

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
            return sum(1 for line in f) + 1
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

    @discord.slash_command(name="famous_line", description="名言を読み込むよ")
    async def famous_line(self, ctx, member: discord.Member, line=int):
        await ctx.respond(member.name+"の名言\n"+read_line(member.name,line))

    @discord.slash_command(name="famous_file", description="名言をテキストファイルとして出力するよ")
    async def famous_file(self, ctx, member: discord.Member):
        await ctx.respond(file=discord.File("./cogs/meigen/" + member.name +".txt"))

    @discord.slash_command(name="crt_file", description="管理者用ファイル生成コマンド。使わないでね。")
    async def crt_file(self, ctx):
        for member in ctx.guild.members:
            create(member.name)

def setup(bot):
    bot.add_cog(fom_cog(bot))