import asyncio
import aiohttp
import time

async def network_load(duration=None):
    """
    Generate network load using fast.com test servers and iperf3 public servers
    """
    # Safe test URLs (CDN-hosted large files)
    test_urls = [
        'https://speed.cloudflare.com/__down',
        'https://speed.hetzner.de/100MB.bin',
        'https://proof.ovh.net/files/100Mb.dat'
    ]

    start_time = time.time()
    chunks = []  # Keep reference to prevent garbage collection

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            # Download tasks
            for url in test_urls:
                tasks.append(asyncio.create_task(session.get(url)))
            
            # Process responses
            for response in await asyncio.gather(*tasks, return_exceptions=True):
                if isinstance(response, aiohttp.ClientResponse):
                    chunk = await response.read()
                    chunks.append(chunk)  # Store to prevent immediate cleanup
            
            if duration and time.time() - start_time >= duration:
                break

if __name__ == '__main__':
    try:
        asyncio.run(network_load(30))
    except KeyboardInterrupt:
        pass