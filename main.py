import sys
import os
from wikiextractor import WikiExtractor

def main():

    # 设置要执行的命令及其参数
    command = [
        sys.executable,  # Python 解释器路径
        "-m", "wikiextractor.WikiExtractor",  # 模块路径
        "-b", "2048M",  # 设置分块大小为 2048MB
        "-o", "Data/enwiki",  # 输出目录
        "Data/zhwiki-20250201-pages-articles-multistream.xml.bz2"  # 输入文件路径
    ]

    # 使用 os.system 执行命令
    os.system(" ".join(command))

if __name__ == "__main__":
    main()
