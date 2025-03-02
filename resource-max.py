import time
import multiprocessing
import asyncio
import aiohttp
import numpy as np
import torch
from typing import Optional, List

def cpu_worker(target_percent: float, duration: Optional[float]):
    start_time = time.time()
    while True:
        work_time = 0.01 * (target_percent / 100)
        sleep_time = 0.01 - work_time
        
        end_time = time.time() + work_time
        while time.time() < end_time:
            _ = 1 + 1
            
        time.sleep(max(0, sleep_time))
        
        if duration and time.time() - start_time >= duration:
            break

class ResourceMaximizer:
    def __init__(self):
        self.chunks = []  # For network data
        self.matrices = []  # For GPU data
        self.memory_arrays = []  # For RAM data
        self.cpu_processes = []  # For CPU processes

    async def start_network_load(self, duration: Optional[float] = None):
        """Generate network load using test servers"""
        test_urls = [
            'https://speed.cloudflare.com/__down',
            'https://speed.hetzner.de/100MB.bin',
            'https://proof.ovh.net/files/100Mb.dat'
        ]
        
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = [asyncio.create_task(session.get(url)) for url in test_urls]
                for response in await asyncio.gather(*tasks, return_exceptions=True):
                    if isinstance(response, aiohttp.ClientResponse):
                        chunk = await response.read()
                        self.chunks.append(chunk)
                
                if duration and time.time() - start_time >= duration:
                    break

    def start_cpu_load(self, target_percent: float = 90, duration: Optional[float] = None):
        """Start CPU load on all cores"""
        cores = multiprocessing.cpu_count()
        for _ in range(cores):
            p = multiprocessing.Process(target=cpu_worker, args=(target_percent, duration))
            p.start()
            self.cpu_processes.append(p)

    def consume_ram(self, size_in_mb: int):
        """Consume specified amount of RAM"""
        bytes_count = size_in_mb * 1024 * 1024
        array = np.ones(bytes_count, dtype=np.int8)
        self.memory_arrays.append(array)
        return array

    def start_gpu_load(self, duration: Optional[float] = None):
        """Generate GPU load using parallel streams"""
        if not torch.cuda.is_available():
            raise RuntimeError("No CUDA-capable GPU detected")

        torch.cuda.set_device(0)
        streams = [torch.cuda.Stream() for _ in range(4)]
        size = 2500
        num_matrices = 8
        start_time = time.time()

        self.matrices = [torch.randn(size, size, device='cuda') for _ in range(num_matrices)]
        torch.backends.cudnn.benchmark = False
        
        while True:
            for stream in streams:
                with torch.cuda.stream(stream):
                    for i in range(num_matrices):
                        self.matrices[i] = torch.matmul(self.matrices[i], 
                                                      self.matrices[(i + 1) % num_matrices])
                        self.matrices[i] = torch.nn.functional.relu(self.matrices[i])
                        self.matrices[i] = torch.sqrt(torch.abs(self.matrices[i]) + 1e-8)
                        self.matrices[i] = torch.tanh(self.matrices[i])

            for stream in streams:
                stream.synchronize()
                
            if duration and time.time() - start_time >= duration:
                break

    def cleanup(self):
        """Clean up all resources"""
        # Stop CPU processes
        for p in self.cpu_processes:
            p.terminate()
            p.join()
        
        # Clear RAM
        self.memory_arrays.clear()
        
        # Clear GPU memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            self.matrices.clear()
        
        # Clear network data
        self.chunks.clear()

async def main():
    maximizer = ResourceMaximizer()
    try:
        # Start all resource loads
        maximizer.start_cpu_load(duration=30)
        maximizer.consume_ram(1024 * 13)  # ~13GB RAM
        await maximizer.start_network_load(duration=30)
        if torch.cuda.is_available():
            maximizer.start_gpu_load(duration=30)
    except KeyboardInterrupt:
        pass
    finally:
        maximizer.cleanup()

if __name__ == '__main__':
    asyncio.run(main())