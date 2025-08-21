import json
import os

import down
import search

# 检查config.json
config_path = f'{os.getcwd()}\\config.json'
if not os.path.exists(config_path):
    # 文件不存在，创建
    default_config = {
        "update": 0,
        "json_files": []
    }
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, ensure_ascii=False, indent=4)
    print('已创建 config.json 配置文件')

# 使用 'r+' 模式读写文本文件，写入前清空内容
with open(config_path, 'r+', encoding = 'utf-8') as file:
    try:
        settings = json.load(file)

        # 确保必要的字段存在
        if 'update' not in settings:
            settings['update'] = 0
        if 'json_files' not in settings:
            settings['json_files'] = []
        
        # 更新文件内容
        file.seek(0)
        json.dump(settings, file, ensure_ascii=False, indent=4)
        file.truncate()

        if settings.get('update', 0) == 1:
            print('skip initialization update.')

        else:
            print('首次运行请按照引导配置')
            search.update_books_data()
            print('The config.json was written.')

    except (json.decoder.JSONDecodeError, KeyError) as e:

        # 如果文件内容无效，重新加载并初始化 settings
        settings = {
            "update": 0,
            "json_files": []
        }
        search.update_books_data()
        print('The config.json was rewritten.')

while True:
    os.system('cls')
    choose = input('1.选择书籍\n2.下载书籍(教材URL|contentId|复制的IDs)\n3.更新教材数据\n4.退出\n请选择:')
    if choose == '1':
        os.system('cls')
        print('⚠️注意:有些学科只在特定年级有')
        print('\n选择学段：1.义务教育(包括五•四学制)  2.普通高中')
        xue_duan = input('请输入选项数字: ( 0 返回)')
        if xue_duan == '1':
            print(
                '\n义务教育:\n1.一年级   2.二年级   3.三年级   4.四年级   5.五年级   6.六年级   7.七年级   8.八年级   9.九年级')
            nian_ji_num = input('请输入选项数字: ( 0 返回)')
            if nian_ji_num in ['1', '2', '3', '4', '5', '6']:
                nian_ji_chs = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级'][int(nian_ji_num) - 1]
                # print('学科：1.语文\n2.数学\n3.英语\n4.物理\n5.化学\n6.生物\n7.历史\n8.地理\n9.政治')
                print(
                    '\n学科：1.语文    2.数学    3.英语    4.道德与法治    5.语文·书法练习指导    6.艺术    7.科学    8.体育与健康    9.信息科技')
                xue_ke = input('请输入选项数字: ( 0 返回)')
                if xue_ke in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    xue_ke_name = \
                    ['语文', '数学', '英语', '道德与法治', '语文·书法练习指导', '艺术', '科学', '体育与健康',
                     '信息科技'][int(xue_ke) - 1]
                    search_content = f'^.*义务教育.*{xue_ke_name}.*{nian_ji_chs}'
                    # print(f'正在搜索：{search_content}')
                    search.books_search(search_content, '1')
                else:
                    print('无效输入')
                    os.system('cls')
            elif nian_ji_num in ['7', '8', '9']:
                nian_ji_chs = ['七', '八', '九'][int(nian_ji_num) - 7]
                print(
                    '\n学科：1.道德与法治    2.语文    3.数学    4.英语    5.日语    6.俄语    7.体育与健康    8.艺术    9.科学    \n'
                    '10.物理    11.化学  12.生物学    13.历史    14.人文地理    15.地理    16.地理图册    17.信息科技    18.西班牙语    \n'
                    '19.德语    20.法语')
                xue_ke = input('请输入选项数字: ( 0 返回)')
                if xue_ke in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                              '17', '18', '19', '20']:
                    xue_ke_name = ['道德与法治', '语文', '数学', '英语', '日语', '俄语', '体育与健康', '艺术', '科学',
                                   '物理', '化学', '生物学', '历史', '人文地理', '地理', '地理图册', '信息科技',
                                   '西班牙语',
                                   '德语', '法语'][int(xue_ke) - 1]
                    search_content = f'^.*义务教育.*{xue_ke_name}.*{nian_ji_chs}.*$'
                    # print(f'正在搜索：{search_content}')
                    search.books_search(search_content, '1')
                else:
                    print('无效输入')
                    # os.system('cls')

        elif xue_duan == '2':
            print('\n学科：1.语文    2.数学    3.英语    4.日语    5.俄语    6.思想政治    7.历史    8.地理    9.地理图册    \n'
                  '10.物理    11.化学    12.生物学    13.信息技术    14.通用技术    15.音乐    16.美术    17.艺术    18.体育与健康    \n'
                  '19.西班牙语    20.德语    21.法语')
            xue_ke = input("请输入选项数字: ( 0 返回)")
            if xue_ke in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                          '18', '19', '20', '21']:
                xue_ke_name = ['语文', '数学', '英语', '日语', '俄语', '思想政治', '历史', '地理', '地理图册',
                               '物理', '化学', '生物学', '信息技术', '通用技术', '音乐', '美术', '艺术',
                               '体育与健康', '西班牙语', '德语', '法语'][int(xue_ke) - 1]
                search_content = f'普通高中.*{xue_ke_name}'
                # print(f'正在搜索：{search_content}')
                search.books_search(search_content, '1')
            else:
                print('无效输入')
                # os.system('cls')
        else:
            print('无效输入')


    elif choose == '2':
        down.down_books(input('请输入URL|ID:'))
    elif choose == '3':
        search.update_books_data()
    elif choose == '4':
        quit(114514)
    else:
        print('无效输入')


