import sys
from api import get_user_collections
from parser import get_anime_list
from output import generate_filename, export_data
from ui import (
    display_welcome,
    get_user_id,
    get_collection_type,
    get_selected_properties,
    get_output_format,
    display_summary
)
from cache import load_cache, save_cache
from config import LOG_LEVEL, LOG_DIR
from utils.logger import setup_logger, get_logger


def main() -> int:
    """
    主程序入口

    :return: 退出码
    """
    logger = setup_logger(level=getattr(logging, LOG_LEVEL.upper(), logging.INFO), log_dir=LOG_DIR)
    logger.info("=" * 60)
    logger.info("程序启动")

    try:
        display_welcome()

        user_id = get_user_id()
        collection_type = get_collection_type()
        selected_props = get_selected_properties()
        output_format = get_output_format()

        display_summary(user_id, collection_type, selected_props, output_format)

        logger.info(f"正在获取 {user_id} 的 {collection_type} 番剧列表...")

        cached_data = load_cache(user_id, collection_type)
        if cached_data:
            print("\n使用缓存数据...")
            collections = cached_data
        else:
            print(f"\n正在从 Bangumi 获取 {user_id} 的 {collection_type} 番剧列表...")
            collections = get_user_collections(user_id, collection_type)
            save_cache(user_id, collection_type, collections)

        if not collections:
            print(f"未找到 {user_id} 的 {collection_type} 番剧列表！")
            logger.warning(f"未找到 {user_id} 的 {collection_type} 番剧列表")
            return 0

        print(f"成功获取到 {len(collections)} 部番剧！")
        logger.info(f"成功获取到 {len(collections)} 部番剧")

        print("\n正在解析番剧信息...")
        anime_list = get_anime_list(collections)
        logger.info(f"成功解析 {len(anime_list)} 条番剧信息")

        print("\n正在导出数据...")
        filename = generate_filename(user_id, collection_type)
        full_filename = export_data(anime_list, selected_props, filename, output_format)

        print(f"\n{output_format.upper()} 文件已生成：{full_filename}")
        print("\n操作完成！")
        logger.info(f"操作完成，文件已保存到: {full_filename}")

        return 0

    except KeyboardInterrupt:
        print("\n\n操作已被用户取消。")
        logger.info("程序被用户中断")
        return 130
    except Exception as e:
        print(f"\n错误：{str(e)}")
        logger.error(f"程序运行出错: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    import logging
    sys.exit(main())
