import discord
import logging
from discord import app_commands
import asyncio

TOKEN = 'MTE5Mjg2NzQzNjIzMjQ2MjQxNg.G6Ta7I.ekNHUq_Jjn3wOonmoMd3M6lnCOW56F9Sqe_uAw'  # TOKENを貼り付け
CHANNELID = 1097682587994050603  # チャンネルIDを貼り付け

intents = discord.Intents.default()#適当に。
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()#スラッシュコマンドを同期


@tree.command(name="test",description="msid: massageID  stmp: つけたいリアクション ")
async def test(interaction: discord.Interaction, msid: str, stmp: str):
     # 応答を遅延させる
    await interaction.response.defer()
    channel = client.get_channel(CHANNELID)
    msg = await channel.fetch_message(msid)
    for str in stmp:
        if str.isalpha():
            await msg.add_reaction(chr(0x1F1E6 + ord(str.upper()) - ord('A')))
    # エフェメラルメッセージを送信する
    followup_message = await interaction.followup.send("つけたよ", ephemeral=True)
    
    # メッセージを後で削除する
    await asyncio.sleep(2)
    await followup_message.delete()

@tree.command(name="reaction",description="before: 何個前のメッセージか  stmp: つけたいリアクション ")
async def reaction(interaction: discord.Interaction, before: int, stmp: str):
    # 応答を遅延させる
    await interaction.response.defer()
    channel = client.get_channel(CHANNELID)
    messages = [message async for message in channel.history(limit=before + 1)]
    print(messages[before].id)  # メッセージIDを出力
    msg = await channel.fetch_message(messages[before].id)
    for str in stmp:
        if str.isalpha():
            await msg.add_reaction(chr(0x1F1E6 + ord(str.upper()) - ord('A')))
        elif str == "?":
            await msg.add_reaction("\N{BLACK QUESTION MARK ORNAMENT}")
        elif str == "!":
            await msg.add_reaction("\N{Heavy Exclamation Mark Symbol}")
    # エフェメラルメッセージを送信する
    followup_message = await interaction.followup.send("つけたよ", ephemeral=True)
    
    # メッセージを後で削除する
    await asyncio.sleep(2)
    await followup_message.delete()

@tree.command(name="cancel",description="before: 何個前のメッセージのリアクションを取り消すか")
async def cancel(interaction: discord.Interaction, before: int):
     # 応答を遅延させる
    await interaction.response.defer()
    channel = client.get_channel(CHANNELID)
    messages = [message async for message in channel.history(limit=before + 1)]
    print(messages[before].id)  # メッセージIDを出力
    msg = await channel.fetch_message(messages[before].id)
    for reaction in msg.reactions:
        await msg.remove_reaction(reaction.emoji, client.user)
    # エフェメラルメッセージを送信する
    followup_message = await interaction.followup.send("消したよ", ephemeral=True)
    
    # メッセージを後で削除する
    await asyncio.sleep(2)
    await followup_message.delete()

client.run(TOKEN)
