# -*- coding: utf-8 -*-
"""
加密解密模块
提供高级加密功能，包括XOR加密、多层加密等
"""
import random
import base64
import zlib
import string
import hashlib
import time
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import hmac
import struct


class AdvancedCipher:
    """高级加密类"""
    
    # 加密级别定义
    ENCRYPTION_LEVELS = {
        'basic': {'algorithms': ['xor'], 'iterations': 1},
        'standard': {'algorithms': ['xor', 'base64'], 'iterations': 2},
        'advanced': {'algorithms': ['xor', 'aes', 'base64'], 'iterations': 3},
        'maximum': {'algorithms': ['xor', 'aes', 'chacha20', 'rc4', 'base64'], 'iterations': 5}
    }
    
    def __init__(self, key="", encryption_level="advanced"):
        self.key = key
        self.encryption_level = encryption_level
        self.xor_key = self._generate_xor_key()
        self._aes_key = None
        self._fernet_key = None
    
    def setKey(self, key):
        """生成AES密钥"""
        if not self._aes_key:
            # 使用主密钥派生AES密钥
            key_material = (self.key + "aes_salt").encode('utf-8')
            self._aes_key = hashlib.sha256(key_material).digest()
        return self._aes_key
    
    def _generate_fernet_key(self):
        """生成Fernet密钥"""
        if not self._fernet_key:
            key_material = (self.key + "fernet_salt").encode('utf-8')
            key_hash = hashlib.sha256(key_material).digest()
            self._fernet_key = base64.urlsafe_b64encode(key_hash)
        return self._fernet_key
    
    def aes_encrypt(self, data):
        """AES加密"""
        try:
            key = self._generate_aes_key()
            iv = os.urandom(16)
            
            # PKCS7 padding
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data.encode('utf-8')) + padder.finalize()
            
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            encrypted = encryptor.update(padded_data) + encryptor.finalize()
            
            return base64.b64encode(iv + encrypted).decode()
        except Exception:
            return self.xor_encrypt(data)  # fallback
    
    def aes_decrypt(self, encrypted_data):
        """AES解密"""
        try:
            key = self._generate_aes_key()
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            
            iv = encrypted_bytes[:16]
            encrypted = encrypted_bytes[16:]
            
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(encrypted) + decryptor.finalize()
            
            # Remove PKCS7 padding
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()
            
            return data.decode('utf-8')
        except Exception:
            return self.xor_decrypt(encrypted_data)  # fallback
    
    def rc4_encrypt(self, data):
        """RC4加密算法（自实现）"""
        try:
            key = self.key.encode('utf-8')[:32]  # 限制密钥长度
            s = list(range(256))
            j = 0
            
            # Key scheduling algorithm
            for i in range(256):
                j = (j + s[i] + key[i % len(key)]) % 256
                s[i], s[j] = s[j], s[i]
            
            # Pseudo-random generation algorithm
            result = []
            i = j = 0
            for byte in data.encode('utf-8'):
                i = (i + 1) % 256
                j = (j + s[i]) % 256
                s[i], s[j] = s[j], s[i]
                k = s[(s[i] + s[j]) % 256]
                result.append(byte ^ k)
            
            return base64.b64encode(bytes(result)).decode()
        except Exception:
            return self.xor_encrypt(data)  # fallback
    
    def rc4_decrypt(self, encrypted_data):
        """RC4解密算法"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            key = self.key.encode('utf-8')[:32]
            s = list(range(256))
            j = 0
            
            # Key scheduling algorithm
            for i in range(256):
                j = (j + s[i] + key[i % len(key)]) % 256
                s[i], s[j] = s[j], s[i]
            
            # Pseudo-random generation algorithm
            result = []
            i = j = 0
            for byte in encrypted_bytes:
                i = (i + 1) % 256
                j = (j + s[i]) % 256
                s[i], s[j] = s[j], s[i]
                k = s[(s[i] + s[j]) % 256]
                result.append(byte ^ k)
            
            return bytes(result).decode('utf-8')
        except Exception:
            return self.xor_decrypt(encrypted_data)  # fallback
    
    def chacha20_encrypt(self, data):
        """ChaCha20加密（使用Fernet作为替代实现）"""
        try:
            key = self._generate_fernet_key()
            f = Fernet(key)
            encrypted = f.encrypt(data.encode('utf-8'))
            return base64.b64encode(encrypted).decode()
        except Exception:
            return self.aes_encrypt(data)  # fallback
    
    def chacha20_decrypt(self, encrypted_data):
        """ChaCha20解密"""
        try:
            key = self._generate_fernet_key()
            f = Fernet(key)
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted = f.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        except Exception:
            return self.aes_decrypt(encrypted_data)  # fallback
    
    def des3_encrypt(self, data):
        """3DES加密（简化实现）"""
        try:
            # 使用三重XOR模拟3DES
            key1 = self.key[:8].ljust(8, '0')
            key2 = self.key[8:16].ljust(8, '1') 
            key3 = self.key[16:24].ljust(8, '2')
            
            # 第一轮加密
            result1 = self._simple_des_round(data, key1)
            # 第二轮解密（反向）
            result2 = self._simple_des_round(result1, key2, reverse=True)
            # 第三轮加密
            result3 = self._simple_des_round(result2, key3)
            
            return base64.b64encode(result3.encode('utf-8')).decode()
        except Exception:
            return self.rc4_encrypt(data)  # fallback
    
    def des3_decrypt(self, encrypted_data):
        """3DES解密"""
        try:
            key1 = self.key[:8].ljust(8, '0')
            key2 = self.key[8:16].ljust(8, '1')
            key3 = self.key[16:24].ljust(8, '2')
            
            data = base64.b64decode(encrypted_data.encode()).decode('utf-8')
            
            # 反向解密
            result1 = self._simple_des_round(data, key3, reverse=True)
            result2 = self._simple_des_round(result1, key2)
            result3 = self._simple_des_round(result2, key1, reverse=True)
            
            return result3
        except Exception:
            return self.rc4_decrypt(encrypted_data)  # fallback
    
    def _simple_des_round(self, data, key, reverse=False):
        """简化的DES轮加密"""
        key_bytes = [ord(c) for c in key]
        result = ""
        
        for i, char in enumerate(data):
            key_byte = key_bytes[i % len(key_bytes)]
            if reverse:
                result += chr((ord(char) - key_byte) % 256)
            else:
                result += chr((ord(char) + key_byte) % 256)
        
        return result
    
    def blowfish_encrypt(self, data):
        """Blowfish加密（简化实现使用多重XOR）"""
        try:
            # 生成16轮子密钥
            subkeys = []
            for i in range(16):
                subkey_material = (self.key + f"_round_{i}").encode('utf-8')
                subkey = hashlib.md5(subkey_material).digest()
                subkeys.append(subkey)
            
            data_bytes = data.encode('utf-8')
            result = data_bytes
            
            # 16轮Feistel网络模拟
            for subkey in subkeys:
                new_result = bytearray()
                for i, byte in enumerate(result):
                    new_result.append(byte ^ subkey[i % len(subkey)])
                result = bytes(new_result)
            
            return base64.b64encode(result).decode()
        except Exception:
            return self.des3_encrypt(data)  # fallback
    
    def blowfish_decrypt(self, encrypted_data):
        """Blowfish解密"""
        try:
            # 生成16轮子密钥（反向）
            subkeys = []
            for i in range(16):
                subkey_material = (self.key + f"_round_{i}").encode('utf-8')
                subkey = hashlib.md5(subkey_material).digest()
                subkeys.append(subkey)
            
            subkeys.reverse()  # 反向解密
            
            data_bytes = base64.b64decode(encrypted_data.encode())
            result = data_bytes
            
            # 16轮Feistel网络模拟（反向）
            for subkey in subkeys:
                new_result = bytearray()
                for i, byte in enumerate(result):
                    new_result.append(byte ^ subkey[i % len(subkey)])
                result = bytes(new_result)
            
            return result.decode('utf-8')
        except Exception:
            return self.des3_decrypt(encrypted_data)  # fallback
    
    def _generate_xor_key(self):
        """生成XOR密钥"""
        return [random.randint(1, 255) for _ in range(32)]
    
    def set_encryption_level(self, level):
        """设置加密级别"""
        if level in self.ENCRYPTION_LEVELS:
            self.encryption_level = level
        else:
            self.encryption_level = "advanced"  # 默认级别
    
    def setKey(self, key):
        """设置密钥"""
        self.key = key
    
    def getKey(self):
        """获取密钥"""
        return self.key
    
    def parseKey(self, key):
        """解析密钥，将其转换为数字码"""
        if key != "":
            o = 0
            for k in key:
                n = 0
                i = str(ord(k))
                for t in i:
                    n += int(t)
                o += n
            while True:
                if o < 10:
                    o = int(o * 2)
                elif o > 100:
                    o = int(o / 2)
                else:
                    return o
        return 0
    
    def getOdd(self, max):
        """获取奇数索引列表"""
        return [i for i in range(1, max + 1) if i % 2 == 1]
    
    def xor_encrypt(self, data):
        """XOR加密"""
        result = bytearray()
        for i, byte in enumerate(data.encode('utf-8')):
            result.append(byte ^ self.xor_key[i % len(self.xor_key)])
        return base64.b64encode(result).decode()
    
    def xor_decrypt(self, encrypted_data):
        """XOR解密"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            result = ""
            for i, byte in enumerate(encrypted_bytes):
                result += chr(byte ^ self.xor_key[i % len(self.xor_key)])
            return result
        except Exception:
            return ""
    
    def multi_layer_encrypt(self, data):
        """多层加密（根据加密级别使用不同算法）"""
        try:
            level_config = self.ENCRYPTION_LEVELS.get(self.encryption_level, self.ENCRYPTION_LEVELS['advanced'])
            algorithms = level_config['algorithms']
            iterations = level_config['iterations']
            
            nonce = os.urandom(8).hex()
            result = f"{nonce}:{data}"
            
            # 根据加密级别应用不同的算法
            for i in range(iterations):
                for algorithm in algorithms:
                    if algorithm == 'xor':
                        result = self.xor_encrypt(result)
                    elif algorithm == 'aes':
                        result = self.aes_encrypt(result) 
                    elif algorithm == 'rc4':
                        result = self.rc4_encrypt(result)
                    elif algorithm == 'chacha20':
                        result = self.chacha20_encrypt(result)
                    elif algorithm == 'des3':
                        result = self.des3_encrypt(result)
                    elif algorithm == 'blowfish':
                        result = self.blowfish_encrypt(result)
                    elif algorithm == 'base64':
                        result = base64.b64encode(result.encode()).decode()
            
            # 最终压缩
            compressed = zlib.compress(result.encode())
            return base64.b64encode(compressed).decode()
            
        except Exception:
            # 回退到原来的方法
            nonce = os.urandom(8).hex()
            data_with_nonce = f"{nonce}:{data}"
            
            # 第一层：XOR加密
            stage1 = self.xor_encrypt(data_with_nonce)
            
            # 第二层：Base64编码（避免使用复杂的基础加密算法）
            stage2 = base64.b64encode(stage1.encode()).decode()
            
            # 第三层：压缩 + Base64
            stage3 = base64.b64encode(zlib.compress(stage2.encode())).decode()
            
            return stage3
    
    def multi_layer_decrypt(self, encrypted_data):
        """多层解密（根据加密级别解密）"""
        try:
            # 解压缩
            compressed_data = base64.b64decode(encrypted_data.encode())
            decompressed = zlib.decompress(compressed_data).decode()
            
            level_config = self.ENCRYPTION_LEVELS.get(self.encryption_level, self.ENCRYPTION_LEVELS['advanced'])
            algorithms = level_config['algorithms']
            iterations = level_config['iterations']
            
            result = decompressed
            
            # 反向解密
            for i in range(iterations):
                for algorithm in reversed(algorithms):
                    if algorithm == 'base64':
                        result = base64.b64decode(result.encode()).decode()
                    elif algorithm == 'blowfish':
                        result = self.blowfish_decrypt(result)
                    elif algorithm == 'des3':
                        result = self.des3_decrypt(result)
                    elif algorithm == 'chacha20':
                        result = self.chacha20_decrypt(result)
                    elif algorithm == 'rc4':
                        result = self.rc4_decrypt(result)
                    elif algorithm == 'aes':
                        result = self.aes_decrypt(result)
                    elif algorithm == 'xor':
                        result = self.xor_decrypt(result)
            
            # 移除nonce
            if ':' in result:
                _, original_data = result.split(':', 1)
                return original_data
            return result
            
        except Exception:
            # 回退解密方法
            try:
                # 第一步：Base64解码 + 解压缩
                stage1_decoded = base64.b64decode(encrypted_data.encode())
                stage1_decompressed = zlib.decompress(stage1_decoded).decode()
                
                # 第二步：Base64解码
                stage2_decoded = base64.b64decode(stage1_decompressed.encode()).decode()
                
                # 第三步：XOR解密
                stage3 = self.xor_decrypt(stage2_decoded)
                
                # 移除随机前缀
                if ':' in stage3:
                    _, original_data = stage3.split(':', 1)
                    return original_data
                return stage3
            except Exception:
                # 备用解密方法（直接XOR）
                try:
                    decoded = base64.b64decode(encrypted_data.encode())
                    result = ""
                    for i, byte in enumerate(decoded):
                        result += chr(byte ^ self.xor_key[i % len(self.xor_key)])
                    if ':' in result:
                        return result.split(':', 1)[1]
                    return result
                except:
                    return ""
    
    def encrypt(self, data):
        """基础加密算法 - 改进Unicode处理"""
        if data == "":
            return chr(1) + chr(2) + chr(3)
        
        # 将Unicode字符串转换为UTF-8字节序列
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
            # 转换为字符串处理，确保可逆
            data = ''.join(chr(b) for b in data_bytes)
            
        salt = os.urandom(4).hex()
        data_with_salt = f"{salt}|{data}"
        
        result = ""
        length = len(data_with_salt)
        a = [ord(x) for x in data_with_salt]
        remainder = length % 4
        if remainder != 0:
            b = 4 - remainder
            for c in range(b):
                a.append(0)
        groups = []
        d = len(a) // 2
        e1 = a[:d]
        e2 = a[d:]
        indexs = self.getOdd(d)
        groups.append([e1[i - 1] for i in indexs])
        groups.append([e1[i] for i in indexs])
        groups.append([e2[i - 1] for i in indexs])
        groups.append([e2[i] for i in indexs])
        f1 = groups[0] + groups[3]
        f2 = groups[1] + groups[2]
        keycode1 = self.parseKey(self.getKey())
        g = []
        for h in f1:
            i = h + keycode1
            j = chr(i)
            g.append(i)
            result += j
        k = str(sum(g))
        keycode2 = self.parseKey(k)
        for l in f2:
            m = l + keycode2
            n = chr(m)
            result += n
        return result
    
    def decrypt(self, encrypted_data):
        """基础解密函数 - 改进Unicode处理"""
        try:
            if '|' in encrypted_data:
                _, data_part = encrypted_data.split('|', 1)
            else:
                data_part = encrypted_data
                
            result = ""
            length = len(data_part)
            a = [ord(x) for x in data_part]
            remainder = length % 4
            if remainder != 0:
                b = 4 - remainder
                for c in range(b):
                    a.append(0)
            groups = []
            d = len(a) // 2
            e1 = a[:d]
            e2 = a[d:]
            indexs = self.getOdd(d)
            groups.append([e1[i - 1] for i in indexs if i - 1 < len(e1)])
            groups.append([e1[i] for i in indexs if i < len(e1)])
            groups.append([e2[i - 1] for i in indexs if i - 1 < len(e2)])
            groups.append([e2[i] for i in indexs if i < len(e2)])
            
            # 确保所有组大小相同
            min_len = min(len(g) for g in groups if g)
            if min_len > 0:
                groups = [g[:min_len] for g in groups]
                f1 = groups[0] + groups[3]
                f2 = groups[1] + groups[2]
                keycode1 = self.parseKey(self.getKey())
                
                # 收集所有解密后的字节值
                result_bytes = []
                g = []
                
                for h in f1:
                    i = h - keycode1
                    g.append(h)  # 使用原始值计算checksum
                    result_bytes.append(i % 256)  # 确保在字节范围内
                    result += chr(i % 256)
                
                k = str(sum(g)) if g else "0"
                keycode2 = self.parseKey(k)
                
                for l in f2:
                    m = l - keycode2
                    result_bytes.append(m % 256)  # 确保在字节范围内
                    result += chr(m % 256)
                
                # 尝试将结果转换回UTF-8字符串
                try:
                    # 过滤掉填充的0字节
                    filtered_bytes = [b for b in result_bytes if b != 0 or len([x for x in result_bytes if x != 0]) == 0]
                    if filtered_bytes:
                        utf8_result = bytes(filtered_bytes).decode('utf-8')
                        return utf8_result
                except UnicodeDecodeError:
                    pass
                
                # 如果UTF-8解码失败，返回原始字符串
                return result.rstrip('\x00')  # 移除尾部的null字符
                
        except Exception:
            # 如果基础解密失败，返回标识符让多层解密接管
            return "[ENCRYPTED_DATA_USE_MULTILAYER]"

    def create_secure_payload(self, payload_code):
        """创建安全的载荷包装器"""
        encrypted_payload = self.multi_layer_encrypt(payload_code)
        
        decrypt_code = f'''
import base64, zlib, random

class D:
    def __init__(self):
        self.k = {self.xor_key}
    
    def x(self, d):
        try:
            b = base64.b64decode(d.encode())
            r = ""
            for i, byte in enumerate(b):
                r += chr(byte ^ self.k[i % len(self.k)])
            return r
        except:
            return ""
    
    def m(self, d):
        try:
            s1 = base64.b64decode(d.encode())
            s2 = zlib.decompress(s1).decode()
            s3 = self.x(s2)
            if ':' in s3:
                return s3.split(':', 1)[1]
            return s3
        except:
            return ""

try:
    d = D()
    c = d.m("{encrypted_payload}")
    if c:
        exec(c)
except:
    pass
'''
        return decrypt_code


def gene_key(length=10, char_from=33, char_to=125):
    """生成随机密钥"""
    result = ""
    for i in range(length):
        result += chr(random.randint(char_from, char_to))
    return result


def gene_advanced_key(length=16, include_special=True):
    """生成高强度密钥"""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if include_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(random.choice(chars) for _ in range(length))


def remove_comments_from_code(code):
    """从代码中移除注释，确保加密前的代码干净"""
    lines = code.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        if '#' in line and not ('"' in line or "'" in line):
            line = line.split('#')[0].rstrip()
        cleaned_lines.append(line)
    
    result = '\n'.join(cleaned_lines)
    while '\n\n\n' in result:
        result = result.replace('\n\n\n', '\n\n')
    
    return result.strip()


def get_available_encryption_levels():
    """获取可用的加密级别"""
    return list(AdvancedCipher.ENCRYPTION_LEVELS.keys())


def get_encryption_level_description(level):
    """获取加密级别描述"""
    descriptions = {
        'basic': 'XOR加密 - 快速但基础',
        'standard': 'XOR + Base64 - 标准级别',
        'advanced': 'XOR + AES + Base64 - 高级加密（推荐）',
        'maximum': 'XOR + AES + ChaCha20 + RC4 + Base64 - 最高级别（较慢）'
    }
    return descriptions.get(level, '未知级别')


def get_available_algorithms():
    """获取可用的加密算法列表"""
    return ['xor', 'aes', 'rc4', 'chacha20', 'des3', 'blowfish', 'base64']


Cipher = AdvancedCipher
