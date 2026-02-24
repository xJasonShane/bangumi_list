import json
import hashlib
import time
from pathlib import Path
from typing import Any, Optional
from config import CACHE_ENABLED, CACHE_DIR, CACHE_TTL
from utils.logger import get_logger

logger = get_logger(__name__)


def get_cache_key(user_id: str, collection_type: str) -> str:
    """
    生成缓存键

    :param user_id: 用户 ID
    :param collection_type: 收藏类型
    :return: 缓存键
    """
    key_str = f"{user_id}:{collection_type}"
    return hashlib.md5(key_str.encode("utf-8")).hexdigest()


def get_cache_path(cache_key: str) -> Path:
    """
    获取缓存文件路径

    :param cache_key: 缓存键
    :return: 缓存文件路径
    """
    cache_dir = Path(CACHE_DIR)
    cache_dir.mkdir(exist_ok=True)
    return cache_dir / f"{cache_key}.json"


def load_cache(user_id: str, collection_type: str) -> Optional[Any]:
    """
    从缓存加载数据

    :param user_id: 用户 ID
    :param collection_type: 收藏类型
    :return: 缓存的数据，如果缓存不存在或已过期则返回 None
    """
    if not CACHE_ENABLED:
        return None

    cache_key = get_cache_key(user_id, collection_type)
    cache_path = get_cache_path(cache_key)

    if not cache_path.exists():
        logger.debug(f"缓存不存在: {cache_key}")
        return None

    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            cache_data = json.load(f)

        cached_time = cache_data.get("timestamp", 0)
        current_time = time.time()

        if current_time - cached_time > CACHE_TTL:
            logger.debug(f"缓存已过期: {cache_key}")
            return None

        logger.info(f"从缓存加载数据: {cache_key}")
        return cache_data.get("data")
    except Exception as e:
        logger.warning(f"读取缓存失败: {e}")
        return None


def save_cache(user_id: str, collection_type: str, data: Any) -> None:
    """
    保存数据到缓存

    :param user_id: 用户 ID
    :param collection_type: 收藏类型
    :param data: 要缓存的数据
    """
    if not CACHE_ENABLED:
        return

    cache_key = get_cache_key(user_id, collection_type)
    cache_path = get_cache_path(cache_key)

    try:
        cache_data = {
            "timestamp": time.time(),
            "user_id": user_id,
            "collection_type": collection_type,
            "data": data
        }

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

        logger.info(f"数据已缓存: {cache_key}")
    except Exception as e:
        logger.warning(f"保存缓存失败: {e}")
