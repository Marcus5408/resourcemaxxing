import torch
import time

def gpu_load(duration=None):
    """
    Generate constant GPU load using parallel streams and continuous computation
    """
    if not torch.cuda.is_available():
        raise RuntimeError("No CUDA-capable GPU detected")

    # Create multiple CUDA streams for parallel execution
    streams = [torch.cuda.Stream() for _ in range(4)]
    size = 2500
    num_matrices = 8
    start_time = time.time()

    # Pre-allocate matrices with different sizes
    matrices = [torch.randn(size, size, device='cuda') for _ in range(num_matrices)]
    
    # Disable auto-tuning to prevent optimization
    torch.backends.cudnn.benchmark = False
    
    while True:
        for stream_idx, stream in enumerate(streams):
            with torch.cuda.stream(stream):
                for i in range(num_matrices):
                    # Complex chain of operations
                    matrices[i] = torch.matmul(matrices[i], matrices[(i + 1) % num_matrices])
                    matrices[i] = torch.nn.functional.relu(matrices[i])
                    matrices[i] = torch.sqrt(torch.abs(matrices[i]) + 1e-8)
                    matrices[i] = torch.tanh(matrices[i])

        # Ensure all streams are synchronized
        for stream in streams:
            stream.synchronize()
            
        if duration and time.time() - start_time >= duration:
            break

if __name__ == '__main__': 
    try:
        torch.cuda.set_device(0)  # Ensure primary GPU is used
        gpu_load(30)
    except KeyboardInterrupt:
        torch.cuda.empty_cache()