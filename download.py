import asyncio
import aiohttp
import os
import json
from tqdm.asyncio import tqdm


FOLDER = 'emojis'
os.makedirs(FOLDER, exist_ok=True)


async def download_emoji(session, semaphore, url, progress_bar):
    filename = url.split('/')[-1]
    async with semaphore:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                with open(os.path.join(FOLDER, filename), 'wb') as f:
                    f.write(content)
            else:
                print(f'Failed to download {filename} from {url}')
            progress_bar.update(1)


async def main():
    existing = os.listdir(FOLDER)

    data = json.load(open('metadata.json'))
    urls = set()
    for dp in data['data'].values():
        for combinations in dp['combinations'].values():
            latest = [c for c in combinations if c['isLatest']][0]
            url = latest['gStaticUrl']
            filename = url.split('/')[-1]
            if filename not in existing:
                urls.add(url)

    semaphore = asyncio.Semaphore(8)
    async with aiohttp.ClientSession() as session:
        progress_bar = tqdm(total=len(urls))
        tasks = []
        for url in urls:
            tasks.append(download_emoji(session, semaphore, url, progress_bar))
        await asyncio.gather(*tasks)
        progress_bar.close()


if __name__ == "__main__":
    asyncio.run(main())
