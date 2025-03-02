import time
import multiprocessing

def cpu_load(target_percent, duration=None):
    """
    Generate CPU load for a specified percentage
    
    Args:
        target_percent (float): CPU load percentage (0-100)
        duration (float): Duration in seconds, None for indefinite
    """
    start_time = time.time()
    while True:
        # Calculate work/sleep ratio
        work_time = 0.01 * (target_percent / 100)
        sleep_time = 0.01 - work_time
        
        # Do useless work
        end_time = time.time() + work_time
        while time.time() < end_time:
            _ = 1 + 1
            
        # Sleep to achieve target percentage
        time.sleep(max(0, sleep_time))
        
        # Check duration
        if duration and time.time() - start_time >= duration:
            break

# Example usage for 50% CPU load for 10 seconds
if __name__ == '__main__':
    # Use multiple cores
    cores = multiprocessing.cpu_count()
    processes = []
    target_percent = 50  # Set CPU load to 50%
    for _ in range(cores):
        p = multiprocessing.Process(target=cpu_load, args=(target_percent,))
        p.start()
        processes.append(p)