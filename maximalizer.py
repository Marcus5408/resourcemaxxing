import time
import multiprocessing
import asyncio
import aiohttp
import numpy as np
import torch
import os
from typing import Optional, List
from tests.cpu import cpu_load  # Import the CPU load function
from tests.gpu import cuda_load, mps_load  # Import the GPU load functions
from tests.net import network_load  # Import the network load function
from tests.ram import consume_memory_precise  # Import the RAM load function


class ResourceMaximizer:
    def __init__(self):
        self.chunks = []  # For network data
        self.matrices = []  # For GPU data
        self.memory_arrays = []  # For RAM data
        self.cpu_processes = []  # For CPU processes

    async def start_network_load(self, duration: Optional[float] = None):
        """Generate network load using test servers"""
        await network_load(duration)

    def start_cpu_load(
        self, target_percent: float = 90, duration: Optional[float] = None
    ):
        """Start CPU load on all cores"""
        cores = multiprocessing.cpu_count()
        for _ in range(cores):
            p = multiprocessing.Process(
                target=cpu_load, args=(target_percent, duration)
            )
            p.start()
            self.cpu_processes.append(p)

    def start_gpu_load(self, duration: Optional[float] = None):
        """Generate GPU load using parallel streams"""
        if torch.cuda.is_available():
            cuda_load(duration)
        elif torch.backends.mps.is_available():
            mps_load(duration)
        else:
            raise RuntimeError("No compatible GPU detected")

    def consume_ram(self, size_in_mb: int):
        """Consume specified amount of RAM"""
        array = consume_memory_precise(size_in_mb)
        self.memory_arrays.append(array)
        return array

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

    async def run_basic(self, tier: int):
        """Run a specific tier of the test"""
        tiers = {
            1: {"cpu": 50, "ram": 1024, "network": 10, "gpu": 10},
            2: {"cpu": 70, "ram": 2048, "network": 20, "gpu": 20},
            3: {"cpu": 85, "ram": 4096, "network": 30, "gpu": 30},
            4: {"cpu": 95, "ram": 8192, "network": 40, "gpu": 40},
            5: {"cpu": 100, "ram": 16384, "network": 50, "gpu": 50},
        }

        config = tiers[tier]
        try:
            self.start_cpu_load(
                target_percent=config["cpu"], duration=config["network"]
            )
            self.start_gpu_load(duration=config["gpu"])
            self.consume_ram(config["ram"])
            await self.start_network_load(duration=config["network"])
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    # support for running the test advanced (custom configuration)
    async def run_advanced(self, cpu: int, ram: int, network: int, gpu: int, disk: int):
        """Run a custom configuration of the test"""
        try:
            self.start_cpu_load(target_percent=cpu, duration=network)
            self.start_gpu_load(duration=gpu)
            self.consume_ram(ram)
            await self.start_network_load(duration=network)
            self.start_disk_load(disk, duration=network)
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    def start_disk_load(self, size_in_mb: int, duration: Optional[float] = None):
        """Generate disk load by writing and reading a file"""
        file_path = "/tmp/disk_load_test"
        data = b"0" * (size_in_mb * 1024 * 1024)
        start_time = time.time()

        while True:
            with open(file_path, "wb") as f:
                f.write(data)
            with open(file_path, "rb") as f:
                _ = f.read()

            if duration and time.time() - start_time >= duration:
                break

        # Clean up the file after the test
        try:
            os.remove(file_path)
        except OSError:
            pass


async def main():
    maximizer = ResourceMaximizer()
    tier = int(input("Enter test tier (1-5): "))
    await maximizer.run_basic(tier)


if __name__ == "__main__":
    asyncio.run(main())
