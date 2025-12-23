from config import ANIME_TYPE_MAP


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
        "卷数": subject.get("volumes", 0),
        "发售日": subject.get("date", ""),
        "评分": subject.get("score", 0),
        "用户评分": collection.get("rate", 0),
        "类型": type_name,
        "状态": collection.get("type_name", ""),
        "总收藏数": subject.get("collection_total", 0),
        "排名": subject.get("rank", 0)
    }
    
    return anime_info


def get_anime_list(user_collections):
    """
    将收藏列表转换为番剧信息列表
    :param user_collections: 用户收藏列表
    :return: 解析后的番剧信息列表
    """
    return [parse_anime_info(collection) for collection in user_collections]