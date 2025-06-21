import subprocess
import os
from PyInstaller.__main__ import run
def package_with_pyinstaller_api():
    opts = [
        "--onefile",
        "--icon=NONE",#图标
        "--name", "dd", #文件名
        "ddos.py"
        ]
    try:
        print("开始PyInstaller打包...")
        run(opts)
        print("PyInstaller打包完成")

        # 压缩可执行文件
        exe_path = os.path.join("dist", "dd.exe")
        compress_executable(exe_path)

        # 加壳保护
        pack_executable(exe_path)

        print("打包成功! 最终文件:", exe_path)
    except SystemExit as e:
        print("打包过程出错:", e)

def compress_executable(exe_path):
    print("开始压缩可执行文件...")
    # 使用 lzma 压缩
    subprocess.run(["upx", "--lzma", exe_path])
    print("压缩完成")

def pack_executable(exe_path):
    print("开始加壳保护...")
    # 使用 UPX 进行加壳
    subprocess.run(["upx","--force", exe_path])
    print("加壳完成")

if __name__ == "__main__":
    package_with_pyinstaller_api()