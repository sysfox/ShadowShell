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


class AdvancedCipher:
    """高级加密类"""
    
    def __init__(self, key=""):
        self.key = key
        self.xor_key = self._generate_xor_key()
    
    def _generate_xor_key(self):
        """生成XOR密钥"""
        return [random.randint(1, 255) for _ in range(32)]
    
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
        """多层加密（简化但更可靠的版本）"""
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
        """多层解密（对应简化版本）"""
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
        """基础加密算法"""
        if data == "":
            return chr(1) + chr(2) + chr(3)
            
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
        """基础解密算法（占位符实现）"""
        if encrypted_data == chr(1) + chr(2) + chr(3):
            return ""
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


Cipher = AdvancedCipher
