import jieba
import re

# 定义一些大整数
BIGINT_0 = 0
BIGINT_1 = 1
BIGINT_2 = 2
BIGINT_1000003 = 1000003
BIGINT_2E64M1 = (BIGINT_2 ** 64) - BIGINT_1


# SimHash服务类
class SimHashService:
    @staticmethod
    def get(text):
        if text is None:
            return None

        text = SimHashService.preprocess_data(text)
        sum_weight = 0
        max_weight = 0
        bits = [0] * 64
        terms = list(jieba.cut(text))

        for term in terms:
            word = term
            if re.match(r'[\W]+', word):  # 跳过标点和停用词
                continue

            word_hash = SimHashService.get_word_hash(word)
            word_weight = SimHashService.get_word_weight(word)
            if word_weight == 0:
                continue

            sum_weight += word_weight
            if max_weight < word_weight:
                max_weight = word_weight

            # 逐位计算哈希值，并按权重记录到数组
            for i in range(64):
                bit_mask = BIGINT_1 << (63 - i)
                if word_hash & bit_mask != 0:
                    bits[i] += word_weight
                else:
                    bits[i] -= word_weight

        # 将统计结果转为0/1字符串
        sim_hash_builder = []
        for i in range(64):
            if bits[i] > 0:
                sim_hash_builder.append("1")
            else:
                sim_hash_builder.append("0")

        return ''.join(sim_hash_builder)

    @staticmethod
    def preprocess_data(text_content):
        if not text_content:
            return text_content
        text_content = SimHashService.to_dbc(text_content)
        text_content = re.sub(r'<.*?>', '', text_content)  # 去除HTML标签
        text_content = re.sub(r'[^\u4e00-\u9fa5]', '', text_content)  # 只保留中文字符
        return text_content

    @staticmethod
    def to_dbc(input_str):
        """全角转半角"""
        result = []
        for char in input_str:
            code = ord(char)
            if code == 12288:  # 全角空格
                code = 32
            elif 65281 <= code <= 65374:  # 全角字符 (其他字符按此范围转换)
                code -= 65248
            result.append(chr(code))
        return ''.join(result)

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


# 论文查重系统
class PaperChecker:
    def __init__(self, threshold=3):
        self.threshold = threshold  # 汉明距离的阈值，越低查重越严格

    def check_similarity(self, text1, text2):
        # 计算两篇论文的SimHash
        simhash1 = SimHashService.get(text1)
        simhash2 = SimHashService.get(text2)

        # 计算汉明距离
        hamming_dist = SimHashService.hamming_distance(simhash1, simhash2)

        print(f"汉明距离: {hamming_dist}")

        # 根据汉明距离判断是否相似
        if hamming_dist <= self.threshold:
            return "相似论文，疑似重复"
        else:
            return "论文不相似"


# 示例使用
if __name__ == "__main__":
    text1 = "这是第一篇测试文本，用来进行论文查重。"
    text2 = "这是第二篇测试文章，用于查重。"

    checker = PaperChecker(threshold=5)  # 设置汉明距离阈值为5
    result = checker.check_similarity(text1, text2)
    print(result)
