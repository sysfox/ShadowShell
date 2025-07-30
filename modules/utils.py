# -*- coding: utf-8 -*-
"""
工具模块
提供验证、配置文件生成等辅助功能
"""
import re
import os
import json
import hashlib
import datetime


def validate_ip(ip):
    """验证IP地址格式"""
    pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return pattern.match(ip) is not None


def validate_port(port):
    """验证端口号"""
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False


def create_config_file(ip, port, key, filepath):
    """创建配置文件用于记录生成信息"""
    config = {
        "timestamp": datetime.datetime.now().isoformat(),
        "target_ip": ip,
        "target_port": port,
        "key_hash": hashlib.md5(key.encode()).hexdigest(),
        "generated_file": os.path.basename(filepath)
    }
    
    config_path = filepath.replace('.py', '.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    return config_path


def print_banner():
    """打印程序横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                     ShadowShell v2.0                          ║
║               高级模块化Shell生成器                              ║
║                Advanced Modular Shell Generator               ║
╠══════════════════════════════════════════════════════════════╣
║  功能: 生成加密的反向Shell客户端                                ║
║  用途: 渗透测试和安全研究 (仅限授权使用)                        ║
║  作者: Teror Fox (@sysfox)                                    ║
║  项目: https://github.com/sysfox/ShadowShell                  ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_results(filepath, config_path, key, config, quiet=False):
    """打印生成结果"""
    if not quiet:
        print("✅ 生成成功!")
        print(f"📁 Shell文件: {filepath}")
        print(f"📄 配置文件: {config_path}")
        print(f"🔑 密钥长度: {len(key)} 字符")
        print(f"🌐 目标地址: {config['ip']}:{config['port']}")
        print(f"🔄 重试配置: {config['retry']}次, 间隔{config['delay']}秒")
        
        if config['persistence']:
            print("⚠️  已添加持久化功能 (仅限测试环境)")
        
        if config['anti_detection']:
            print("🛡️  已添加反杀毒特征")
            
        if config['use_dropper']:
            print("🔄  使用分阶段执行模式")
        
        print("\n⚠️  安全提醒:")
        print("   - 此工具仅用于授权的渗透测试")
        print("   - 使用前请确保获得明确授权")
        print("   - 遵守当地法律法规")
