import numpy as np

def consume_memory_precise(size_in_mb):
    # Using numpy for more precise memory allocation
    bytes_count = size_in_mb * 1024 * 1024  # Convert MB to bytes
    return np.ones(bytes_count, dtype=np.int8)

# Example: Use 5gb of RAM
array = consume_memory_precise(1024*13)
input("Press Enter to release memory...")