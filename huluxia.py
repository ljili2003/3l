import json,requests,hashlib,re

def sign_in(key):
    url = 'https://floor.huluxia.com/category/forum/list/IOS/1.0'
    # 获取所有板块url
    uri = 'https://floor.huluxia.com/category/forum/list/all/IOS/1.0'
    # 获取所有板块下的内容url
    urk = 'https://floor.huluxia.com/user/signin/IOS/1.1'
    # 签到板块url
    f = requests.post(url).json()
    # 获取所有板块
    categoryforum = f['categoryforum']
    for i in categoryforum:
        print('=' * 20)
        print('板块:',i['title'])
        f = requests.post(url=uri,data={'fum_id': i['id']}).json()
        # 获取所有板块下的内容
        for cat in f['categories']:
            print(cat['title'])
            # print(cat['categoryID'])
            headers = {
                'Host': 'floor.huluxia.com',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'User-Agent': 'Floor/1.3.0 (iPhone; iOS 15.3; Scale/3.00)',
                'Accept-Language': 'zh-Hans-CN;q=1',
                'Content-Length': '304',
                'Accept-Encoding': 'gzip, deflate, br'
            }
            exp = requests.post(url=urk,data={'_key': key,'cat_id': cat['categoryID']},headers=headers).json()
            # 签到板块
            print('签到成功获得经验:',exp['experienceVal'])
mian()
