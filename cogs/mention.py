import discord
from discord import commands
from discord.ext import commands as extcommands
import asyncio

class men_cog(extcommands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @extcommands.Cog.listener()
    async def on_ready(self):
        print("Cog ready!")
    
    @commands.application_command(name="hundred", description="subject: メンション対象   times: 回数 ")
    async def hundred(self, interaction: discord.Interaction, subject: discord.Option(discord.Member, "メンション対象")="<@584021152176013333>", times: discord.Option(int,"回数") = 1):
        await interaction.response.defer()
        user = interaction.user
        # ニックネームが設定されていればそれを、そうでなければユーザー名を取得
        nickname = user.nick if user.nick else user.name
        messages_to_delete = []
        if(nickname == "緊急地震速報"):
            await interaction.send("おわったああああ")
            return
        elif(nickname == "八方ブス"):
            await interaction.send("ゲーセン連れてって")
            return
        elif(nickname == "PAYDAYぶどう"):
            await interaction.send("詐欺に気を付けようね")
            return
        elif(nickname == "SMILE-UP."):
            await interaction.send("ずんだもん = SMILE-UP.")
            return
        # メンバーが見つかった場合はメンションを送信
        else:
            # forループが実行されるかどうかを事前に確認
            if times > 0:
                for num in range(times):
                    message = await interaction.send(f'{subject.mention}')
                    messages_to_delete.append(message.id)

        # for文を回し切った後、保存したメッセージIDを利用して一括で削除
        for message_id in messages_to_delete:
            message = await interaction.fetch_message(message_id)
            await message.delete()
        # エフェメラルメッセージを送信する
        followup_message = await interaction.followup.send(nickname + "に命令されました", ephemeral=True)
    
    
    
def setup(bot):
    bot.add_cog(men_cog(bot))