import unittest
from src.simhash_service import SimHashService

import coverage
cov = coverage.coverage()
cov.start()

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
        self.assertEqual(result, 3)


if __name__ == '__main__':
    unittest.main()

cov.stop()
cov.save()
# 命令行模式展示结果
cov.report()