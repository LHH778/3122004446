import unittest
from main import DataPreprocessing
from main import SimHashService
from main import SimilarityChecker

# 定义一些大整数
BIGINT_0 = 0
BIGINT_1 = 1
BIGINT_2 = 2
BIGINT_1000003 = 1000003
BIGINT_2E64M1 = (BIGINT_2 ** 64) - BIGINT_1

class TestDataPreprocessing(unittest.TestCase):

    def test_preprocess_data_with_valid_input(self):
        """测试 preprocess_data 方法，包含 HTML 标签和非中文字符"""
        text_content = "<html>这是一个测试! 123</html>"
        result = DataPreprocessing.preprocess_data(text_content)
        expected = "这是一个测试"  # 去除HTML标签和非中文字符后的结果
        self.assertEqual(result, expected)

    def test_preprocess_data_with_empty_input(self):
        """测试 preprocess_data 方法，输入为空字符串"""
        text_content = ""
        result = DataPreprocessing.preprocess_data(text_content)
        self.assertEqual(result, "")

    def test_preprocess_data_with_all_non_chinese(self):
        """测试 preprocess_data 方法，输入不包含中文字符"""
        text_content = "Hello, World! 123"
        result = DataPreprocessing.preprocess_data(text_content)
        self.assertEqual(result, "")

    def test_to_dbc_with_full_width_characters(self):
        """测试 to_dbc 方法，将全角字符转换为半角"""
        input_str = "ＡＢＣａｂｃ１２３！＠＃"
        result = DataPreprocessing.to_dbc(input_str)
        expected = "ABCabc123!@#"
        self.assertEqual(result, expected)

    def test_to_dbc_with_mixed_characters(self):
        """测试 to_dbc 方法，混合全角和半角字符"""
        input_str = "Hello ＡＢＣ"
        result = DataPreprocessing.to_dbc(input_str)
        expected = "Hello ABC"
        self.assertEqual(result, expected)

    def test_read_file(self):
        """测试 read_file 方法"""
        file_path = "D:\PyCharmCode\SimHash\\3122004446\DataSet\测试用例\DataPreprocessing.txt"
        result = DataPreprocessing.read_file(file_path)
        expected = "《软 件工程！，123"
        self.assertEqual(result, expected)

    def test_read_file_err1(self):
        """测试 read_file 方法 不存在次文件"""
        file_path = "D:\PyCharmCode\SimHash\\3122004446\DataSet\测试用例\DataPreprocessing_err1.txt"
        result = DataPreprocessing.read_file(file_path)
        # print(f"result7:{result}")
        expected = -1
        self.assertEqual(result, expected)


class TestGetWordHash(unittest.TestCase):
    def test_empty_string(self):
        # 测试空字符串输入
        result = SimHashService.get_word_hash("")
        self.assertEqual(result, BIGINT_0)

    def test_single_character(self):
        # 测试单字符输入
        result = SimHashService.get_word_hash("a")
        expected = ((ord('a') << 12) * BIGINT_1000003 ^ ord('a')) & BIGINT_2E64M1 ^ 1
        self.assertEqual(result, expected)

    def test_multiple_characters(self):
        # 测试多个字符输入
        result = SimHashService.get_word_hash("abc")
        hash_value = (ord('a') << 12)
        for ch in "abc":
            hash_value = (hash_value * BIGINT_1000003) ^ ord(ch)
            hash_value &= BIGINT_2E64M1
        expected = hash_value ^ len("abc")
        self.assertEqual(result, expected)

    def test_special_characters(self):
        # 测试包含特殊字符的输入
        result = SimHashService.get_word_hash("a@#")
        hash_value = (ord('a') << 12)
        for ch in "a@#":
            hash_value = (hash_value * BIGINT_1000003) ^ ord(ch)
            hash_value &= BIGINT_2E64M1
        expected = hash_value ^ len("a@#")
        self.assertEqual(result, expected)

    def test_multiple_character(self):
        # 测试单个中文字符
        result = SimHashService.get_word_hash("我")
        hash_value = (ord('我'[0]) << 12)  # 取中文字符的第一个字节
        for ch in "我":
            hash_value = (hash_value * BIGINT_1000003) ^ ord(ch[0])  # 取每个中文字符的第一个字节
            hash_value &= BIGINT_2E64M1
        expected = hash_value ^ len("我")
        self.assertEqual(result, expected)

    def test_multiple_characters_cn(self):
        # 测试多个中文字符
        result = SimHashService.get_word_hash("你好世界")
        hash_value = (ord('你'[0]) << 12)  # 取中文字符的第一个字节
        for ch in "你好世界":
            hash_value = (hash_value * BIGINT_1000003) ^ ord(ch[0])  # 取每个中文字符的第一个字节
            hash_value &= BIGINT_2E64M1
        expected = hash_value ^ len("你好世界")
        self.assertEqual(result, expected)


class TestHammingDistance(unittest.TestCase):

    def test_both_none(self):
        # 测试两个输入都为 None
        result = SimHashService.hamming_distance(None, None)
        self.assertEqual(result, -1)

    def test_one_none(self):
        # 测试其中一个输入为 None
        result = SimHashService.hamming_distance("abc", None)
        self.assertEqual(result, -1)
        result = SimHashService.hamming_distance(None, "abc")
        self.assertEqual(result, -1)

    def test_different_lengths(self):
        # 测试输入长度不同
        result = SimHashService.hamming_distance("abc", "abcd")
        self.assertEqual(result, -1)

    def test_same_strings(self):
        # 测试两个完全相同的字符串，汉明距离应该为 0
        result = SimHashService.hamming_distance("abc", "abc")
        self.assertEqual(result, 0)

    def test_partial_different(self):
        # 测试部分字符不同的字符串
        result = SimHashService.hamming_distance("abc", "abd")
        self.assertEqual(result, 1)

    def test_completely_different(self):
        # 测试所有字符都不同的字符串
        result = SimHashService.hamming_distance("abc", "xyz")
        # print(result)
        self.assertEqual(result, 3)

class TestSimilarityChecker(unittest.TestCase):

    def test_similarity_with_identical_text(self):
        """测试输入为相同文本的情况"""
        checker = SimilarityChecker()
        text = "广东工业大学"
        similarity = checker.check_similarity(text, text)
        self.assertEqual(similarity, 100.0)  # 相同文本相似率应为100%

    def test_similarity_with_completely_different_text(self):
        """测试输入为完全不同的文本"""
        checker = SimilarityChecker()
        text1 = "广东工业大学"
        text2 = "幼儿园"
        similarity = checker.check_similarity(text1, text2)
        self.assertLess(similarity, 100.0)  # 不同文本相似率应小于100%

    def test_similarity_with_similar_text(self):
        """测试输入为相似的文本"""
        checker = SimilarityChecker()
        text1 = "今天天气真好"
        text2 = "今天天气不错"
        similarity = checker.check_similarity(text1, text2)
        self.assertGreater(similarity, 0.0)  # 相似文本应有较高的相似率

    def test_similarity_threshold(self):
        """测试不同阈值下的相似性判断"""
        checker = SimilarityChecker(threshold=5)  # 设置不同的汉明距离阈值
        text1 = "今天天气真好"
        text2 = "今天天气不错"
        simhash1 = SimHashService.get(text1)
        simhash2 = SimHashService.get(text2)
        hamming_dist = SimHashService.hamming_distance(simhash1, simhash2)
        if hamming_dist <= 5:
            similarity = checker.check_similarity(text1, text2)
            self.assertGreater(similarity, 0.0)
        else:
            self.assertLess(checker.check_similarity(text1, text2), 100.0)

    def test_similarity_with_empty_string(self):
        """测试输入为空字符串"""
        checker = SimilarityChecker()
        similarity = checker.check_similarity("", "")
        self.assertEqual(similarity, 100.0)  # 空字符串应视为相同，相似率为100%

    def test_similarity_with_none(self):
        """测试输入为 None 的情况"""
        checker = SimilarityChecker()
        similarity = checker.check_similarity(None, None)
        self.assertEqual(similarity, -1)  # None 的情况下应返回0相似率

if __name__ == '__main__':
    # .. run your code ..
    print("start")
    unittest.main(verbosity=2)

# cov.stop()
# cov.save()
# # 命令行模式展示结果
# cov.report()
#
# # 生成HTML覆盖率报告
# cov.html_report(directory='result_html')

