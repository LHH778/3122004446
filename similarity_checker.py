from simhash_service import SimHashService


class SimilarityChecker:
    def __init__(self, threshold=3):
        self.threshold = threshold  # 汉明距离的阈值

    def check_similarity(self, text1, text2):
        # 计算两篇文章的SimHash
        simhash1 = SimHashService.get(text1)
        simhash2 = SimHashService.get(text2)

        # 计算汉明距离
        hamming_dist = SimHashService.hamming_distance(simhash1, simhash2)

        print(f"汉明距离: {hamming_dist}")

        # 计算相似率
        similarity_rate = (64 - hamming_dist) / 64 * 100

        return similarity_rate
