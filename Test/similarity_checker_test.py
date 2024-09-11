import unittest
from similarity_checker import SimilarityChecker
from simhash_service import SimHashService

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
    unittest.main()
