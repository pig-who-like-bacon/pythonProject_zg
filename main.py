import csv
import datetime
import json
import requests

def is_repeat(a, b):
    for u in a:
        if u['链接'] == b['链接']:
            return True
    return False

x = []
for i in range(1, 2920): 
# for i in range(1, 3):
    count = 0
    try_num = 0
    while count == 0 and try_num < 5:
        try_num += 1
        print('i', i)
        try:
            html2 = requests.get(
                'https://tieba.baidu.com/mg/f/getFrsData?kw=%E4%B8%AD%E5%8E%9F%E5%B7%A5%E5%AD%A6%E9%99%A2&rn=100&pn=' + str(
                    i))
            json_obj = json.loads(html2.text)
            # print(json_obj)
            for u in json_obj['data']['thread_list']:
                count += 1
                t = {
                    "回复": u['reply_num'],
                    "标题": u['title'],
                    "时间": datetime.datetime.fromtimestamp(u['create_time']).strftime('%Y-%m-%d %H:%M:%S'),
                    "链接": 'https://tieba.baidu.com/p/' + str(u['id']),
                    "简介": u['abstract'][0]['text']
                }
                if not is_repeat(x, t):
                    x.append(t)
            print('count', count)
            print()
        except Exception as e:
            print('第', i, '页异常')
            print(f"错误：{e}")

headers = ("回复", "标题", "时间", "链接", "简介")  # 元组 列表  集合
with open(f'res.csv', mode='w+', encoding='utf_8_sig', newline="") as f:
    # 创建一个字典数据的写入对象
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()  # 写入表头
    writer.writerows(x)
    print(f'保存成功')