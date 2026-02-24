import requests
import time
from typing import List, Dict, Any
from config import (
    BASE_URL,
    HEADERS,
    COLLECTION_TYPE_MAP,
    REQUEST_TIMEOUT,
    REQUEST_RETRY_TIMES,
    REQUEST_RETRY_DELAY,
    REQUEST_INTERVAL
)
from utils.logger import get_logger

logger = get_logger(__name__)


def fetch_with_retry(url: str, params: Dict[str, Any], retry_times: int = REQUEST_RETRY_TIMES) -> Dict[str, Any]:
    """
    带重试机制的 API 请求

    :param url: API URL
    :param params: 请求参数
    :param retry_times: 重试次数
    :return: API 返回的 JSON 数据
    :raises: Exception 请求失败时抛出异常
    """
    for attempt in range(retry_times):
        try:
            logger.debug(f"请求 URL: {url}, 参数: {params}")
            response = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            logger.debug(f"请求成功，返回 {len(data.get('data', []))} 条数据")
            return data
        except requests.RequestException as e:
            if attempt < retry_times - 1:
                wait_time = REQUEST_RETRY_DELAY * (attempt + 1)
                logger.warning(f"请求失败 (尝试 {attempt + 1}/{retry_times}): {e}，{wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                logger.error(f"请求失败，已重试 {retry_times} 次: {e}")
                raise Exception(f"API 请求失败: {str(e)}")


def get_user_collections(user_id: str, collection_type: str, per_page: int = 50) -> List[Dict[str, Any]]:
    """
    获取用户的番剧收藏列表

    :param user_id: Bangumi 用户 ID
    :param collection_type: 收藏类型（想看/在看/已看）
    :param per_page: 每页数量
    :return: 番剧收藏列表
    :raises: ValueError 不支持的收藏类型
    :raises: Exception API 请求失败
    """
    collections: List[Dict[str, Any]] = []
    page = 1
    type_id = COLLECTION_TYPE_MAP.get(collection_type)

    if not type_id:
        logger.error(f"不支持的收藏类型: {collection_type}")
        raise ValueError(f"不支持的收藏类型: {collection_type}")

    logger.info(f"开始获取用户 {user_id} 的 {collection_type} 番剧列表...")

    while True:
        url = f"{BASE_URL}/users/{user_id}/collections"
        params = {
            "subject_type": 2,
            "type": type_id,
            "limit": per_page,
            "offset": (page - 1) * per_page
        }

        try:
            data = fetch_with_retry(url, params)

            if not data.get("data"):
                logger.debug(f"第 {page} 页没有数据，停止获取")
                break

            page_collections = data["data"]
            collections.extend(page_collections)
            logger.debug(f"第 {page} 页获取到 {len(page_collections)} 条数据")

            if len(page_collections) < per_page:
                logger.debug("数据少于每页数量，停止获取")
                break

            page += 1

            if page > 1:
                time.sleep(REQUEST_INTERVAL)

        except Exception as e:
            logger.error(f"获取第 {page} 页数据时出错: {e}")
            raise

    logger.info(f"成功获取到 {len(collections)} 部番剧")
    return collections
