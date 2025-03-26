import re
import json
from bs4 import BeautifulSoup

def clean_text(text):
    """
    清洗文本内容：
    - 去除HTML标签
    - 去除参考文献、外部链接等内容
    - 处理特殊符号和多余空格
    """
    # 去除 HTML 标签
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text()

    # 去除多余的空格
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    return clean_text

def remove_empty_lines(text):
    """
    移除文本中的多余空行，保证文档连续。
    """
    return re.sub(r'\n+', ' ', text)

def process_file(input_file, output_file, temp_file):
    """
    读取输入文件，清洗并转换为JSONL格式，保存临时文件。
    """
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile, open(temp_file, 'w', encoding='utf-8') as tempfile:
        line_number = 0  # 用于跟踪行号
        inside_doc = False  # 标记是否在<doc>标签内部
        doc_buffer = ""  # 用于存储临时的<doc>标签内容
        doc_id = None
        doc_url = None
        doc_title = None
        
        for line in infile:
            line_number += 1
            line = line.strip()

            # 跳过空行
            if not line:
                continue

            # 检测到带有信息的<doc>标签
            if line.startswith("<doc") and not inside_doc:
                match = re.search(r'<doc\s+id="(\d+)"\s+url="(https?://[^\s]+)"\s+title="([^"]+)">', line)
                if match:
                    inside_doc = True
                    doc_id = match.group(1)
                    doc_url = match.group(2)
                    doc_title = match.group(3)
                    doc_buffer = line  # 初始化doc内容缓存

            # 如果当前在处理一个<doc>标签，继续读取直到</doc>标签
            elif inside_doc:
                doc_buffer += " " + line.strip()
                
                # 如果遇到 </doc> 标签，表示当前文档结束
                if line == "</doc>":
                    # 保存中间文件（删除换行和空格后的文本）
                    temp_text = remove_empty_lines(doc_buffer)
                    tempfile.write(temp_text + "\n")  # 保存临时文件
                    
                    # 清洗并写入最终文件
                    cleaned_text = clean_text(remove_empty_lines(doc_buffer))

                    # 创建JSON对象并写入文件
                    data = {
                        "text": cleaned_text,
                        "meta": {
                            "title": doc_title,
                            "url": doc_url,
                            "id": doc_id
                        }
                    }
                    outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

                    # 重置状态
                    inside_doc = False
                    doc_buffer = ""  # 清空缓存

        # 输出匹配统计信息
        print(f"数据处理完成，结果已保存到: {output_file}")
        print(f"中间文件已保存到: {temp_file}")

def process_data(input_file, output_file, temp_file):
    """
    处理指定的文件。
    """
    process_file(input_file, output_file, temp_file)

# 输入文件路径和输出文件路径
input_file = '/home/puppytag/moonshot/Data/enwiki1/AA/wiki_00'  # WSL中的Linux风格路径
output_file = 'processed_data.jsonl'  # 输出文件
temp_file = 'temp_processed_data.txt'  # 临时文件，保存删除换行和空格后的内容

# 执行数据处理
process_data(input_file, output_file, temp_file)
