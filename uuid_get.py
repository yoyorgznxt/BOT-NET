import uuid
import platform
import socket
import psutil
import datetime
import os
import subprocess  # 用于获取GPU信息

def check_file_content():
    #检测之前有无运行过
    file_path = "C:\\ud.txt"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read().strip()
            if content == "1":
                exit()

def get_device_info():
    #获取设备信息（不含IP和磁盘，增加GPU信息）
    info = {}
    
    # 获取主机信息
    info['主机名'] = socket.gethostname()
    
    # 获取系统信息
    system_info = platform.uname()
    info['系统'] = system_info.system
    info['版本'] = system_info.release
    info['具体版本'] = system_info.version
    info['CPU架构'] = system_info.machine
    info['CPU具体信息'] = system_info.processor
    
    # 获取CPU信息
    info['CPU核心数'] = psutil.cpu_count(logical=False)
    info['CPU逻辑核心数'] = psutil.cpu_count(logical=True)
    
    # 获取内存信息
    memory = psutil.virtual_memory()
    info['总内存 '] = f"{memory.total / (1024**3):.2f} GB"
    
    # 获取GPU信息
    gpu_info = get_gpu_info()
    if gpu_info:
        info['GPU型号'] = gpu_info
    else:
        info['GPU型号'] = "Not detected or not supported"
    
    # 获取设备UUID
    info['设备UUID'] = str(uuid.uuid4())  # 生成新的UUID
    # 或者使用机器特定的UUID（如果有）
    try:
        info['设备UUID'] = str(uuid.UUID(int=uuid.getnode()))
    except:
        pass
    
    # 添加时间戳
    info['时间'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return info

def get_gpu_info():
    #获取GPU型号信息
    try:
        # Windows系统使用wmic命令
        if platform.system() == "Windows":
            try:
                result = subprocess.check_output(
                    "wmic path win32_VideoController get name",
                    shell=True,
                    stderr=subprocess.DEVNULL,
                    universal_newlines=True
                )
                gpus = [line.strip() for line in result.splitlines() if line.strip()]
                if len(gpus) > 1:  # 第一行是标题"Name"
                    return ", ".join(gpus[1:])
                return "Not detected"
            except:
                pass
    except Exception as e:
        print(f"获取GPU信息时出错: {e}")
    
    return None

def write_info_to_file(info):
    #将信息写入以UUID命名的文件
    uuid_str = info['设备UUID']
    filename = f"{uuid_str}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"设备详细信息 - {info['时间']}\n")
        f.write("=" * 50 + "\n\n")
        
        for key, value in info.items():
            f.write(f"{key}: {value}\n")
    
    print(f"设备信息已成功写入文件: {os.path.abspath(filename)}")

if __name__ == "__main__":
    # 获取设备信息
    device_info = get_device_info()
    
    # 将信息写入文件
    write_info_to_file(device_info)
