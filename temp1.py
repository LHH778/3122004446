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
            # 这里模拟分词后的词性（根据需要调整）
            # 如果是标点或停用词跳过 (可以自定义停用词表)
            if re.match(r'[\W]+', word):
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


# 示例使用
if __name__ == "__main__":
    text = "这是一个测试文本，用来计算simhash。"
    sim_hash = SimHashService.get(text)
    print("SimHash:", sim_hash)
