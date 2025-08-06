import json
import os
import re
from time import sleep
from urllib.parse import parse_qs

import requests


# 通过DevTools抓包发现
# 教材pdf文件的URL>>> https://r3-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/<教材码(contentId)>.pkg/pdf.pdf
# 教材信息.json的URL>>> https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/<教材码(contentId)>.json
# 其中教材信息.json中的"global_title"字段下的"zh-CN"字段为教材名
# 好吧刚刚发现这个json其实还包含了教材pdf链接...
# 在"ti_items"字段的列表下[1]中的"ti_storages"有三个教材pdf链接


def down_books(query_string):
    book_json_urls = []
    while True:
        if 'https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=' in query_string:

            # 解析URL
            params = parse_qs(query_string)

            # 提取 contentId 的值
            content_id = params.get('contentId', [None])[0]

            print('contentId:', content_id)
            # url_output = f'https://r3-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/{content_id}.pkg/pdf.pdf'
            book_json_urls.append(
                f'https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/{content_id}.json')
            break
        elif isinstance(query_string, str) and re.match(
                r"^\['[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'(?:,\s*'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}')*\]$", query_string):
            query_string = query_string.strip("[]'") + ", "
            query_strings = query_string.split("', '")
            if len(query_strings) > 1:
                query_strings[-1] = query_strings[-1].strip(", ")
            try:
                query_strings.remove('')  # 什么鬼...
            except ValueError:
                pass
            for item in query_strings:
                # url_output = f'https://r3-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/{query_string}.pkg/pdf.pdf'
                book_json_urls.append(
                    f'https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/{item}.json')
            break
        elif isinstance(query_string, str) and re.match(
                r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", query_string):
            # 处理单个UUID格式的字符串
            content_id = query_string
            book_json_urls.append(
                f'https://s-file-1.ykt.cbern.com.cn/zxx/ndrv2/resources/tch_material/details/{content_id}.json')
            break

        else:
            print('无效输入')
            sleep(1)
            return


    # url = get_url()[0]
    # p_url = get_url()[1]
    # 解析 headers.json 为 json
    with open('headers.json', 'r') as headers_file:
        headers = json.loads(headers_file.read())  # headers.json to JSON
    print(f'\nHeaders:{headers}')

    # 请求教材pdf & 教材信息.json
    # pdf = requests.get(url, headers = headers)
    # book_json = requests.get(p_url, headers = headers)
    for json_url in book_json_urls:

        book_json = requests.get(json_url, headers = headers)
        # print(book_json.content)
        if book_json.status_code == 200:
            book_name = book_json.json()['global_title']['zh-CN']
            # 匹配ti_items字段下的"ti_format"为"pdf"
            book_url = None
            ti_items = book_json.json()["ti_items"]
            for item in ti_items:
                if item.get("ti_format") == "pdf":
                    book_url = item["ti_storages"][0]  # 默认取第一个链接
                    break

            print(f'\nbook_url: {book_url}\nDownloading...')
            pdf = requests.get(book_url, headers = headers)
            # print(book_name)
            print(f'\n{pdf.status_code}')
            # getpdf
            content = pdf.content
            # 接收字节数
            byte = len(pdf.content)
            print(f'接收字节：{byte}')
            # 计算文件大小
            size = round(byte / 1048576, 2)
            # 检查后缀
            if not book_name.endswith('.pdf'):
                book_name += '.pdf'
            # save_pdf
            with open(book_name, 'wb') as file:
                file.write(content)
                print(f'🎉保存成功>>>{os.getcwd()}\\{book_name}  ({size} MB)')
        elif book_json.status_code == 401:
            print('\n🤯Error 401 Unauthorized\n👀检查 headers.json 配置是否正确')
            os.system(f'explorer "https://basic.smartedu.cn/tchMaterial"')
            break
        else:
            print(f'\n🤯Error {book_json.status_code}\n👀检查教材码/教材URL是否正确')
        # print('--------')
    print('\n----Done.----')
    os.system('pause')


if __name__ == '__main__':
    down_books(input('请输入教材码/教材URL：'))
