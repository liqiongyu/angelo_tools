import numpy as np
import jieba
import hashlib
import re


class Repeat:
    REX_CH = re.compile(u'[\u4e00-\u9fa5]+')    # 中文
    REX_EN = re.compile('[A-Za-z]+')        # 英文

    cut_func = jieba.cut
    @classmethod
    def hash2bin(cls, hash):
        d = ''
        for i in hash:
            try:
                if int(i) > 7:
                    d = d + '1'
                else:
                    d = d + '0'
            except ValueError:
                d = d + '1'
        return d

    @classmethod
    def hash_bin(cls, s):
        h = hashlib.md5(s.encode()).hexdigest()
        return cls.hash2bin(h)

    @classmethod
    def hist(cls, cut):
        _cut = {x: 0 for x in set(cut)}
        for i in cut:
            _cut[i] += 1
        return {cls.hash_bin(k): v/len(cut) for k, v in _cut.items()}

    @classmethod
    def simhash(cls, s, RE=None, cut_func=None):
        if RE:
            REX = RE
        else:
            REX = re.compile(u'[\u4e00-\u9fa5]+')
        if not cut_func:
            cut_func = cls.cut_func

        cut = [x for x in cut_func(s) if re.match(REX, x)]

        ver = [[v * (int(x) if int(x) > 0 else -1) for x in k] for k, v in cls.hist(cut).items()]
        ver = np.array(ver)
        ver_sum = ver.sum(axis=0)
        sim = ''.join(['1' if x > 0 else '0' for x in ver_sum])
        return sim

    def _hamming(self, s1, s2):
        d = [1 if a1 == a2 else 0 for a1, a2 in zip(s1, s2)].count(1)
        return d