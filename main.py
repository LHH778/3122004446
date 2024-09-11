import argparse
import time
from data_preprocessing import DataPreprocessing
from similarity_checker import SimilarityChecker

def main():
    # 记录开始时间
    start_time = time.time()

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='论文查重工具')
    parser.add_argument(
        '--orig_path',
        type=str,
        help='论文原文的文件绝对路径',
        default='D:\PyCharmCode\SimHash\\3122004446\DataSet\测试文本\orig.txt'
    )
    parser.add_argument(
        '--plagiarized_path',
        type=str,
        help='抄袭版论文的文件绝对路径',
        default='D:\PyCharmCode\SimHash\\3122004446\DataSet\测试文本\orig_0.8_add.txt'
    )
    parser.add_argument(
        '--output_path',
        type=str,
        help='输出结果文件的绝对路径',
        default='D:/PyCharmCode/SimHash/3122004446/Result/output.txt'
    )
    args = parser.parse_args()

    # 读取文件
    text1 = DataPreprocessing.read_file(args.orig_path)
    text2 = DataPreprocessing.read_file(args.plagiarized_path)

    # 进行数据预处理
    processed_text1 = DataPreprocessing.preprocess_data(text1)
    processed_text2 = DataPreprocessing.preprocess_data(text2)

    # 初始化相似度检查器
    checker = SimilarityChecker(threshold=5)  # 设置汉明距离阈值为5

    # 进行论文查重
    similarity_rate = checker.check_similarity(processed_text1, processed_text2)

    # 输出相似率到文件
    with open(args.output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"相似率: {similarity_rate:.2f}%\n")
        output_file.write(f"耗时: {(time.time() - start_time):.2f} s\n")

    # 打印相似率到控制台
    print(f"相似率: {similarity_rate:.2f}%")
    print(f"耗时: {(time.time() - start_time):.2f} s")

if __name__ == "__main__":
    main()








# from data_preprocessing import DataPreprocessing
# from similarity_checker import SimilarityChecker
# import time
#
# if __name__ == "__main__":
#     # 记录开始时间
#     start_time = time.time()
#
#     # 读取文件
#     text1 = DataPreprocessing.read_file("D:\PyCharmCode\SimHash\\3122004446\DataSet\测试文本\orig.txt")
#     text2 = DataPreprocessing.read_file("D:\PyCharmCode\SimHash\\3122004446\DataSet\测试文本\orig_0.8_add.txt")
#
#     # 进行数据预处理
#     processed_text1 = DataPreprocessing.preprocess_data(text1)
#     processed_text2 = DataPreprocessing.preprocess_data(text2)
#
#     # 初始化相似度检查器
#     checker = SimilarityChecker(threshold=5)  # 设置汉明距离阈值为5
#
#     # 进行论文查重
#     similarity_rate = checker.check_similarity(processed_text1, processed_text2)
#
#     # 输出相似率
#     print(f"相似率: {similarity_rate:.2f}%")
#
#     # 记录结束时间
#     end_time = time.time()
#     print(f"耗时: {(end_time - start_time):.2f} s")