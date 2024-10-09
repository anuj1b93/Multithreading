import asyncio
import aiohttp
import threading
from time import sleep

# Sample list of URLs to fetch
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

# fetch  all data concurrently
async def fetch_all_urls():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in URLS:
            tasks.append(fetch_url(session, url))
        results = await asyncio.gather(*tasks)  # Fetch all URLs concurrently
        return results

# CPU-bound task: Simulate processing of data (e.g., word count)
def process_data(data, url):
    print(f"Processing data from {url}...")
    sleep(2)  # Simulate a long-running task
    word_count = len(data.split())
    print( f"Processed data from {url}. Word Count: {word_count}\n")

# Function to process data using multithreading
def multi_threaded_processing(results):
    threads = []
    for data, url in results:
        thread = threading.Thread(target=process_data, args=(data, url))
        threads.append(thread)
        thread.start()  # Start the thread for each processing task

    for thread in threads:
        thread.join()  # Wait for all threads to finish

# Main function to orchestrate async fetching and multithreaded processing
async def main():
    # Fetch all URLs asynchronously
    results = await fetch_all_urls()

    # Pair each URL with its corresponding data
    url_data_pairs = list(zip(results, URLS))

    # Process the fetched data using multithreading
    multi_threaded_processing(url_data_pairs)

# Entry point
if __name__ == '__main__':
    # Run the async main function using asyncio event loop
    asyncio.run(main())
