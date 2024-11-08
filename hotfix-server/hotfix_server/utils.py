import subprocess


def get_gpu_info_linux():
    try:
        command = "lspci | grep -i vga"
        result = subprocess.check_output(command, shell=True).decode()
        gpus = [{"name": line.strip()} for line in result.splitlines()]
        return gpus
    except Exception as e:
        return str(e)

def get_gpu_info_windows():
    try:
        command = "wmic path win32_videocontroller get caption, adapterram"
        result = subprocess.check_output(command, shell=True).decode()
        gpus = []
        for line in result.splitlines()[1:]:
            if line.strip():
                gpu_info = line.split()
                gpus.append({"name": gpu_info[0], "memory_total": int(gpu_info[1]) / (1024**2)})  # MB to GB
        return gpus
    except Exception as e:
        return str(e)
