import unittest
from simhash_service import SimHashService


class TestSimHashService(unittest.TestCase):

    def test_get_with_none(self):
        """测试输入为 None 的情况"""
        result = SimHashService.get(None)
        self.assertIsNone(result)

    def test_get_with_empty_string(self):
        """测试输入为空字符串的情况"""
        result = SimHashService.get("")
        expected = "0" * 64  # 空字符串返回全零的 SimHash
        self.assertEqual(result, expected)

    def test_get_with_simple_string(self):
        """测试输入为简单字符串"""
        result = SimHashService.get("测试")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 64)  # 确保返回结果是64位

    def test_get_with_punctuation(self):
        """测试输入含有标点符号"""
        result = SimHashService.get("测试, 这是一个例子!")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 64)  # 确保返回结果是64位

    def test_get_with_chinese_text(self):
        """测试输入为中文文本"""
        text = "这是一个中文测试文本"
        result = SimHashService.get(text)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 64)  # 确保返回结果是64位
        # 可以进一步断言返回的 SimHash 是否符合预期

    def test_get_with_english_text(self):
        """测试输入为英文文本"""
        text = "This is a test text."
        result = SimHashService.get(text)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 64)  # 确保返回结果是64位

if __name__ == '__main__':
    unittest.main()
