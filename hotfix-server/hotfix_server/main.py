'''
by: lei.lei.fam.meng@gmail.com
updated: 20241108
'''

import platform
import psutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
from .utils import get_gpu_info_linux, get_gpu_info_windows
import socket
import subprocess


app = FastAPI()



@app.get("/")
async def root():
    '''
    show machine info(ip, status, cpu, gpu...) and app info(status)
    '''
    return {"machine": "Hello World",
            "app": "run"}
    
@app.get("/get-machine-name")
async def get_machine_name():
    """
    获取当前机器名
    """
    machine_name = socket.gethostname()
    return {"machine_name": machine_name}


@app.put("/rename-machine")
async def rename_machine(new_name: str):
    """
    修改机器名为指定的名称
    """
    current_os = platform.system()

    try:
        # 根据系统选择重命名命令
        if current_os == "Windows":
            # 在 Windows 上重命名机器
            command = ["wmic", "computersystem", "where", "name='%COMPUTERNAME%'", "call", "rename", new_name]
            subprocess.run(command, check=True, shell=True)

        elif current_os == "Linux":
            # 在 Linux 上使用 hostnamectl 进行重命名
            command = ["sudo", "hostnamectl", "set-hostname", new_name]
            subprocess.run(command, check=True)

        else:
            raise HTTPException(status_code=400, detail="不支持的操作系统")

        return {"status": "成功", "new_name": new_name}

    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="重命名失败。需要管理员权限")


@app.get("/app-logs")
async def app_logs():
    '''
    show app logs for some app
    '''
    return {"message": "logs"}

@app.get("/app-version")
async def app_versions():
    '''
    show app logs for some app
    '''
    return {"message": "version"}

@app.get("/app-status")
async def app_status():
    '''
    show app running status
    '''
    return {"message": "status"}

@app.get("/app-settings")
async def app_settings():
    '''
    show app settings
    '''
    return {"message": "status"}


@app.get("/machine-status")
async def machine_status():
    '''
    show machine status
    '''
    return {"message": "machine status"}

@app.get("/machine-info")
async def machine_info():
    # 获取操作系统信息
    os_info = platform.system()

    # 获取内存信息
    memory_info = psutil.virtual_memory()
    total_memory = memory_info.total / (1024 ** 3)  # GB
    available_memory = memory_info.available / (1024 ** 3)  # GB

    # 获取显卡信息
    gpu_info = None
    if os_info == "Windows":
        gpu_info = get_gpu_info_windows()
    elif os_info == "Linux":
        gpu_info = get_gpu_info_linux()

    return {
        "platform": os_info,
        "total_memory_gb": total_memory,
        "available_memory_gb": available_memory,
        "gpu_info": gpu_info
    }

@app.get("/machine-settings")
async def machine_settings():
    return {"message": "machine settings"}

# 定义文件保存目录
UPLOAD_DIRECTORY = "./uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    """
    上传文件到服务器并保存在指定目录
    """
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    return {"message": f"文件 '{file.filename}' 已成功上传"}







@app.get("/upgrade-app")
async def upgrade_app():
    return {"message": "upgrade trigger"}