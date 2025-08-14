import os
import sys

def generate_random_key(length=8):
    # 定义字符集：数字、大小写字母和可打印的ASCII特殊字符
    chars = (
        '0123456789'
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '/!@#$%^&*()_+-=[]{}|;:,.<>?'
    )
    
    try:
        # 使用os.urandom()获取随机字节
        random_bytes = os.urandom(length)
        
        # 将字节转换为0-255的整数列表
        random_ints = [byte for byte in random_bytes]
        
        # 将随机整数映射到字符集
        key = ''.join([chars[i % len(chars)] for i in random_ints])
        return key
    except Exception as e:
        print(f"生成密钥时出错: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    key = generate_random_key()
    if key:
        print(f"生成的随机密钥: {key}")
    else:
        print("无法生成随机密钥", file=sys.stderr)