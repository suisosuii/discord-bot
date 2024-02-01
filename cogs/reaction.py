import discord
from discord import commands
from discord.ext import commands as extcommands
import asyncio


intents = discord.Intents.default()  # 必要なインテントを含める
# client = commands.Bot(command_prefix="!", intents=intents)
# app_commands.client = client  # コマンドを同期するためにクライアントを設定

# commands.Cogを継承する
class rec_cog(extcommands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @extcommands.Cog.listener()
    async def on_ready(self):
        print("Cog ready!")

    @commands.application_command(name="test", description="msid: massageID  stmp: つけたいリアクション ")
    async def test(self, interaction: discord.Interaction, msid: str, stmp: str):
        # 応答を遅延させる
        await interaction.response.defer()
        msg = await interaction.channel.fetch_message(msid)
        for char in stmp:
            if char.isalpha():
                await msg.add_reaction(chr(0x1F1E6 + ord(char.upper()) - ord('A')))
        # エフェメラルメッセージを送信する
        followup_message = await interaction.followup.send("つけたよ", ephemeral=True)
        
        # メッセージを後で削除する
        await asyncio.sleep(2)
        await followup_message.delete()

    @commands.application_command(name="reaction", description="before: 何個前のメッセージか  stmp: つけたいリアクション ")
    async def reaction(self, interaction: discord.Interaction, before: int, stmp: str):
        # 応答を遅延させる
        await interaction.response.defer()
        messages = [message async for message in interaction.channel.history(limit=before + 1)]
        print(messages[before].id)  # メッセージIDを出力
        msg = await interaction.channel.fetch_message(messages[before].id)
        for char in stmp:
            if char.isalpha():
                await msg.add_reaction(chr(0x1F1E6 + ord(char.upper()) - ord('A')))
            elif char == "?":
                await msg.add_reaction("\N{BLACK QUESTION MARK ORNAMENT}")
            elif char == "!":
                await msg.add_reaction("\N{Heavy Exclamation Mark Symbol}")
        # エフェメラルメッセージを送信する
        followup_message = await interaction.followup.send("つけたよ", ephemeral=True)
        
        # メッセージを後で削除する
        await asyncio.sleep(2)
        await followup_message.delete()

    @commands.application_command(name="cancel", description="before: 何個前のメッセージのリアクションを取り消すか")
    async def cancel(self, interaction: discord.Interaction, before: int):
        # 応答を遅延させる
        await interaction.response.defer()
        messages = [message async for message in interaction.channel.history(limit=before + 1)]
        print(messages[before].id)  # メッセージIDを出力
        msg = await interaction.channel.fetch_message(messages[before].id)
        for reaction in msg.reactions:
            await msg.remove_reaction(reaction.emoji, self.bot.user)
        # エフェメラルメッセージを送信する
        followup_message = await interaction.followup.send("消したよ", ephemeral=True)
        
        # メッセージを後で削除する
        await asyncio.sleep(2)
        await followup_message.delete()

def setup(bot):
    bot.add_cog(rec_cog(bot))

