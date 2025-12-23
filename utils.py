import requests
import time

# bangumi API基础URL
BASE_URL = "https://api.bgm.tv/v0"

# API请求头，添加User-Agent避免403
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 收藏类型映射
COLLECTION_TYPE_MAP = {
    "想看": 1,
    "在看": 2,
    "已看": 3
}

# 番剧类型映射
ANIME_TYPE_MAP = {
    1: "TV",
    2: "OVA",
    3: "剧场版",
    4: "Web动画",
    5: "电影",
    6: "其他"
}

# 番剧属性列表
ANIME_PROPERTIES = [
    "番剧名",
    "中文名",
    "话数",
    "发售日",
    "评分",
    "状态",
    "类型"
]


def get_user_collections(user_id, collection_type, per_page=50):
    """
    获取用户的番剧收藏列表
    :param user_id: bangumi用户ID
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


def parse_anime_info(collection):
    """
    解析番剧信息
    :param collection: 单条收藏记录
    :return: 解析后的番剧信息字典
    """
    subject = collection["subject"]
    
    # 提取基本信息
    name = subject.get("name", "")
    name_cn = subject.get("name_cn", "")
    
    # 当中文名空时用番剧名代替
    if not name_cn:
        name_cn = name
    
    # 获取类型名称
    type_id = subject.get("type", 0)
    type_name = ANIME_TYPE_MAP.get(type_id, "未知")
    
    anime_info = {
        "番剧名": name,
        "中文名": name_cn,
        "话数": subject.get("eps", 0),
        "发售日": subject.get("date", ""),
        "评分": subject.get("score", 0),
        "类型": type_name,
        "状态": collection.get("type_name", "")
    }
    
    return anime_info


def get_anime_list(user_id, collection_type):
    """
    获取并解析用户的番剧列表
    :param user_id: bangumi用户ID
    :param collection_type: 收藏类型（想看/在看/已看）
    :return: 解析后的番剧列表
    """
    collections = get_user_collections(user_id, collection_type)
    anime_list = [parse_anime_info(collection) for collection in collections]
    return anime_list