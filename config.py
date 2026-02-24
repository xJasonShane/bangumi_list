import os
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()


# Bangumi API 配置
BASE_URL = os.getenv("BANGUMI_BASE_URL", "https://api.bgm.tv/v0")

# 请求头
USER_AGENT = os.getenv("BANGUMI_USER_AGENT", "bangumi_list/1.0.0 (+https://github.com/yourusername/bangumi_list)")
HEADERS = {
    "User-Agent": USER_AGENT
}

# 请求配置
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
REQUEST_RETRY_TIMES = int(os.getenv("REQUEST_RETRY_TIMES", "3"))
REQUEST_RETRY_DELAY = float(os.getenv("REQUEST_RETRY_DELAY", "1.0"))
REQUEST_INTERVAL = float(os.getenv("REQUEST_INTERVAL", "0.5"))

# 缓存配置
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
CACHE_DIR = os.getenv("CACHE_DIR", "cache")
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", "logs")

# 收藏类型映射
COLLECTION_TYPE_MAP: Dict[str, int] = {
    "想看": 1,
    "在看": 2,
    "已看": 3,
    "搁置": 4,
    "抛弃": 5
}

# 收藏类型逆向映射（用于显示）
COLLECTION_TYPE_REVERSE_MAP: Dict[int, str] = {
    1: "想看",
    2: "在看",
    3: "已看",
    4: "搁置",
    5: "抛弃"
}

# 番剧类型映射
ANIME_TYPE_MAP: Dict[int, str] = {
    1: "TV",
    2: "OVA",
    3: "剧场版",
    4: "Web动画",
    5: "电影",
    6: "其他"
}

# 番剧属性列表
ANIME_PROPERTIES: List[str] = [
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
CATEGORY_CHOICES: Dict[str, str] = {
    "1": "想看",
    "2": "在看",
    "3": "已看",
    "4": "搁置",
    "5": "抛弃"
}

# 输出格式选择映射
OUTPUT_FORMAT_CHOICES: Dict[str, str] = {
    "1": "excel",
    "2": "txt",
    "3": "csv"
}