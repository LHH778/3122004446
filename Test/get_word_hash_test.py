import unittest
from src.simhash_service import SimHashService

import coverage
cov = coverage.coverage()
cov.start()


# 定义一些大整数
BIGINT_0 = 0
BIGINT_1 = 1
BIGINT_2 = 2
BIGINT_1000003 = 1000003
BIGINT_2E64M1 = (BIGINT_2 ** 64) - BIGINT_1

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

    def test_multiple_characters(self):
        # 测试多个中文字符
        result = SimHashService.get_word_hash("你好世界")
        hash_value = (ord('你'[0]) << 12)  # 取中文字符的第一个字节
        for ch in "你好世界":
            hash_value = (hash_value * BIGINT_1000003) ^ ord(ch[0])  # 取每个中文字符的第一个字节
            hash_value &= BIGINT_2E64M1
        expected = hash_value ^ len("你好世界")
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

cov.stop()
cov.save()
# 命令行模式展示结果
cov.report()
# 生成HTML覆盖率报告
# cov.html_report(directory='result_html2')