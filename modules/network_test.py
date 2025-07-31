#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络连通性测试模块
用于测试反弹shell连接的可达性
"""
import socket
import subprocess
import platform
import time
import threading


def test_port_connectivity(host, port, timeout=5):
    """测试端口连通性"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def test_reverse_shell_connection(host, port, timeout=10):
    """测试反弹shell连接"""
    try:
        # 创建测试连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        
        # 发送测试消息
        test_msg = "[TEST] Connection test from ShadowShell\n"
        sock.send(test_msg.encode())
        
        # 等待响应
        try:
            response = sock.recv(1024).decode()
            sock.close()
            return True, f"连接成功，收到响应: {response[:50]}"
        except socket.timeout:
            sock.close()
            return True, "连接成功，但未收到响应"
            
    except ConnectionRefusedError:
        return False, "连接被拒绝 - 请检查监听器是否启动"
    except socket.timeout:
        return False, "连接超时 - 请检查网络配置和防火墙"
    except Exception as e:
        return False, f"连接错误: {str(e)}"


def check_firewall_status():
    """检查防火墙状态"""
    system = platform.system()
    try:
        if system == "Windows":
            result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                                  capture_output=True, text=True, timeout=10)
            if "State                                 ON" in result.stdout:
                return True, "Windows防火墙已启用"
            else:
                return False, "Windows防火墙已禁用"
        elif system == "Darwin":  # macOS
            result = subprocess.run(['sudo', 'pfctl', '-sr'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout.strip():
                return True, "macOS防火墙已启用"
            else:
                return False, "macOS防火墙已禁用或无规则"
        elif system == "Linux":
            # 检查iptables
            result = subprocess.run(['iptables', '-L'], 
                                  capture_output=True, text=True, timeout=10)
            if "DROP" in result.stdout or "REJECT" in result.stdout:
                return True, "Linux iptables防火墙已启用"
            else:
                return False, "Linux iptables防火墙未发现阻断规则"
    except Exception as e:
        return None, f"无法检查防火墙状态: {str(e)}"


def get_network_interfaces():
    """获取网络接口信息"""
    try:
        import netifaces
        interfaces = []
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    ip = addr['addr']
                    if ip != '127.0.0.1':
                        interfaces.append((interface, ip))
        return interfaces
    except ImportError:
        # 备用方法
        try:
            result = subprocess.run(['ifconfig' if platform.system() != 'Windows' else 'ipconfig'], 
                                  capture_output=True, text=True, timeout=10)
            # 简单解析输出
            lines = result.stdout.split('\n')
            interfaces = []
            current_iface = None
            for line in lines:
                if ':' in line and not line.startswith(' '):
                    current_iface = line.split(':')[0].strip()
                elif 'inet ' in line and current_iface:
                    parts = line.strip().split()
                    for i, part in enumerate(parts):
                        if part == 'inet' and i + 1 < len(parts):
                            ip = parts[i + 1]
                            if ip != '127.0.0.1' and '.' in ip:
                                interfaces.append((current_iface, ip))
                            break
            return interfaces
        except:
            return []


def comprehensive_network_test(host, port):
    """综合网络连通性测试"""
    print(f"🌐 开始网络连通性测试...")
    print(f"目标: {host}:{port}")
    print("=" * 50)
    
    # 1. 基础端口测试
    print("1. 测试端口连通性...")
    port_reachable = test_port_connectivity(host, port)
    if port_reachable:
        print(f"   ✅ 端口 {port} 可达")
    else:
        print(f"   ❌ 端口 {port} 不可达")
    
    # 2. 反弹shell连接测试
    print("2. 测试反弹shell连接...")
    shell_success, shell_msg = test_reverse_shell_connection(host, port)
    if shell_success:
        print(f"   ✅ {shell_msg}")
    else:
        print(f"   ❌ {shell_msg}")
    
    # 3. 防火墙检查
    print("3. 检查防火墙状态...")
    fw_enabled, fw_msg = check_firewall_status()
    if fw_enabled is True:
        print(f"   ⚠️  {fw_msg}")
    elif fw_enabled is False:
        print(f"   ✅ {fw_msg}")
    else:
        print(f"   ❓ {fw_msg}")
    
    # 4. 网络接口检查
    print("4. 检查网络接口...")
    interfaces = get_network_interfaces()
    if interfaces:
        print("   📡 可用网络接口:")
        for iface, ip in interfaces:
            print(f"      - {iface}: {ip}")
    
    # 5. 生成建议
    print("\n💡 建议:")
    if not port_reachable:
        print("   - 检查监听器是否在正确端口启动")
        print("   - 确认IP地址是否正确（本地测试用127.0.0.1，远程用外网IP）")
        print("   - 检查防火墙是否阻止了连接")
    
    if not shell_success and port_reachable:
        print("   - 端口可达但shell连接失败，可能是监听器类型不匹配")
        print("   - 建议使用: nc -l [端口] 或 MSF监听器")
    
    if fw_enabled:
        print("   - 防火墙已启用，可能需要添加例外规则")
        print("   - Windows: 添加端口到防火墙例外")
        print("   - macOS: 检查系统偏好设置 > 安全性与隐私 > 防火墙")
        print("   - Linux: 使用 iptables 或 ufw 添加规则")
    
    return shell_success


def start_test_listener(port, duration=60):
    """启动测试监听器"""
    def listener():
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', port))
            server.listen(1)
            server.settimeout(duration)
            
            print(f"🎧 测试监听器已启动，端口: {port}")
            print(f"   等待连接... (超时: {duration}秒)")
            
            try:
                client, addr = server.accept()
                print(f"✅ 收到来自 {addr} 的连接")
                
                # 接收数据
                data = client.recv(1024)
                if data:
                    print(f"📨 收到数据: {data.decode()}")
                
                client.close()
                return True
            except socket.timeout:
                print("⏰ 监听器超时，未收到连接")
                return False
            finally:
                server.close()
                
        except Exception as e:
            print(f"❌ 监听器错误: {str(e)}")
            return False
    
    # 在后台线程中运行
    thread = threading.Thread(target=listener)
    thread.daemon = True
    thread.start()
    return thread


if __name__ == "__main__":
    # 示例用法
    test_host = "127.0.0.1"
    test_port = 4444
    
    comprehensive_network_test(test_host, test_port)
