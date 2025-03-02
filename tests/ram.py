import numpy as np

def consume_memory_precise(size_in_mb):
    bytes_count = size_in_mb * 1024 * 1024  # Convert MB to bytes
    return np.ones(bytes_count, dtype=np.int8)


array = consume_memory_precise(1024*1024)
input("Press Enter to release memory...")