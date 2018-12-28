import re
import jieba
import hashlib
import numpy as np


class SimHash:
    def __init__(self, num):
        self.oct_digest = num
    
    def hex_digest(self):
        return hex(self.oct_digest)[2:]
    
    def bin_digest(self):
        return bin(self.oct_digest)[2:]


class CalculateSimHash:
    def __init__(self):
        self.re_han = re.compile(u'[\u4e00-\u9fa5]+')
    
    def sim_hash(self, text=''):
        res = 0
        feature_iters = [self.__text2feature_iter(word) for word in jieba.cut(text)]
        for i in range(128):
            res <<= 1
            res += self.__sum2bin(next(feature_iter) for feature_iter in feature_iters)
        return SimHash(res)
    
    def sim_hamming(self, text1, text2):
        r, s = 0, self.sim_hash(text1).oct_digest^self.sim_hash(text2).oct_digest
        while s:
            r += s&1
            s >>= 1
        return r
    
    @staticmethod
    def __text2md5(text=''):
        return int(hashlib.md5(text.encode()).hexdigest(), 16)
    
    def __text2md5_bin_iter(self, text):
        md5_hex = self.__text2md5(text)
        for i in range(128):
            yield md5_hex & 1
            md5_hex >>= 1
            
    def __text2feature_iter(self, text):
        idf = self.__text2idf(text)
        for bin_pos in self.__text2md5_bin_iter(text):
            yield idf*(2*bin_pos-1)
    
    def __text2idf(self, text):
        if self.re_han.match(text):
            return round(6 - np.log10((jieba.dt.FREQ.get(text) or 0) + 1))
        else:
            return 1
    
    @staticmethod
    def __sum2bin(num_iter):
        return sum(num_iter) > 0 and 1 or 0

    
csh = CalculateSimHash()
sim_hash = csh.sim_hash
sim_hamming = csh.sim_hamming

if __name__ == '__main__':
    print(sim_hash('你好，世界！'))
    print(sim_hamming('你好，世界！'))
