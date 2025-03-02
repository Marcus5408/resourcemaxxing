import torch
import time
import platform

def get_gpu_backend():
    """Detect available GPU backend"""
    if platform.system() == "Windows":
        try:
            import pynvml
            pynvml.nvmlInit()
            return "cuda" if torch.cuda.is_available() else None
        except:
            return None
    else:
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
    return None

def cuda_load(duration=None, stop_event=None):
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
    matrices = [torch.randn(size, size, device="cuda") for _ in range(num_matrices)]

    # Disable auto-tuning to prevent optimization
    torch.backends.cudnn.benchmark = False

    while True:
        if stop_event and stop_event.is_set():
            break

        for stream_idx, stream in enumerate(streams):
            with torch.cuda.stream(stream):
                for i in range(num_matrices):
                    # Complex chain of operations
                    matrices[i] = torch.matmul(
                        matrices[i], matrices[(i + 1) % num_matrices]
                    )
                    matrices[i] = torch.nn.functional.relu(matrices[i])
                    matrices[i] = torch.sqrt(torch.abs(matrices[i]) + 1e-8)
                    matrices[i] = torch.tanh(matrices[i])

        # Ensure all streams are synchronized
        for stream in streams:
            stream.synchronize()

        if duration and time.time() - start_time >= duration:
            break


def mps_load(duration=None, stop_event=None):
    """
    Generate constant GPU load using continuous computation on Apple Silicon
    """
    if not torch.backends.mps.is_available():
        raise RuntimeError("No MPS-capable GPU detected")

    size = 2500
    num_matrices = 8
    start_time = time.time()

    # Pre-allocate matrices with different sizes
    matrices = [torch.randn(size, size, device="mps") for _ in range(num_matrices)]

    while True:
        if stop_event and stop_event.is_set():
            break

        for i in range(num_matrices):
            # Complex chain of operations
            matrices[i] = torch.matmul(matrices[i], matrices[(i + 1) % num_matrices])
            matrices[i] = torch.nn.functional.relu(matrices[i])
            matrices[i] = torch.sqrt(torch.abs(matrices[i]) + 1e-8)
            matrices[i] = torch.tanh(matrices[i])

        if duration and time.time() - start_time >= duration:
            break


def runGPUtest(time=30):
    try:
        backend = get_gpu_backend()
        if backend == "cuda":
            torch.cuda.set_device(0)  # Ensure primary GPU is used
            cuda_load(time)
        elif backend == "mps":
            mps_load(time)
        else:
            print("No compatible GPU found.")
    except KeyboardInterrupt:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


if __name__ == "__main__":
    runGPUtest(30)
