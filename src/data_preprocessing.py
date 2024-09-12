import re

class DataPreprocessing:
    @staticmethod
    def preprocess_data(text_content):
        if not text_content:
            return ""
        text_content = DataPreprocessing.to_dbc(text_content)
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
    def read_file(file_path):
        """读取文件内容"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

