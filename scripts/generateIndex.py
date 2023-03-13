# 负责生成../data.json
# 生成的数据格式为：
# {
#     "base-url": "http://www.baidu.com",
#     "list": [
#         {
#             "title": "20181211升旗",
#             "type": "image",
#             "content": "MjjnuqcxMOePrTIwMTjlubTmnIgxMeaXpeWNh+aXl+S7quW8j+iusOW9leOAgg==",
#             "url": "22223"
#         },
#         {
#             "title": "参考图",
#             "type": "image",
#             "content": "5qCh5Zut6aOO5pmv44CC",
#             "url": "112222"
#         },
#         {
#             "title": "毕业纪念",
#             "type": "video",
#             "content": "5qCh5Zut6aOO5pmv44CC",
#             "url": "121212"
#         }
#     ]
# }
# 其中，base-url为网站的根目录，list为数据列表，每个元素为一个数据，
# title为标题，type为类型，content为base64编码后的简介，url为链接
# 生成时，首先遍历../data目录下的所有文件夹，每个文件夹为一个数据
# 然后读取和文件夹同名的markdown文件，并读取这个md文件的meta data
# meta data的格式为：
# ---
# title: 20181211升旗
# type: image
# introduce: 28级10班2018年月11日升旗仪式记录。
# date: yyyy-mm-dd hh:mm:ss
# ---
# 其中，title为标题，type为类型，introduce为简介，date为日期
# json中的url为文件夹的名称，content为简介的base64编码
# 然后将这些数据写入到../data.json中
# 生成的数据将会被网站读取并展示

# requirements:
# markdown
# base64
# datetime

import os
import json
import base64

# 错误信息文件
errorFile = open('errors.txt', 'a', encoding='utf-8')

# 获取当前目录
currentPath = os.path.dirname(os.path.realpath(__file__))
# 获取data目录
dataPath = os.path.join(currentPath, '..', 'data')
# 获取data.json的路径
dataJsonPath = os.path.join(currentPath, '..', 'index.json')

# 获取data目录下的所有文件夹
dataFolders = os.listdir(dataPath)

# 生成的数据
data = {
    'base-url': '',
    'list': []
}

# 遍历data目录下的所有文件夹
for folder in dataFolders:
    try:
        # 获取文件夹的路径
        folderPath = os.path.join(dataPath, folder)
        # 判断文件夹是否存在
        if not os.path.isdir(folderPath):
            continue
        # 获取md文件的路径
        mdPath = os.path.join(folderPath, folder + '.md')
        # 判断md文件是否存在
        if not os.path.isfile(mdPath):
            continue
        # 读取md文件
        with open(mdPath, 'r', encoding='utf-8') as f:
            md = f.read()
            f.close()
        # 解析md文件的meta data
        # 使用re提取文件头部的两个---之间的内容
        # meta data的格式为：
        # ---
        # title: xxx
        # type: image
        # introduce: xxx
        # date: yyyy-mm-dd hh:mm:ss
        # ---

        # 现在提取meta
        if md.startswith("---"):
            metadata = md[3:md.find("---", 3)]
            md = md[md.find("---", 3) + 3:]
        else:
            # 写入错误信息
            errorFile.write("Meta data error: " + mdPath + '\n')
            continue

        # 将meta data转换为字典
        meta = {}
        for line in metadata.splitlines():
            if not ":" in line:
                continue
            key, value = line.split(": ")
            meta[key.strip()] = value.strip()

        # 获取标题
        title = meta['title']
        # 获取类型
        type = meta['type']
        # 获取简介
        introduce = meta['introduce']
        # 获取日期
        date = meta['date']
        # 获取链接
        url = folder
        # 将简介base64编码
        introduce = base64.b64encode(introduce.encode('utf-8')).decode('utf-8')
        # 将日期转换为时间戳
        # date = datetime.datetime.strptime(
        #     date, '%Y-%m-%d %H:%M:%S').timestamp()
        # 将数据添加到data中
        data['list'].append({
            'title': title,
            'type': type,
            'content': introduce,
            'url': url,
            'date': date
        })
    except Exception as e:
        # 写入错误信息
        errorFile.write("Error: " + mdPath + ' ' + str(e) + '\n')
        continue

errorFile.close()

# 将data转换为json字符串
dataJson = json.dumps(data, indent=4, ensure_ascii=False)
# 将json字符串写入到data.json中
with open(dataJsonPath, 'w', encoding='utf-8') as f:
    f.write(dataJson)
    f.close()
