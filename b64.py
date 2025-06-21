import base64
import math

def file_to_base64_chunks(input_file, output_file, chunk_size=76):
#    将文件编码为Base64并分块保存
#    参数:
#        input_file: 要编码的输入文件路径
#        output_file: 输出文件路径
#        chunk_size: 每行的字符数(默认76，符合RFC 2045标准)
    with open(input_file, 'rb') as f:
        # 读取文件内容并编码为Base64
        b64_content = base64.b64encode(f.read()).decode('utf-8')
    
    # 计算总块数
    total_chunks = math.ceil(len(b64_content) / chunk_size)
    
    with open(output_file, 'w') as f:
        # 写入分块数据
        for i in range(total_chunks):
            start = i * chunk_size
            end = start + chunk_size
            chunk = b64_content[start:end]
            
            # 写入块数据，每块用引号包围并用逗号分隔
            if i == 0:
                f.write(f'"{chunk}"')
            else:
                f.write(f',\n"{chunk}"')        

if __name__ == '__main__':
    input_filename = 'dist.zip'  # 要编码的文件
    output_filename = 'b64.txt'  # 输出文件
    
    print(f"正在将 {input_filename} 编码为Base64并分块...")
    file_to_base64_chunks(input_filename, output_filename)
    print(f"分块Base64数据已保存到 {output_filename}")