from data_preprocessing import DataPreprocessing
from similarity_checker import SimilarityChecker
import time

if __name__ == "__main__":
    # 记录开始时间
    start_time = time.time()

    # 读取文件
    text1 = DataPreprocessing.read_file("D:\PyCharmCode\SimHash\\3122004446\DataSet\测试文本\orig.txt")
    text2 = DataPreprocessing.read_file("D:\PyCharmCode\SimHash\\3122004446\DataSet\测试文本\orig_0.8_add.txt")

    # 进行数据预处理
    processed_text1 = DataPreprocessing.preprocess_data(text1)
    processed_text2 = DataPreprocessing.preprocess_data(text2)

    # 初始化相似度检查器
    checker = SimilarityChecker(threshold=5)  # 设置汉明距离阈值为5

    # 进行论文查重
    similarity_rate = checker.check_similarity(processed_text1, processed_text2)

    # 输出相似率
    print(f"相似率: {similarity_rate:.2f}%")

    # 记录结束时间
    end_time = time.time()
    print(f"耗时: {(end_time - start_time):.2f} s")