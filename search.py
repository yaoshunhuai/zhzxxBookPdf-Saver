import json
import os
import re

import requests

web_jsons = []


def update_books_data():
    os.system('cls')
    json_book_data = requests.get(
        'https://s-file-1.ykt.cbern.com.cn/zxx/ndrs/resources/tch_material/version/data_version.json')
    data_urls = json_book_data.json()['urls']
    # print(data_urls)
    json_urls = data_urls.split(',')
    # print(urls)
    for url in json_urls:
        print(f'downloading...>>>{url}')
        json_file = requests.get(url)
        json_name = re.findall(r'part_\d+\.json', url)[0]
        folder_path = os.path.join(os.getcwd(), 'books_data')
        # print(folder_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f'创建 "{folder_path}"')

        with open(f'{folder_path}\\{json_name}', 'wb') as file:
            file.write(json_file.content)
        print(f'✅ {url}\n ┗━{json_name} downloaded.\n')
        web_jsons.append(json_name)


    settings_path = os.path.join(os.getcwd(), 'config.json')
    if os.path.exists(settings_path):
        with open(settings_path, 'r', encoding = 'utf-8') as file:
            existing_data = json.load(file)

        # 在 update 后插入
        existing_data["json_files"] = web_jsons

        # 写入更新后的数据
        with open(settings_path, 'w', encoding = 'utf-8') as file:
            json.dump(existing_data, file, ensure_ascii = False, indent = 4)
        # 从文件头开始覆写完成
        """
        优化books_data目录下JSON文件，保留必要字段
        """
        # JSON文件目录
        json_dir = r'.\books_data'

        # 检查配置文件获取JSON文件列表

        with open('config.json', 'r', encoding = 'utf-8') as settings:
            try:
                config_data = json.load(settings)
                json_files = config_data.get("json_files", [])
            except json.JSONDecodeError:
                print('❌ config.json 格式错误')
                return

        # 遍历处理每个JSON文件
        for json_file in json_files:
            file_path = os.path.join(json_dir, json_file)

            if not os.path.exists(file_path):
                print(f'❌NO SUCH FILE: {file_path}')
                continue

            print(f'正在处理: {json_file}')

            # 读取JSON文件
            with open(file_path, 'r', encoding = 'utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f'❌ {json_file} 格式错误，跳过')
                    continue

            # 清理数据，只保留必要字段
            cleaned_data = []
            for item in data:
                # 只保留需要的字段
                cleaned_item = {}

                # 必要字段
                if "id" in item:
                    cleaned_item["id"] = item["id"]

                if "global_title" in item and "zh-CN" in item["global_title"]:
                    cleaned_item["global_title"] = {"zh-CN": item["global_title"]["zh-CN"]}

                # 保留出版社信息
                if "provider_list" in item:
                    cleaned_item["provider_list"] = item["provider_list"]

                # 保留标签信息
                if "tag_list" in item:
                    cleaned_item["tag_list"] = item["tag_list"]

                # 保留下载相关
                if "ti_items" in item:
                    cleaned_item["ti_items"] = item["ti_items"]

                # 添加到清理后的数据中
                if cleaned_item:  # 确保有内容才添加
                    cleaned_data.append(cleaned_item)

            # 保存清理后的数据
            with open(file_path, 'w', encoding = 'utf-8') as f:
                json.dump(cleaned_data, f, ensure_ascii = False, indent = 4)

            print(f'✅ 已优化: {json_file}')

        header_x_nd_auth = input('输入引导配置header的内容:')

        # 读取现有，如果存在
        headers_file_path = 'headers.json'
        if os.path.exists(headers_file_path):
            try:
                with open(headers_file_path, 'r', encoding='utf-8') as f:
                    headers_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                headers_data = {}
        else:
            headers_data = {}
        
        # 更新x-nd-auth
        headers_data["x-nd-auth"] = header_x_nd_auth
        
        # 写入更新
        with open(headers_file_path, 'w', encoding='utf-8') as f:
            json.dump(headers_data, f, ensure_ascii=False, indent=4)

    # 保存设置
    if os.path.exists(settings_path):
        # 重新读取文件
        with open(settings_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
        
        # 设置 update 字段
        existing_data["update"] = 1

        # 写入更新
        with open(settings_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)


def books_search(keyword, mode):
    # JSON 文件所在目录
    json_dir = r'.\books_data'
    with open('config.json', 'r', encoding = 'utf-8') as settings:
        json_files = json.load(settings)["json_files"]

    all_titles = []

    # 遍历每个 JSON 文件并提取数据
    for json_file in json_files:
        file_path = os.path.join(json_dir, json_file)

        with open(file_path, 'r', encoding = 'utf-8') as f:
            data = json.load(f)

        for item in data:
            if "global_title" in item and "zh-CN" in item["global_title"]:
                title = item["global_title"]["zh-CN"]
                provider_name = ""

                # 处理出版社名称显示逻辑
                if "provider_list" in item and isinstance(item["provider_list"], list) and len(
                        item["provider_list"]) > 0:
                    first_provider = item["provider_list"][0]
                    if isinstance(first_provider, dict) and "name" in first_provider:
                        if first_provider["name"] == "智慧中小学":
                            if "label" in first_provider and isinstance(first_provider["label"], dict) and "zxx" in \
                                    first_provider["label"]:
                                provider_name = f'(zxx)'
                            else:
                                provider_name = '(智慧中小学)'
                        else:
                            provider_name = f'({first_provider["name"]})'

                # 优先显示 tag_dimension_id=zxxbb 的 tag_name
                tag_name = ""
                if "tag_list" in item and isinstance(item["tag_list"], list):
                    for tag in item["tag_list"]:
                        if isinstance(tag, dict) and "tag_dimension_id" in tag and tag["tag_dimension_id"] == "zxxbb":
                            tag_name = tag["tag_name"]
                            break
                if tag_name:
                    provider_name = f'({tag_name})'

                all_titles.append({
                    "title": title,
                    "id": item["id"],
                    "provider": provider_name
                })



    if mode == 0: # 模糊匹配
        print('自由搜索(未完工')
        filtered_titles = []
    elif mode == 1: # 正则匹配

        try:
            relaxed_pattern = re.compile(rf'.*{keyword}.*', re.IGNORECASE | re.UNICODE)
            filtered_titles = [t for t in all_titles if relaxed_pattern.search(t["title"])]

        except re.error:
            print('正则表达式无效，请检查输入格式')
            os.system('pause')
            return

    else:
        print('未知的 mode 模式')
        os.system('pause')
        return

    if not filtered_titles:
        print('未找到匹配的结果！')
        os.system('pause')
        return

    # 展示带编号和出版社名称的过滤结果
    print('\n匹配到以下结果：')
    for idx, title_info in enumerate(filtered_titles, start = 1):
        print(f'{idx}. {title_info['title']} {title_info['provider']}')

    # 添加出版社模糊匹配检索功能
    provider_search = input('\n是否根据教材版本筛选？(输入准确版本关键词，按Enter跳过): ').strip()
    if provider_search.upper() != '' and provider_search:
        # 根据出版社关键词进行模糊匹配筛选
        provider_filtered_titles = [t for t in filtered_titles if provider_search.lower() in t['provider'].lower()]
        if not provider_filtered_titles:
            print('🧐未找到匹配的版本')
            os.system('pause')
            return
        filtered_titles = provider_filtered_titles
        print(f'\n根据"{provider_search}"模糊匹配筛选后的结果：')
        for idx, title_info in enumerate(filtered_titles, start = 1):
            print(f'{idx}. {title_info['title']} {title_info['provider']}')

    # 用户批量选择输入
    try:
        choices_input = input('\n请输入编号选择（支持的格式：1 3 5 或 2-4）: ')
        selected_ids = []

        for part in choices_input.strip().split():
            if '-' in part:
                # 处理范围选择，例如 2-5
                start, end = map(int, part.split('-'))
                if start > end:
                    start, end = end, start
                for options in range(start, end + 1):
                    if 1 <= options <= len(filtered_titles):
                        selected_ids.append(filtered_titles[options - 1]["id"])
                    else:
                        print(f'编号 {options} 超出范围，已忽略。')
            else:
                # 单个编号
                idx = int(part)
                if 1 <= idx <= len(filtered_titles):
                    selected_ids.append(filtered_titles[idx - 1]["id"])
                else:
                    print(f'已忽略超出范围的编号 {idx} ')

        if selected_ids:
            print('\n你选择的 ID 列表是：')
            # 格式化输出每个 ID 及其对应的标题和出版社
            for idx, sid in enumerate(selected_ids, start = 1):
                matched = next((item for item in filtered_titles if item["id"] == sid), None)
                if matched:
                    title = matched["title"]
                    provider = matched["provider"]
                    print(f'{idx}. {title} {provider}')
                    print(f'{sid}\n')
                else:
                    print(f'{idx}. <未知条目>')
                    print(f'{sid}\n')

            print('📋 IDs:  (下载时复制完整一行)')
            print(repr(selected_ids))  # 使用 repr() 输出 Python 的列表格式
            os.system('pause')

        else:
            print('没有有效的选择。')
            os.system('pause')

    except ValueError:
        print('请输入有效的编号或范围，如：1 3 5 或 2-4')
        os.system('pause')