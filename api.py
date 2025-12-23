import requests
import time
from config import BASE_URL, HEADERS, COLLECTION_TYPE_MAP


def get_user_collections(user_id, collection_type, per_page=50):
    """
    获取用户的番剧收藏列表
    :param user_id: Bangumi用户ID
    :param collection_type: 收藏类型（想看/在看/已看）
    :param per_page: 每页数量
    :return: 番剧收藏列表
    """
    collections = []
    page = 1
    type_id = COLLECTION_TYPE_MAP.get(collection_type)
    
    if not type_id:
        raise ValueError(f"不支持的收藏类型: {collection_type}")
    
    while True:
        url = f"{BASE_URL}/users/{user_id}/collections"
        params = {
            "subject_type": 2,  # 2表示动画
            "type": type_id,
            "limit": per_page,
            "offset": (page - 1) * per_page
        }
        
        try:
            response = requests.get(url, params=params, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            
            # 检查是否有数据
            if not data["data"]:
                break
            
            collections.extend(data["data"])
            
            # 检查是否还有下一页
            if len(data["data"]) < per_page:
                break
            
            page += 1
            # 防止请求过快被封
            time.sleep(0.5)
            
        except requests.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    return collections