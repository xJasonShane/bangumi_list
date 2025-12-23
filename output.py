import pandas as pd
from datetime import datetime


def generate_filename(user_id, collection_type):
    """
    生成输出文件名
    :param user_id: 用户ID
    :param collection_type: 收藏类型
    :return: 生成的文件名（不包含扩展名）
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"bangumi_{user_id}_{collection_type}_{timestamp}"


def export_to_excel(data, selected_props, filename):
    """
    导出数据到Excel文件
    :param data: 番剧信息列表
    :param selected_props: 选择的属性列表
    :param filename: 文件名（不包含扩展名）
    :return: 完整的文件名
    """
    df = pd.DataFrame(data)
    selected_df = df[selected_props]
    
    full_filename = f"{filename}.xlsx"
    selected_df.to_excel(full_filename, index=False, engine="openpyxl")
    
    return full_filename


def export_to_txt(data, selected_props, filename):
    """
    导出数据到TXT文件
    :param data: 番剧信息列表
    :param selected_props: 选择的属性列表
    :param filename: 文件名（不包含扩展名）
    :return: 完整的文件名
    """
    full_filename = f"{filename}.txt"
    
    with open(full_filename, "w", encoding="utf-8") as f:
        # 写入表头
        f.write("\t".join(selected_props) + "\n")
        
        # 写入数据
        for item in data:
            row_data = [str(item.get(prop, "")) for prop in selected_props]
            f.write("\t".join(row_data) + "\n")
    
    return full_filename


def export_data(data, selected_props, filename, output_format):
    """
    根据指定格式导出数据
    :param data: 番剧信息列表
    :param selected_props: 选择的属性列表
    :param filename: 文件名（不包含扩展名）
    :param output_format: 输出格式（excel/txt）
    :return: 完整的文件名
    """
    if output_format == "excel":
        return export_to_excel(data, selected_props, filename)
    elif output_format == "txt":
        return export_to_txt(data, selected_props, filename)
    else:
        raise ValueError(f"不支持的输出格式: {output_format}")