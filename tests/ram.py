import numpy as np
import psutil

def consume_memory_precise(size_in_mb):
    """
    Safely consume specified amount of RAM
    
    Args:
        size_in_mb (int): Amount of RAM to consume in MB
    Returns:
        numpy.ndarray: Array holding the allocated memory
    """
    # Safety check - don't use more than 80% of available memory
    available = psutil.virtual_memory().available / (1024 * 1024)  # Convert to MB
    safe_limit = min(size_in_mb, available * 0.8)
    
    # Convert MB to bytes
    bytes_count = int(safe_limit * 1024 * 1024)
    
    try:
        return np.ones(bytes_count, dtype=np.int8)
    except MemoryError:
        print(f"Could not allocate {safe_limit}MB, trying half...")
        return consume_memory_precise(safe_limit / 2)

# Remove the test allocation that was causing issues
if __name__ == '__main__':
    # Example usage
    array = consume_memory_precise(1024)  # Try to consume 1GB
    input("Press Enter to release memory...")