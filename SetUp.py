from PyInstaller.__main__ import run
def package_with_pyinstaller_api():
    opts = [
        "--onefile",
        "--name", "BOT-NET",
        "--windowed", #需要隐藏窗口
        "client.py",
        ]
    try:
        run(opts)
        print("打包成功")
    except SystemExit as e:
        print("打包过程出错:", e)
if __name__ == "__main__":
    package_with_pyinstaller_api()
