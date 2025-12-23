from config import ANIME_PROPERTIES, CATEGORY_CHOICES, OUTPUT_FORMAT_CHOICES


def display_welcome():
    """
    显示欢迎信息
    """
    print("欢迎使用Bangumi番剧清单获取工具！")
    print("=" * 50)


def get_user_id():
    """
    获取用户输入的Bangumi用户ID
    :return: 用户ID
    """
    while True:
        user_id = input("请输入Bangumi用户ID: ").strip()
        if user_id:
            return user_id
        else:
            print("错误：用户ID不能为空！")


def get_collection_type():
    """
    获取用户选择的收藏类型
    :return: 收藏类型（想看/在看/已看）
    """
    print("\n请选择要获取的番剧分类：")
    for key, value in CATEGORY_CHOICES.items():
        print(f"{key}. {value}")
    
    while True:
        choice = input("请输入数字选择：").strip()
        collection_type = CATEGORY_CHOICES.get(choice)
        if collection_type:
            return collection_type
        else:
            print("错误：无效的选择！")


def get_selected_properties():
    """
    获取用户选择的番剧属性
    :return: 选择的属性列表
    """
    print("\n请选择要输出的番剧属性（可多选，用逗号分隔，例如：1,2,3）：")
    for i, prop in enumerate(ANIME_PROPERTIES, 1):
        print(f"{i}. {prop}")
    
    while True:
        choice = input("请输入数字选择：").strip()
        if not choice:
            print("错误：属性选择不能为空！")
            continue
        
        selected_props = []
        for num in choice.split(","):
            num = num.strip()
            if num.isdigit():
                index = int(num) - 1
                if 0 <= index < len(ANIME_PROPERTIES):
                    selected_props.append(ANIME_PROPERTIES[index])
        
        if selected_props:
            return selected_props
        else:
            print("错误：无效的属性选择！")


def get_output_format():
    """
    获取用户选择的输出格式
    :return: 输出格式（excel/txt）
    """
    print("\n请选择输出格式：")
    print("1. Excel (.xlsx)")
    print("2. TXT (.txt)")
    
    while True:
        choice = input("请输入数字选择：").strip()
        output_format = OUTPUT_FORMAT_CHOICES.get(choice)
        if output_format:
            return output_format
        else:
            print("错误：无效的输出格式选择！")