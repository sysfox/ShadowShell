# -*- coding: utf-8 -*-
"""
ShadowShell - 高级模块化Shell生成器
提供模块化的Shell生成、加密、反检测等功能

作者: Teror Fox (@sysfox)
项目: ShadowShell v2.0
"""

from .cipher import AdvancedCipher, gene_key, gene_advanced_key
from .code_generator import (
    gene_code, gene_code_obfuscated, advanced_obfuscate_code,
    generate_random_strings, split_payload
)
from .anti_detection import create_advanced_evasion_code
from .shell_generator import gene_shell, create_payload_dropper, create_downloader
from .white_black import (
    create_white_black_payload, create_dll_sideloading_payload,
    create_hijacking_payload, generate_white_black_template
)
from .utils import (
    validate_ip, validate_port, create_config_file, 
    print_banner, print_results
)
from .ui import interactive_mode, command_line_mode

__version__ = "2.0.0"
__author__ = "Teror Fox (@sysfox)"
__description__ = "ShadowShell - 高级模块化Shell生成器"

__all__ = [
    # 加密模块
    'AdvancedCipher', 'gene_key', 'gene_advanced_key',
    
    # 代码生成模块
    'gene_code', 'gene_code_obfuscated', 'advanced_obfuscate_code',
    'generate_random_strings', 'split_payload',
    
    # 反检测模块
    'create_advanced_evasion_code',
    
    # Shell生成模块
    'gene_shell', 'create_payload_dropper', 'create_downloader',
    
    # 白加黑模块
    'create_white_black_payload', 'create_dll_sideloading_payload',
    'create_hijacking_payload', 'generate_white_black_template',
    
    # 工具模块
    'validate_ip', 'validate_port', 'create_config_file',
    'print_banner', 'print_results',
    
    # 用户界面模块
    'interactive_mode', 'command_line_mode'
]
