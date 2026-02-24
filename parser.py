from typing import List, Dict, Any
from config import ANIME_TYPE_MAP, COLLECTION_TYPE_REVERSE_MAP
from utils.logger import get_logger

logger = get_logger(__name__)


def parse_anime_info(collection: Dict[str, Any]) -> Dict[str, Any]:
    """
    解析番剧信息

    :param collection: 单条收藏记录
    :return: 解析后的番剧信息字典
    """
    subject = collection.get("subject", {})

    name = subject.get("name", "")
    name_cn = subject.get("name_cn", "")

    if not name_cn:
        name_cn = name

    type_id = subject.get("type", 0)
    type_name = ANIME_TYPE_MAP.get(type_id, "未知")

    collection_type_id = collection.get("type", 0)
    collection_status = COLLECTION_TYPE_REVERSE_MAP.get(collection_type_id, "未知")

    anime_info = {
        "番剧名": name,
        "中文名": name_cn,
        "话数": subject.get("eps", 0),
        "卷数": subject.get("volumes", 0),
        "发售日": subject.get("date", ""),
        "评分": subject.get("score", 0),
        "用户评分": collection.get("rate", 0),
        "类型": type_name,
        "状态": collection_status,
        "总收藏数": subject.get("collection_total", 0),
        "排名": subject.get("rank", 0)
    }

    return anime_info


def get_anime_list(user_collections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    将收藏列表转换为番剧信息列表

    :param user_collections: 用户收藏列表
    :return: 解析后的番剧信息列表
    """
    logger.debug(f"开始解析 {len(user_collections)} 条收藏记录")
    anime_list = [parse_anime_info(collection) for collection in user_collections]
    logger.debug(f"成功解析 {len(anime_list)} 条番剧信息")
    return anime_list
