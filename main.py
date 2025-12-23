import pandas as pd
from utils import get_anime_list, ANIME_PROPERTIES


def main():
    print("欢迎使用Bangumi番剧清单获取工具！")
    print("=" * 50)
    
    # 1. 获取用户ID
    user_id = input("请输入Bangumi用户ID: ").strip()
    if not user_id:
        print("错误：用户ID不能为空！")
        return
    
    # 2. 选择分类
    print("\n请选择要获取的番剧分类：")
    print("1. 想看")
    print("2. 在看")
    print("3. 已看")
    
    category_choice = input("请输入数字选择：").strip()
    category_map = {
        "1": "想看",
        "2": "在看",
        "3": "已看"
    }
    
    collection_type = category_map.get(category_choice)
    if not collection_type:
        print("错误：无效的选择！")
        return
    
    # 3. 选择属性
    print("\n请选择要输出的番剧属性（可多选，用逗号分隔，例如：1,2,3）：")
    for i, prop in enumerate(ANIME_PROPERTIES, 1):
        print(f"{i}. {prop}")
    
    prop_choice = input("请输入数字选择：").strip()
    if not prop_choice:
        print("错误：属性选择不能为空！")
        return
    
    selected_props = []
    for choice in prop_choice.split(","):
        choice = choice.strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(ANIME_PROPERTIES):
                selected_props.append(ANIME_PROPERTIES[index])
    
    if not selected_props:
        print("错误：无效的属性选择！")
        return
    
    # 4. 选择输出格式
    print("\n请选择输出格式：")
    print("1. Excel (.xlsx)")
    print("2. TXT (.txt)")
    
    format_choice = input("请输入数字选择：").strip()
    if format_choice == "1":
        output_format = "excel"
    elif format_choice == "2":
        output_format = "txt"
    else:
        print("错误：无效的输出格式选择！")
        return
    
    # 5. 获取番剧列表
    print(f"\n正在获取{user_id}的{collection_type}番剧列表...")
    try:
        anime_list = get_anime_list(user_id, collection_type)
        if not anime_list:
            print(f"未找到{user_id}的{collection_type}番剧列表！")
            return
        print(f"成功获取到 {len(anime_list)} 部番剧！")
    except Exception as e:
        print(f"获取失败：{str(e)}")
        return
    
    # 6. 数据处理
    df = pd.DataFrame(anime_list)
    selected_df = df[selected_props]
    
    # 7. 输出文件
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bangumi_{user_id}_{collection_type}_{timestamp}"
    
    if output_format == "excel":
        filename += ".xlsx"
        selected_df.to_excel(filename, index=False, engine="openpyxl")
        print(f"\nExcel文件已生成：{filename}")
    else:
        filename += ".txt"
        with open(filename, "w", encoding="utf-8") as f:
            # 写入表头
            f.write("\t".join(selected_props) + "\n")
            # 写入数据
            for _, row in selected_df.iterrows():
                f.write("\t".join([str(val) for val in row.tolist()]) + "\n")
        print(f"\nTXT文件已生成：{filename}")
    
    print("\n操作完成！")


if __name__ == "__main__":
    main()