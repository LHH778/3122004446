import unittest
from unittest.mock import patch
from data_preprocessing import DataPreprocessing

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

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="sample text")
    def test_read_file(self, mock_open):
        """测试 read_file 方法"""
        file_path = "dummy_path.txt"
        result = DataPreprocessing.read_file(file_path)
        expected = "sample text"
        self.assertEqual(result, expected)
        mock_open.assert_called_with(file_path, 'r', encoding='utf-8')

if __name__ == '__main__':
    unittest.main()
