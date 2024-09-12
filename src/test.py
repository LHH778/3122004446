# import unittest
# from main import DataPreprocessing
# from main import SimHashService
# from main import SimilarityChecker
#
# # 定义一些大整数
# BIGINT_0 = 0
# BIGINT_1 = 1
# BIGINT_2 = 2
# BIGINT_1000003 = 1000003
# BIGINT_2E64M1 = (BIGINT_2 ** 64) - BIGINT_1
#
# class TestDataPreprocessing(unittest.TestCase):
#     def test_to_dbc_with_mixed_characters(self):
#         """测试 to_dbc 方法，混合全角和半角字符"""
#         input_str = None
#         result = DataPreprocessing.to_dbc(input_str)
#         expected = None
#         self.assertEqual(result, expected)
#
# if __name__ == '__main__':
#     # .. run your code ..
#     print("start")
#     unittest.main(verbosity=2)

# import unittest
# from main import DataPreprocessing
# from main import SimHashService
# from main import SimilarityChecker
#
# # 定义一些大整数
# BIGINT_0 = 0
# BIGINT_1 = 1
# BIGINT_2 = 2
# BIGINT_1000003 = 1000003
# BIGINT_2E64M1 = (BIGINT_2 ** 64) - BIGINT_1
#
# class TestGetWordHash(unittest.TestCase):
#     def test_empty_string(self):
#         # 测试空字符串输入
#         result = SimHashService.get_word_weight(111)
#         self.assertEqual(result, BIGINT_0)
#
# if __name__ == '__main__':
#     # .. run your code ..
#     print("start")
#     unittest.main(verbosity=2)


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

class TestHammingDistance(unittest.TestCase):

    def test_both_none(self):
        # 测试两个输入都为 None
        result = SimHashService.hamming_distance("110", 110)
        self.assertEqual(result, -1)

if __name__ == '__main__':
    # .. run your code ..
    print("start")
    unittest.main(verbosity=2)