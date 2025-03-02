import time
import multiprocessing
import threading

def cpu_load(target_percent, duration=None, stop_event=None):
    """
    Generate CPU load for a specified percentage
    
    Args:
        target_percent (float): CPU load percentage (0-100)
        duration (float): Duration in seconds, None for indefinite
        stop_event (multiprocessing.Event): Event to stop the load
    """
    start_time = time.time()
    while True:
        if stop_event and stop_event.is_set():
            break
            
        # Calculate work/sleep ratio
        work_time = 0.1 * (target_percent / 100)
        sleep_time = 0.1 - work_time
        
        # Do useless work
        end_time = time.time() + work_time
        while time.time() < end_time:
            _ = 1 + 1
            
        # Sleep to achieve target percentage
        time.sleep(max(0, sleep_time))
        
        # Check duration
        if duration and time.time() - start_time >= duration:
            break

class CPULoader:
    def __init__(self):
        self.processes = []
        self.stop_event = multiprocessing.Event()
        
    def start(self, target_percent, duration=None):
        self.stop_event.clear()
        cores = multiprocessing.cpu_count()
        for _ in range(cores):
            p = multiprocessing.Process(
                target=cpu_load, 
                args=(target_percent, duration, self.stop_event)
            )
            p.start()
            self.processes.append(p)
            
    def stop(self):
        self.stop_event.set()
        for p in self.processes:
            p.terminate()
            p.join()
        self.processes.clear()