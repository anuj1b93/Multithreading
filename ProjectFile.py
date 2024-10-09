import asyncio
import aiohttp
import threading
from time import sleep


URLS = [
    'https://huggingface.co/',
    'https://www.anaconda.com/'
]

async def fetch_url(session, url):
    print(f"Fetching {url}...")
    async with session.get(url) as response:
        data = await response.text()
        print(f"Received data from {url} (Length: {len(data)} chars)")
        return data


async def fetch_all_urls():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in URLS:
            tasks.append(fetch_url(session, url))
        results = await asyncio.gather(*tasks) 
        return results

#  word count
def process_data(data, url):
    print(f"Processing data from {url}...")
    sleep(2) 
    word_count = len(data.split())
    print( f"Processed data from {url}. Word Count: {word_count}\n")

def multi_threaded_processing(results):
    threads = []
    for data, url in results:
        thread = threading.Thread(target=process_data, args=(data, url))
        threads.append(thread)
        thread.start() 
    for thread in threads:
        thread.join() 


async def main():
    results = await fetch_all_urls()

    url_data_pairs = list(zip(results, URLS))

    multi_threaded_processing(url_data_pairs)

# Entry point
if __name__ == '__main__':
    asyncio.run(main())
