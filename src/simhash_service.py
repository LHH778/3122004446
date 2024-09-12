import jieba
import re
from memory_profiler import profile

# 定义一些大整数
BIGINT_0 = 0
BIGINT_1 = 1
BIGINT_2 = 2
BIGINT_1000003 = 1000003
BIGINT_2E64M1 = (BIGINT_2 ** 64) - BIGINT_1


# SimHash服务类
class SimHashService:
    @staticmethod
    # @profile
    def get(text):
        if text is None:
            return None

        # 数据预处理
        sum_weight = 0
        max_weight = 0
        bits = [0] * 64

        # 使用jieba分词
        terms = list(jieba.cut(text))  # 这里使用 jieba 分词

        for term in terms:
            word = term
            # 过滤标点符号或无效字符
            if re.match(r'[\W]+', word):
                continue

            # 计算每个词的哈希值和权重
            word_hash = SimHashService.get_word_hash(word)
            word_weight = SimHashService.get_word_weight(word)
            if word_weight == 0:
                continue

            sum_weight += word_weight
            if max_weight < word_weight:
                max_weight = word_weight

            # 按权重逐位计算哈希值
            for i in range(64):
                bit_mask = BIGINT_1 << (63 - i)
                if word_hash & bit_mask != 0:
                    bits[i] += word_weight
                else:
                    bits[i] -= word_weight

        # 将统计结果转换成0/1字符串
        sim_hash_builder = []
        for i in range(64):
            if bits[i] > 0:
                sim_hash_builder.append("1")
            else:
                sim_hash_builder.append("0")

        return ''.join(sim_hash_builder)

    @staticmethod
    def get_word_hash(word):
        if not word:
            return BIGINT_0
        hash_value = (ord(word[0]) << 12)
        for ch in word:
            hash_value = (hash_value * BIGINT_1000003) ^ ord(ch)
            hash_value &= BIGINT_2E64M1  # 保持在64位内
        hash_value ^= len(word)
        return hash_value

    @staticmethod
    def get_word_weight(word):
        """定义词的权重"""
        if not word:
            return 0
        length = len(word)
        if length == 1:
            return 1
        elif word[0] >= '\u3040':
            return 8 if length == 2 else 16
        else:
            return 2 if length == 2 else 4

    @staticmethod
    def hamming_distance(a, b):
        if a is None or b is None:
            return -1
        if len(a) != len(b):
            return -1
        return sum(c1 != c2 for c1, c2 in zip(a, b))
