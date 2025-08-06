# 智慧中小学教材下载

* 前往 [release](https://github.com/yaoshunhuai/SmartEdu-downloader/releases/) 下载使用 [pyinstaller](https://github.com/pyinstaller/pyinstaller) 打包的可执行文件
* 自己在DevTools里抓包一个一个下载效率堪忧,一时兴起
* 刚刚中考完,闲在家,大多数库为现学现卖,质量不高望包涵

# 支持的功能

* 程序内批量选择教材
* 教材url下载|教材ID下载|程序内批量教材下载

# 使用教程

### 设置headers

(可以使用 `get_hearders.py`(已打包在 [release](https://github.com/yaoshunhuai/SmartEdu-downloader/releases/)) 登陆网页自动完成, 手动粘贴)
(源码运行时,请把Edge的WebDriver可执行文件放入运行路径同级目录下)

* 访问 `https://basic.smartedu.cn/tchMaterial` 并登录，进入教材页面，随便选取一本教材，进入教材页面。
* 按下`F12`，在弹出的开发人员工具栏中，选择`网络`（如图）
  ![](https://github.com/yaoshunhuai/SmartEdu-downloader/blob/main/pictures/a.png?raw=true)
* 按下`Ctrl`+`R`键，刷新页面，待页面刷新完毕，先点击 `Fetch/XHR` ，再在筛选器栏中输入 `pdf` （如图）
  ![](https://github.com/yaoshunhuai/SmartEdu-downloader/blob/main/pictures/b.png?raw=true)
* 先点击小三角展开，找到状态为 `200` 且发起程序为 `pdfjs:22` 的一项（如图）并选中
  ![](https://github.com/yaoshunhuai/SmartEdu-downloader/blob/main/pictures/c.png?raw=true)
* 选中符合上图条件项，选中并复制 `X-Nd-Auth` 字段的所有内容
  ![](https://github.com/yaoshunhuai/SmartEdu-downloader/blob/main/pictures/d.png?raw=true)
* 在程序中粘贴
  ![](https://github.com/yaoshunhuai/SmartEdu-downloader/blob/main/pictures/e.png?raw=true)
