# -*- coding: utf-8 -*-
"""
加密解密模块
提供高级加密功能，包括XOR加密、多层加密等
"""
import random
import base64
import zlib
import string


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
    
    def multi_layer_encrypt(self, data):
        """多层加密"""
        # 第一层：XOR加密
        stage1 = self.xor_encrypt(data)
        
        # 第二层：原始加密算法
        stage2 = self.encrypt(stage1)
        
        # 第三层：Base64 + 压缩
        stage3 = base64.b64encode(zlib.compress(stage2.encode())).decode()
        
        return stage3
    
    def encrypt(self, data):
        """原始加密数据"""
        if data == "":
            return ""
        result = ""
        length = len(data)
        a = [ord(x) for x in data]
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


# 保持向下兼容
Cipher = AdvancedCipher
