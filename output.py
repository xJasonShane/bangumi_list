import csv
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)


def generate_filename(user_id: str, collection_type: str) -> str:
    """
    生成输出文件名

    :param user_id: 用户 ID
    :param collection_type: 收藏类型
    :return: 生成的文件名（不包含扩展名）
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bangumi_{user_id}_{collection_type}_{timestamp}"
    logger.debug(f"生成文件名: {filename}")
    return filename


def export_to_excel(data: List[Dict[str, Any]], selected_props: List[str], filename: str) -> str:
    """
    导出数据到 Excel 文件

    :param data: 番剧信息列表
    :param selected_props: 选择的属性列表
    :param filename: 文件名（不包含扩展名）
    :return: 完整的文件名
    """
    logger.info(f"导出 {len(data)} 条数据到 Excel 文件")
    df = pd.DataFrame(data)
    selected_df = df[selected_props]

    full_filename = f"{filename}.xlsx"
    selected_df.to_excel(full_filename, index=False, engine="openpyxl")

    logger.info(f"Excel 文件已生成: {full_filename}")
    return full_filename


def export_to_csv(data: List[Dict[str, Any]], selected_props: List[str], filename: str) -> str:
    """
    导出数据到 CSV 文件

    :param data: 番剧信息列表
    :param selected_props: 选择的属性列表
    :param filename: 文件名（不包含扩展名）
    :return: 完整的文件名
    """
    logger.info(f"导出 {len(data)} 条数据到 CSV 文件")
    full_filename = f"{filename}.csv"

    with open(full_filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=selected_props)
        writer.writeheader()
        for item in data:
            row = {prop: item.get(prop, "") for prop in selected_props}
            writer.writerow(row)

    logger.info(f"CSV 文件已生成: {full_filename}")
    return full_filename


def export_to_txt(data: List[Dict[str, Any]], selected_props: List[str], filename: str) -> str:
    """
    导出数据到 TXT 文件

    :param data: 番剧信息列表
    :param selected_props: 选择的属性列表
    :param filename: 文件名（不包含扩展名）
    :return: 完整的文件名
    """
    logger.info(f"导出 {len(data)} 条数据到 TXT 文件")
    full_filename = f"{filename}.txt"

    with open(full_filename, "w", encoding="utf-8") as f:
        f.write("\t".join(selected_props) + "\n")

        for item in data:
            row_data = [str(item.get(prop, "")) for prop in selected_props]
            f.write("\t".join(row_data) + "\n")

    logger.info(f"TXT 文件已生成: {full_filename}")
    return full_filename


def export_data(data: List[Dict[str, Any]], selected_props: List[str], filename: str, output_format: str) -> str:
    """
    根据指定格式导出数据

    :param data: 番剧信息列表
    :param selected_props: 选择的属性列表
    :param filename: 文件名（不包含扩展名）
    :param output_format: 输出格式（excel/txt/csv）
    :return: 完整的文件名
    :raises: ValueError 不支持的输出格式
    """
    if output_format == "excel":
        return export_to_excel(data, selected_props, filename)
    elif output_format == "csv":
        return export_to_csv(data, selected_props, filename)
    elif output_format == "txt":
        return export_to_txt(data, selected_props, filename)
    else:
        logger.error(f"不支持的输出格式: {output_format}")
        raise ValueError(f"不支持的输出格式: {output_format}")
