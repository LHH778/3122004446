import argparse
import time
# from data_preprocessing import DataPreprocessing
# from similarity_checker import SimilarityChecker
import jieba
import re
from memory_profiler import profile

# 定义一些大整数
BIGINT_0 = 0
BIGINT_1 = 1
BIGINT_2 = 2
BIGINT_1000003 = 1000003
BIGINT_2E64M1 = (BIGINT_2 ** 64) - BIGINT_1

# 数据预处理类
class DataPreprocessing:
    @staticmethod
    def preprocess_data(text_content):
        try:
            if not text_content:
                return ""
            text_content = DataPreprocessing.to_dbc(text_content)
            text_content = re.sub(r'<.*?>', '', text_content)  # 去除HTML标签
            text_content = re.sub(r'[^\u4e00-\u9fa5]', '', text_content)  # 只保留中文字符
            return text_content
        except Exception as e:
            print(f"数据预处理时发生错误: {e}")
            return ""

    @staticmethod
    def to_dbc(input_str):
        """全角转半角"""
        try:
            result = []
            for char in input_str:
                code = ord(char)
                if code == 12288:  # 全角空格
                    code = 32
                elif 65281 <= code <= 65374:  # 全角字符 (其他字符按此范围转换)
                    code -= 65248
                result.append(chr(code))
            return ''.join(result)
        except Exception as e:
            print(f"全角转半角时发生错误: {e}")
            return input_str

    @staticmethod
    def read_file(file_path):
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"文件未找到: {file_path}")
            return -1
        except Exception as e:
            print(f"读取文件时发生错误: {e}")
            return -1


# SimHash服务类
class SimHashService:
    @staticmethod
    # @profile
    def get(text):
        try:
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
        except Exception as e:
            print(f"计算SimHash时发生错误: {e}")
            return None

    @staticmethod
    def get_word_hash(word):
        try:
            if not word:
                return BIGINT_0
            hash_value = (ord(word[0]) << 12)
            for ch in word:
                hash_value = (hash_value * BIGINT_1000003) ^ ord(ch)
                hash_value &= BIGINT_2E64M1  # 保持在64位内
            hash_value ^= len(word)
            return hash_value
        except Exception as e:
            print(f"计算词哈希时发生错误: {e}")
            return BIGINT_0

    @staticmethod
    def get_word_weight(word):
        """定义词的权重"""
        try:
            if not word:
                return 0
            length = len(word)
            if length == 1:
                return 1
            elif word[0] >= '\u3040':
                return 8 if length == 2 else 16
            else:
                return 2 if length == 2 else 4
        except Exception as e:
            print(f"计算词权重时发生错误: {e}")
            return 0

    @staticmethod
    def hamming_distance(a, b):
        try:
            if a is None or b is None:
                return -1
            if len(a) != len(b):
                return -1
            return sum(c1 != c2 for c1, c2 in zip(a, b))
        except Exception as e:
            print(f"计算汉明距离时发生错误: {e}")
            return -1


# 汉明码检查
class SimilarityChecker:
    def __init__(self, threshold=3):
        self.threshold = threshold  # 汉明距离的阈值

    def check_similarity(self, text1, text2):
        try:
            # 计算两篇文章的SimHash
            simhash1 = SimHashService.get(text1)
            simhash2 = SimHashService.get(text2)

            # 计算汉明距离
            hamming_dist = SimHashService.hamming_distance(simhash1, simhash2)

            # 对汉明距离为 -1 的情况进行异常处理
            if hamming_dist == -1:
                print("无效的汉明距离，可能是SimHash长度不一致或输入无效")
                return -1

            print(f"汉明距离: {hamming_dist}")

            # 计算相似率
            similarity_rate = (64 - hamming_dist) / 64 * 100

            return similarity_rate
        except Exception as e:
            print(f"相似度检查时发生错误: {e}")
            return -1


def main():
    try:
        # 记录开始时间
        start_time = time.time()

        # 解析命令行参数
        parser = argparse.ArgumentParser(description='论文查重工具')
        parser.add_argument(
            '--orig_path',
            type=str,
            help='论文原文的文件绝对路径',
            default='D:\PyCharmCode\SimHash\\3122004446\DataSet\测试文本\orig.txt'
        )
        parser.add_argument(
            '--plagiarized_path',
            type=str,
            help='抄袭版论文的文件绝对路径',
            default='D:\PyCharmCode\SimHash\\3122004446\DataSet\测试文本\orig_0.8_add.txt'
        )
        parser.add_argument(
            '--output_path',
            type=str,
            help='输出结果文件的绝对路径',
            default='D:/PyCharmCode/SimHash/3122004446/Result/output.txt'
        )
        args = parser.parse_args()

        # 读取文件
        text1 = DataPreprocessing.read_file(args.orig_path)
        text2 = DataPreprocessing.read_file(args.plagiarized_path)

        if text1 == -1 or text2 == -1:
            print("读取文件失败")
            return

        # 进行数据预处理
        processed_text1 = DataPreprocessing.preprocess_data(text1)
        processed_text2 = DataPreprocessing.preprocess_data(text2)

        # 初始化相似度检查器
        checker = SimilarityChecker(threshold=5)  # 设置汉明距离阈值为5

        # 进行论文查重
        similarity_rate = checker.check_similarity(processed_text1, processed_text2)

        if similarity_rate == -1:
            print("相似度检查失败")
            return

        # 输出相似率到文件
        with open(args.output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"相似率: {similarity_rate:.2f}%\n")
            output_file.write(f"耗时: {(time.time() - start_time):.2f} s\n")

        # 打印相似率到控制台
        print(f"相似率: {similarity_rate:.2f}%")
        print(f"耗时: {(time.time() - start_time):.2f} s")
    except Exception as e:
        print(f"主程序运行时发生错误: {e}")

if __name__ == "__main__":
    main()
