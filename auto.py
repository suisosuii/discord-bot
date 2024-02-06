import asyncio
import aiohttp
import time

async def access_website(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"An error occurred while accessing {url}: {e}")
        return None

async def schedule_access(url, interval):
    async with aiohttp.ClientSession() as session:
        while True:
            print(f"Accessing {url}...")
            content = await access_website(session, url)
            if content is not None:
                print(f"Accessed {url}.")
            await asyncio.sleep(interval)

url = "https://dis-bot-666s.onrender.com"  # アクセスしたいウェブサイトのURL
interval = 600  #10分

async def auto():
    await schedule_access(url, interval)
