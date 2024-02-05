import discord
from discord.ext import commands
import asyncio
from discord import option


intents = discord.Intents.default()  # 必要なインテントを含める
# client = commands.Bot(command_prefix="!", intents=intents)
# app_commands.client = client  # コマンドを同期するためにクライアントを設定

# commands.Cogを継承する
class rec_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog ready!")

    @commands.slash_command(name="test", description="テストコマンドなので実行しないでね")
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

    @commands.slash_command(name="reaction", description="アルファベットを指定すればその通りにリアクションをつけるよ")
    @option("message", description="リアクションをつけたいメッセージを右クリックしてメッセージリンクをコピーして張ってね")
    @option("stmp", description="つけたいリアクションをアルファベットで")
    async def reaction(self, interaction: discord.Interaction, message: commands.MessageConverter, stmp: str):
        # 応答を遅延させる
        await interaction.response.defer()
        print(message.id)  # メッセージIDを出力
        msg = await interaction.channel.fetch_message(message.id)
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

    @commands.slash_command(name="cancel", description="このbotがつけたリアクションを取り消せるよ")
    @option("message", description="リアクションを消したいメッセージを右クリックしてメッセージリンクをコピーして張ってね")
    async def cancel(self, interaction: discord.Interaction, message: commands.MessageConverter):
        # 応答を遅延させる
        await interaction.response.defer()
        print(message.id)  # メッセージIDを出力
        msg = await interaction.channel.fetch_message(message.id)
        for reaction in msg.reactions:
            await msg.remove_reaction(reaction.emoji, self.bot.user)
        # エフェメラルメッセージを送信する
        followup_message = await interaction.followup.send("消したよ", ephemeral=True)
        
        # メッセージを後で削除する
        await asyncio.sleep(2)
        await followup_message.delete()

def setup(bot):
    bot.add_cog(rec_cog(bot))

