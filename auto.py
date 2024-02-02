import asyncio
import aiohttp
import time

async def access_website(session, url):
    async with session.get(url) as response:
        return await response.text()

async def schedule_access(url, interval):
    async with aiohttp.ClientSession() as session:
        while True:
            print(f"Accessing {url}...")
            content = await access_website(session, url)
            print(f"Accessed {url}.")
            await asyncio.sleep(interval)

url = "https://dis-bot-tnme.onrender.com/"  # アクセスしたいウェブサイトのURL
interval = 300  # 5分を秒単位で表したもの

loop = asyncio.get_event_loop()
loop.run_until_complete(schedule_access(url, interval))
