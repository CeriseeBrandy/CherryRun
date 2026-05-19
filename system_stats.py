import subprocess
import psutil


class SystemStats:
    def __init__(self):
        psutil.cpu_percent(interval=None)

    def cpu(self):
        return psutil.cpu_percent(interval=None)

    def ram(self):
        return psutil.virtual_memory().percent

    def gpu(self):
        try:
            result = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=utilization.gpu",
                    "--format=csv,noheader,nounits"
                ],
                stderr=subprocess.DEVNULL
            )
            return float(result.decode().strip().split("\n")[0])
        except Exception:
            return None