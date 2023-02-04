import json,requests,hashlib,re,os
import time
import hmac
import base64
import urllib.parse
text=''
TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
TG_USER_ID = os.environ["TG_USER_ID"]
phone = os.environ["admin"]
# 账号
password = os.environ["psw"]
# 密码
def user():
    # 葫芦侠登录
    md5 = hashlib.md5()
    md5.update(password.encode())
    password_md5 = md5.hexdigest()
    # 将密码转换MD5
    url = 'https://floor.huluxia.com/account/login/IOS/4.0'
    data = {
        'account': phone,
        'deviceCode': '',
        'device_code': '',
        'login_type': '2',
        'password': password_md5,
    }
    f = requests.post(url=url,data=data).json()
    # 将登录后返回的用户数据写入user.json
    json_str = json.dumps(f, indent=4)  
    with open('user.json', 'w') as f:
        f.write(json_str)
        

def sign_in(key):
    global text
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
        text=text+'板块:',i['title']/n
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
            text=text+"签到成功获得经验:",exp['experienceVal']/n


def mian():
    url = 'https://floor.huluxia.com/view/level'
    # 获取葫芦侠用户经验值url
    try:
        uj = open('user.json','r')
        user_json = json.loads(uj.read())
        uj.close()
        # 读取用户信息
        payload = {'viewUserID': user_json['user']['userID'],'_key':user_json['_key'],'theme': '0'}
        loh = requests.get(url=url,params=payload).text
        pattern = re.compile('请登录')
        # 检测key是否有效
        if pattern.search(loh):
            print('key已失效正在自动登录中')
            user()
            mian()
        else:
            sign_in(user_json['_key'])
    except FileNotFoundError:
        print('未检测到user.json正在创建登录')
        user()
        mian()

mian()



def tgBotNotify():
            global text
            url = 'https://api.telegram.org/bot' + TG_BOT_TOKEN + '/sendMessage'
            headers = {'Content-type': "application/x-www-form-urlencoded"}
            body = 'chat_id=' + TG_USER_ID + '&text=' + text+ '\n\n'  + '&disable_web_page_preview=true'
            
            
