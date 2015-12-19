# 学期课程查询比对

## 目的
根据课程代码，查询课程详情信息，与白皮书中信息做对比，查找不相同的数据

## 环境
Python 2.7
MonogoDB Server
Requests
pymongo
BeautifulSoup4

## 流程简要说明
1. 首先根据用户名和密码登录校园百合平台（教务处系统）
2. 读取本地csv文件
3. 将csv文件中的课程代码在百合平台查询课程信息，并保存到MongoDB
4. 将csv文件中的各个课程信息和数据库中信息做对比，不一致的数据记录下来

## 运行
1. 修改USER_NAME和PASSWORD为自己的信息
2. 执行`python main.py`
3. 程序读取CSV文件，并查询保存至MongoDB，把不一致的数据以JSON格式保存到`result.json`

## License
[MIT-Liscense](http://mit-license.org/) &copy; 2015 xNathan.