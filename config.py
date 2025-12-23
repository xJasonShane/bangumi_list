# Bangumi API 配置
BASE_URL = "https://api.bgm.tv/v0"

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 收藏类型映射
COLLECTION_TYPE_MAP = {
    "想看": 1,
    "在看": 2,
    "已看": 3,
    "搁置": 4,
    "抛弃": 5
}

# 收藏类型逆向映射（用于显示）
COLLECTION_TYPE_REVERSE_MAP = {
    1: "想看",
    2: "在看",
    3: "已看",
    4: "搁置",
    5: "抛弃"
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
    "卷数",
    "发售日",
    "评分",
    "用户评分",
    "类型",
    "状态",
    "总收藏数",
    "排名"
]

# 分类选择映射
CATEGORY_CHOICES = {
    "1": "想看",
    "2": "在看",
    "3": "已看",
    "4": "搁置",
    "5": "抛弃"
}

# 输出格式选择映射
OUTPUT_FORMAT_CHOICES = {
    "1": "excel",
    "2": "txt"
}