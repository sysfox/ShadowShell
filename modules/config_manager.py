#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
处理配置的导入、导出、验证和管理
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.default_config = {
            'ip': '127.0.0.1',
            'port': 4444,
            'encryption_level': 'advanced',
            'retry': 10,
            'delay': 5,
            'key_length': 16,
            'output_dir': 'output',
            'filename': None,
            'persistence': False,
            'anti_detection': True,
            'use_dropper': False,
            'use_white_black': False,
            'white_black_mode': 'wrapper',
            'use_downloader': False,
            'download_url': None,
            'downloader_silent': True,
            'use_msf': False,
            'msf_payload': 'python/meterpreter/reverse_tcp',
            'msf_encoder': None,
            'msf_iterations': 3,
            'msf_format': 'python',
            'quiet': False,
            'silent_delay': 30,
            'debug': False,
            'strict_mode': True,
            'test_connection': False,
            'benchmark': False
        }
    
    def export_config(self, config: Dict[str, Any], filepath: str) -> bool:
        """导出配置到文件"""
        try:
            # 添加元数据
            export_data = {
                'metadata': {
                    'version': '2.0',
                    'exported_at': datetime.now().isoformat(),
                    'tool': 'ShadowShell'
                },
                'config': config
            }
            
            # 确保目录存在
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 配置已导出到: {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ 配置导出失败: {e}")
            return False
    
    def import_config(self, filepath: str) -> Optional[Dict[str, Any]]:
        """从文件导入配置"""
        try:
            if not os.path.exists(filepath):
                print(f"❌ 配置文件不存在: {filepath}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查是否是新格式（带元数据）
            if 'config' in data and 'metadata' in data:
                config = data['config']
                metadata = data['metadata']
                print(f"📥 导入配置 (版本: {metadata.get('version', 'unknown')}, "
                      f"导出时间: {metadata.get('exported_at', 'unknown')})")
            else:
                # 兼容旧格式
                config = data
                print("📥 导入配置 (兼容模式)")
            
            # 验证和补全配置
            validated_config = self.validate_config(config)
            
            print("✅ 配置导入成功")
            return validated_config
            
        except Exception as e:
            print(f"❌ 配置导入失败: {e}")
            return None
    
    def validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """验证和补全配置"""
        validated = self.default_config.copy()
        
        for key, value in config.items():
            if key in validated:
                # 类型检查和转换
                try:
                    if key in ['port', 'retry', 'delay', 'key_length', 'msf_iterations', 'silent_delay']:
                        validated[key] = int(value)
                    elif key in ['persistence', 'anti_detection', 'use_dropper', 'use_white_black',
                               'use_downloader', 'downloader_silent', 'use_msf', 'quiet', 
                               'debug', 'strict_mode', 'test_connection', 'benchmark']:
                        validated[key] = bool(value)
                    else:
                        validated[key] = value
                except (ValueError, TypeError):
                    print(f"⚠️ 配置项 {key} 值无效，使用默认值")
        
        return validated
    
    def get_config_template(self) -> Dict[str, Any]:
        """获取配置模板"""
        return self.default_config.copy()
    
    def merge_configs(self, base_config: Dict[str, Any], 
                     overlay_config: Dict[str, Any]) -> Dict[str, Any]:
        """合并配置（overlay覆盖base）"""
        result = base_config.copy()
        result.update(overlay_config)
        return self.validate_config(result)


def create_sample_configs():
    """创建示例配置文件"""
    manager = ConfigManager()
    
    configs = {
        'basic_config.json': {
            'ip': '127.0.0.1',
            'port': 4444,
            'encryption_level': 'basic',
            'debug': True,
            'strict_mode': False
        },
        'advanced_config.json': {
            'ip': '0.0.0.0',
            'port': 8888,
            'encryption_level': 'maximum',
            'persistence': True,
            'anti_detection': True,
            'use_white_black': True,
            'strict_mode': True
        },
        'msf_config.json': {
            'ip': '192.168.1.100',
            'port': 4444,
            'use_msf': True,
            'msf_payload': 'python/meterpreter/reverse_tcp',
            'msf_encoder': 'x86/shikata_ga_nai',
            'msf_iterations': 5
        }
    }
    
    config_dir = Path('configs')
    config_dir.mkdir(exist_ok=True)
    
    for filename, config in configs.items():
        filepath = config_dir / filename
        manager.export_config(config, str(filepath))
    
    print(f"✅ 示例配置文件已创建在 {config_dir} 目录")


if __name__ == "__main__":
    # 创建示例配置
    create_sample_configs()
