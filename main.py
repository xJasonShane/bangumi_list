from api import get_user_collections
from parser import get_anime_list
from output import generate_filename, export_data
from ui import (
    display_welcome,
    get_user_id,
    get_collection_type,
    get_selected_properties,
    get_output_format
)


def main():
    """
    主程序入口
    """
    display_welcome()
    
    # 1. 获取用户输入
    user_id = get_user_id()
    collection_type = get_collection_type()
    selected_props = get_selected_properties()
    output_format = get_output_format()
    
    # 2. 获取番剧列表
    print(f"\n正在获取{user_id}的{collection_type}番剧列表...")
    try:
        collections = get_user_collections(user_id, collection_type)
        if not collections:
            print(f"未找到{user_id}的{collection_type}番剧列表！")
            return
        print(f"成功获取到 {len(collections)} 部番剧！")
    except Exception as e:
        print(f"获取失败：{str(e)}")
        return
    
    # 3. 解析番剧信息
    anime_list = get_anime_list(collections)
    
    # 4. 导出数据
    filename = generate_filename(user_id, collection_type)
    try:
        full_filename = export_data(anime_list, selected_props, filename, output_format)
        print(f"\n{output_format.upper()}文件已生成：{full_filename}")
        print("\n操作完成！")
    except Exception as e:
        print(f"导出失败：{str(e)}")
        return


if __name__ == "__main__":
    main()