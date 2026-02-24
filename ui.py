from typing import List
from config import ANIME_PROPERTIES, CATEGORY_CHOICES, OUTPUT_FORMAT_CHOICES
from utils.logger import get_logger

logger = get_logger(__name__)


def display_welcome() -> None:
    """显示欢迎信息"""
    print("=" * 60)
    print("欢迎使用 Bangumi 番剧清单获取工具 v2.0")
    print("=" * 60)
    logger.info("程序启动，显示欢迎信息")


def get_user_id() -> str:
    """
    获取用户输入的 Bangumi 用户 ID

    :return: 用户 ID
    """
    while True:
        user_id = input("\n请输入 Bangumi 用户 ID: ").strip()
        if user_id:
            logger.info(f"用户输入的 ID: {user_id}")
            return user_id
        print("错误：用户 ID 不能为空！")


def get_collection_type() -> str:
    """
    获取用户选择的收藏类型

    :return: 收藏类型（想看/在看/已看/搁置/抛弃）
    """
    print("\n请选择要获取的番剧分类：")
    for key, value in CATEGORY_CHOICES.items():
        print(f"{key}. {value}")

    while True:
        choice = input("请输入数字选择：").strip()
        collection_type = CATEGORY_CHOICES.get(choice)
        if collection_type:
            logger.info(f"用户选择的收藏类型: {collection_type}")
            return collection_type
        print("错误：无效的选择！请输入 1-5 之间的数字。")


def get_selected_properties() -> List[str]:
    """
    获取用户选择的番剧属性

    :return: 选择的属性列表
    """
    print("\n请选择要输出的番剧属性（可多选，用逗号分隔，例如：1,2,3）：")
    for i, prop in enumerate(ANIME_PROPERTIES, 1):
        print(f"{i}. {prop}")
    print("提示：直接输入 '0' 或 'all' 选择所有属性")

    while True:
        choice = input("请输入数字选择：").strip()
        if not choice:
            print("错误：属性选择不能为空！")
            continue

        if choice in ["0", "all", "ALL"]:
            logger.info("用户选择了所有属性")
            return ANIME_PROPERTIES.copy()

        selected_props = []
        for num in choice.split(","):
            num = num.strip()
            if num.isdigit():
                index = int(num) - 1
                if 0 <= index < len(ANIME_PROPERTIES):
                    selected_props.append(ANIME_PROPERTIES[index])

        if selected_props:
            logger.info(f"用户选择的属性: {selected_props}")
            return selected_props
        print("错误：无效的属性选择！请输入 1-11 之间的数字，用逗号分隔。")


def get_output_format() -> str:
    """
    获取用户选择的输出格式

    :return: 输出格式（excel/txt/csv）
    """
    print("\n请选择输出格式：")
    print("1. Excel (.xlsx)")
    print("2. TXT (.txt)")
    print("3. CSV (.csv)")

    while True:
        choice = input("请输入数字选择：").strip()
        output_format = OUTPUT_FORMAT_CHOICES.get(choice)
        if output_format:
            logger.info(f"用户选择的输出格式: {output_format}")
            return output_format
        print("错误：无效的输出格式选择！请输入 1-3 之间的数字。")


def display_summary(user_id: str, collection_type: str, selected_props: List[str], output_format: str) -> None:
    """
    显示用户选择的摘要信息

    :param user_id: 用户 ID
    :param collection_type: 收藏类型
    :param selected_props: 选择的属性列表
    :param output_format: 输出格式
    """
    print("\n" + "=" * 60)
    print("您的选择摘要：")
    print(f"  用户 ID: {user_id}")
    print(f"  收藏类型: {collection_type}")
    print(f"  输出属性 ({len(selected_props)} 项): {', '.join(selected_props)}")
    print(f"  输出格式: {output_format.upper()}")
    print("=" * 60)
    logger.info("显示用户选择摘要")
