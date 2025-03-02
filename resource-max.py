import numpy as np
import threading
import time
import asyncio
import gc

class ResourceMaxxer:
    def __init__(self):
        pass
    
    def release_all(self):
        """Release all resources"""
        asyncio.get_event_loop().close()
        gc.collect()
        
        
    async def ram_load(self, bytes_count, duration=30):
        import numpy as np
        import time
        start_time = time.time()
        try:
            while time.time() - start_time < duration:
                array = np.ones(bytes_count, dtype=np.int8)

        except MemoryError:
            print("Memory limit reached")
    
    async def network_load(self, duration=None):
        """Load network resources"""
        import asyncio
        import aiohttp
        import time
        test_urls = [
            'https://speed.cloudflare.com/__down',
            'https://speed.hetzner.de/100MB.bin',
            'https://proof.ovh.net/files/100Mb.dat'
        ]
        start_time = time.time()
        chunks = []
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = []
                for url in test_urls:
                    tasks.append(asyncio.create_task(session.get(url)))
                for response in await asyncio.gather(*tasks, return_exceptions=True):
                    if isinstance(response, aiohttp.ClientResponse):
                        chunk = await response.read()
                        chunks.append(chunk)
                        if duration and time.time() - start_time >= duration:
                            break
                
if __name__ == "__main__":
    rm = ResourceMaxxer()
    ram = 1024*13
    asyncio.run(rm.ram_load(ram))
    asyncio.run(rm.network_load(30))
    rm.release_all()
    