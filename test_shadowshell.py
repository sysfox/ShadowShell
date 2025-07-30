#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShadowShell测试脚本
用于验证所有功能是否正常工作
"""

import os
import sys
import subprocess
import tempfile
import shutil
import time
from pathlib import Path

def print_banner():
    """打印测试横幅"""
    print("=" * 60)
    print("  ShadowShell 功能测试脚本")
    print("  测试所有功能模块是否正常工作")
    print("=" * 60)


def test_import_modules():
    """测试模块导入"""
    print("\n🔧 测试模块导入...")
    try:
        from modules import (
            AdvancedCipher, gene_advanced_key,
            get_available_encryption_levels, get_encryption_level_description,
            interactive_mode, command_line_mode,
            create_advanced_evasion_code
        )
        print("✅ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False


def test_encryption_algorithms():
    """测试加密算法"""
    print("\n🔐 测试加密算法...")
    from modules.cipher import AdvancedCipher, get_available_encryption_levels
    
    test_data = "This is a test message for encryption"
    results = {}
    
    for level in get_available_encryption_levels():
        try:
            cipher = AdvancedCipher("testkey123", level)
            encrypted = cipher.multi_layer_encrypt(test_data)
            decrypted = cipher.multi_layer_decrypt(encrypted)
            success = (test_data == decrypted)
            results[level] = success
            print(f"  {level}: {'✅' if success else '❌'}")
        except Exception as e:
            print(f"  {level}: ❌ 错误: {e}")
            results[level] = False
    
    return all(results.values())


def test_individual_algorithms():
    """测试单独的加密算法"""
    print("\n🔍 测试单独加密算法...")
    from modules.cipher import AdvancedCipher
    
    cipher = AdvancedCipher("testkey123", "advanced")
    test_data = "Algorithm test data"
    
    algorithms = [
        ('XOR', cipher.xor_encrypt, cipher.xor_decrypt),
        ('AES', cipher.aes_encrypt, cipher.aes_decrypt),
        ('RC4', cipher.rc4_encrypt, cipher.rc4_decrypt),
        ('ChaCha20', cipher.chacha20_encrypt, cipher.chacha20_decrypt),
        ('3DES', cipher.des3_encrypt, cipher.des3_decrypt),
        ('Blowfish', cipher.blowfish_encrypt, cipher.blowfish_decrypt)
    ]
    
    results = {}
    for name, encrypt_func, decrypt_func in algorithms:
        try:
            encrypted = encrypt_func(test_data)
            decrypted = decrypt_func(encrypted)
            success = (test_data == decrypted)
            results[name] = success
            print(f"  {name}: {'✅' if success else '❌'}")
        except Exception as e:
            print(f"  {name}: ❌ 错误: {e}")
            results[name] = False
    
    return len([r for r in results.values() if r]) >= 5  # 至少5个算法成功


def test_shell_generation():
    """测试Shell生成功能"""
    print("\n🐚 测试Shell生成...")
    
    # 创建临时目录
    test_dir = tempfile.mkdtemp(prefix="shadowshell_test_")
    
    try:
        # 测试命令行模式的Shell生成
        cmd = [
            sys.executable, "main.py",
            "-i", "127.0.0.1",
            "-p", "4444", 
            "-e", "advanced",
            "-o", test_dir,
            "--quiet",
            "--silent-delay", "1"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # 检查是否生成了文件
            generated_files = list(Path(test_dir).glob("*.py"))
            if generated_files:
                print(f"✅ Shell生成成功，生成了 {len(generated_files)} 个文件")
                return True
            else:
                print("❌ Shell生成失败，未找到生成的文件")
                return False
        else:
            print(f"❌ Shell生成失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Shell生成超时")
        return False
    except Exception as e:
        print(f"❌ Shell生成异常: {e}")
        return False
    finally:
        # 清理临时目录
        shutil.rmtree(test_dir, ignore_errors=True)


def test_anti_detection():
    """测试反检测功能"""
    print("\n🛡️ 测试反检测功能...")
    try:
        from modules.anti_detection import create_advanced_evasion_code, enhanced_evasion_techniques
        
        # 生成反检测代码
        evasion_code = create_advanced_evasion_code()
        enhanced_code = enhanced_evasion_techniques()
        
        if len(evasion_code) > 1000 and len(enhanced_code) > 1000:
            print("✅ 反检测代码生成成功")
            return True
        else:
            print("❌ 反检测代码生成失败，代码长度不足")
            return False
    except Exception as e:
        print(f"❌ 反检测功能测试失败: {e}")
        return False


def test_white_black_generation():
    """测试白加黑技术"""
    print("\n🎭 测试白加黑技术...")
    
    test_dir = tempfile.mkdtemp(prefix="shadowshell_wb_test_")
    
    try:
        cmd = [
            sys.executable, "main.py",
            "-i", "127.0.0.1",
            "-p", "4444",
            "-e", "basic",
            "-o", test_dir,
            "--use-white-black",
            "--white-black-mode", "wrapper",
            "--quiet",
            "--silent-delay", "1"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # 检查是否生成了白加黑文件
            generated_files = list(Path(test_dir).glob("*.py"))
            if len(generated_files) >= 2:  # 原始文件 + 白加黑文件
                print(f"✅ 白加黑技术测试成功，生成了 {len(generated_files)} 个文件")
                return True
            else:
                print("❌ 白加黑技术测试失败，文件数量不足")
                return False
        else:
            print(f"❌ 白加黑技术测试失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 白加黑技术测试异常: {e}")
        return False
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def check_msf_availability():
    """检查MSF可用性"""
    print("\n🎯 检查MSF可用性...")
    try:
        from modules.msf_integration import MSFIntegration
        msf = MSFIntegration()
        
        if msf.is_available():
            print("✅ MSF/msfvenom 可用")
            return True
        else:
            print("⚠️ MSF/msfvenom 不可用，建议安装 Metasploit Framework")
            return False
    except Exception as e:
        print(f"❌ MSF检查失败: {e}")
        return False


def install_msf_if_needed():
    """如果需要的话安装MSF"""
    print("\n📦 检查并安装MSF...")
    
    # 检查是否已安装
    try:
        result = subprocess.run(['which', 'msfvenom'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MSF已安装")
            return True
    except:
        pass
    
    # 尝试安装MSF (仅在支持的系统上)
    if os.path.exists('/etc/debian_version'):
        print("🔧 尝试在Debian/Ubuntu系统上安装MSF...")
        try:
            # 更新包列表
            subprocess.run(['sudo', 'apt', 'update'], check=True, timeout=60)
            
            # 安装MSF
            subprocess.run(['sudo', 'apt', 'install', '-y', 'metasploit-framework'], 
                         check=True, timeout=300)
            
            print("✅ MSF安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ MSF安装失败，请手动安装")
            return False
        except subprocess.TimeoutExpired:
            print("❌ MSF安装超时")
            return False
    else:
        print("⚠️ 不支持自动安装MSF，请手动安装")
        return False


def test_encryption_levels():
    """测试加密级别功能"""
    print("\n📊 测试加密级别...")
    from modules.cipher import get_available_encryption_levels, get_encryption_level_description
    
    levels = get_available_encryption_levels()
    if len(levels) >= 4:
        print(f"✅ 发现 {len(levels)} 个加密级别:")
        for level in levels:
            desc = get_encryption_level_description(level)
            print(f"  - {level}: {desc}")
        return True
    else:
        print(f"❌ 加密级别数量不足，期望至少4个，实际 {len(levels)} 个")
        return False


def generate_test_report():
    """生成测试报告"""
    print("\n📋 运行完整功能测试...")
    
    tests = [
        ("模块导入", test_import_modules),
        ("加密级别", test_encryption_levels),
        ("加密算法", test_encryption_algorithms),
        ("单独算法", test_individual_algorithms),
        ("Shell生成", test_shell_generation),
        ("反检测功能", test_anti_detection),
        ("白加黑技术", test_white_black_generation),
        ("MSF可用性", check_msf_availability),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results[test_name] = False
    
    # 生成报告
    print("\n" + "="*60)
    print("📊 测试结果报告")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    print(f"成功率: {passed/total*100:.1f}%")
    
    if passed >= total * 0.8:  # 80%以上通过
        print("\n🎉 测试总体通过！ShadowShell功能正常")
        return True
    else:
        print("\n⚠️ 测试未完全通过，请检查失败的功能")
        return False


def main():
    """主函数"""
    print_banner()
    
    # 运行测试
    success = generate_test_report()
    
    # 可选：MSF安装
    if not check_msf_availability():
        install_choice = input("\n是否尝试安装MSF? (y/N): ").strip().lower()
        if install_choice == 'y':
            install_msf_if_needed()
    
    print("\n" + "="*60)
    if success:
        print("🎉 ShadowShell测试完成，功能验证成功！")
    else:
        print("⚠️ ShadowShell测试完成，部分功能需要检查")
    print("="*60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())