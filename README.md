# 智慧中小学教材下载

* 前往

# 支持的功能

* 程序内批量选择教材
* 教材url下载|教材ID下载|程序内批量教材下载

# 使用教程

### 设置headers

(可以使用 `get_hearders.py` 登陆网页自动完成, 手动粘贴)

* 访问 `https://basic.smartedu.cn/tchMaterial` 并登录，进入教材页面，随便选取一本教材，进入教材页面。
* 按下`F12`，在弹出的开发人员工具栏中，选择`网络`（如图）
  ![](./pictures/a.png)
* 按下`Ctrl`+`R`键，刷新页面，待页面刷新完毕，先点击 `Fetch/XHR` ，再在筛选器栏中输入 `pdf` （如图）
  ![](./pictures/b.png)
* 先点击小三角展开，找到状态为 `200` 且发起程序为 `pdfjs:22` 的一项（如图）并选中
  ![](./pictures/c.png)
* 选中符合上图条件项，选中并复制 `X-Nd-Auth` 字段的所有内容

![](./pictures/d.png)

* 在程序中粘贴

![](./pictures/e.png)
