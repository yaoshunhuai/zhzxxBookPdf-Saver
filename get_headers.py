import os
import time

from seleniumwire import webdriver


def get_request_headers():
    # 设置临时环境变量,防止selenium-manager找不到webdriver
    os.environ['PATH'] = os.environ.get("PATH") + ';' + os.getcwd()
    print(os.getenv('PATH'))

    # 添加证书
    if input('是否需要添加证书(推荐,减少ssl安全问题 | 需要管理员权限,请使用管理员权限运行):(Y/n)').lower() == 'y':
        os.system(f'certutil -addstore root {os.getcwd()}\ca.crt')

    # 创建driver
    driver = webdriver.Edge()

    # 登陆
    driver.get('https://auth.smartedu.cn/uias/login')

    # 判断
    while True:
        currentPageUrl = driver.current_url
        # print(f"当前页面的url是：{currentPageUrl}")
        time.sleep(1)
        if currentPageUrl == 'https://www.smartedu.cn/': # 登陆成功后跳转,进行检测
            print('登录成功')
            break
    driver.get('https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId='
               'b8e9a3fe-dae7-49c0-86cb-d146f883fd8e&catalogType=tchMaterial&subCatalog=tchMaterial')# 随便选本语文书
    time.sleep(15) # 等待书加载
    header_auth = None
    # 获取响应头
    for request in driver.requests:
        # 有三个链接
        target_urls = ['https://r3-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/%E6%99%AE%E9%80%9A%E9%AB%98%E4%B8%AD%E6%95%99%E7%A7%91%E4%B9%A6%20%E8%AF%AD%E6%96%87%20%E5%BF%85%E4%BF%AE%20%E4%B8%8A%E5%86%8C_1725097589060.pdf',
                       'https://r2-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/%E6%99%AE%E9%80%9A%E9%AB%98%E4%B8%AD%E6%95%99%E7%A7%91%E4%B9%A6%20%E8%AF%AD%E6%96%87%20%E5%BF%85%E4%BF%AE%20%E4%B8%8A%E5%86%8C_1725097589060.pdf',
                       'https://r1-ndr-private.ykt.cbern.com.cn/edu_product/esp/assets/b8e9a3fe-dae7-49c0-86cb-d146f883fd8e.pkg/%E6%99%AE%E9%80%9A%E9%AB%98%E4%B8%AD%E6%95%99%E7%A7%91%E4%B9%A6%20%E8%AF%AD%E6%96%87%20%E5%BF%85%E4%BF%AE%20%E4%B8%8A%E5%86%8C_1725097589060.pdf']
        if request.url in target_urls:
            print('响应headers：')
            print(request.headers)
            # 获取认证信息
            header_auth = request.headers.get('x-nd-auth')
            # print(header_auth)
            driver.quit()
            break

    # 返回响应头
    return header_auth

if __name__ == '__main__':
    auth = get_request_headers()
    if auth:
        print(f'获取到的认证信息: \n{auth}')
        os.system(f'set cmd_auth={auth}')
        os.system('echo %cmd_auth% | clip')
        os.system('echo 认证信息已复制到剪贴板')
        os.system('pause')
    else:
        print('未能获取到认证信息')
        os.system('pause')