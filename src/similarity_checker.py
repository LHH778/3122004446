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

        # 对汉明距离为 -1 的情况进行异常处理
        if hamming_dist == -1:
            # raise InvalidHammingDistanceError("无效的汉明距离，可能是SimHash长度不一致或输入无效")
            print("无效的汉明距离，可能是SimHash长度不一致或输入无效")
            return -1

        print(f"汉明距离: {hamming_dist}")

        # 计算相似率
        similarity_rate = (64 - hamming_dist) / 64 * 100

        return similarity_rate

    # def check_similarity_with_exception_handling(self, text1, text2):
    #     try:
    #         return self.check_similarity(text1, text2)
    #     except InvalidHammingDistanceError as e:
    #         print(f"异常捕获: {str(e)}，相似率设置为1")
    #         return -1  # 返回相似率为 -1


# class InvalidHammingDistanceError(Exception):
#     """自定义异常类，用于处理无效的汉明距离"""
#
#     pass