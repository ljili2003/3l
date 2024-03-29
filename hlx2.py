# -*- coding: UTF-8 -*-
"""
* @脚本作者: 佚名RJ
* @创建时间: 2023/05/11 10:17
* @目标地址:
* @软件版本: V1.0
* @脚本用途: 葫芦侠三楼使用_key一键签到的脚本
* @使用说明: 手机抓包获取葫芦侠三楼账号登录的_key参数，运行此脚本填入即可！
* @其它说明: 注释第31行,使用第32行并将_key填入，可挂云函数使用。
 
"""
 
import requests
import time
import hashlib
import os
import json
 
#tg
TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
TG_USER_ID = os.environ["TG_USER_ID"] 
# MD5加密密码
def md5(param):
    m = hashlib.md5()
    b = param.encode(encoding='utf-8')
    m.update(b)
    passwd_md5 = m.hexdigest()
    return passwd_md5
 
# 签到函数
def signin():
    #登录获取key
    username = os.environ["admin"] #手机号
    password = os.environ["psw"]  #密码
    # 获取密码md5
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    #sign计算
    sign = "account" + username + "device_code[d]b305cc73-8db8-4a25-886f-e73c502b1e99password" + password + "voice_codefa1c28a5b62e79c3e63d9030b6142e4b"
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
    #提交地址
    url = "http://floor.huluxia.com/account/login/ANDROID/4.1.8?platform=2&gkey=000000&app_version=4.2.1.6.1&versioncode=367&market_id=tool_web&_key=&device_code=%5Bd%5Db305cc73-8db8-4a25-886f-e73c502b1e99&phone_brand_type=VO"
    #登录提交数据
    data = {
    'account': username,
    'login_type': '2',
    'password': password,
    'sign': sign}
    #协议头
    headers = {"User-Agent": "okhttp/3.8.1"}
    #请求访问
    retu = requests.post(url=url, data=data, headers=headers)
    retu.encoding = retu.apparent_encoding
    #json解析
    login_json = json.loads(retu.text)
    #提取key数据
    _key = login_json['_key']
    # _key参数抓登录包获取
    # _key = input("请输入抓包账号响应获取的_key：")
    # _key = ""
    print("============================开始签到请耐心等待============================")
    number = 0  # 成功计数
    continueDays = 0  # 连续签到天数
    experienceVal = 0  # 本次签到经验
 
    # 每个版块的ID，包含隐藏版块ID
    for i in range(1, 122):
        cat_id = str(i)
        # print(cat_id)
 
        # 获取时间戳
        time_s = str(time.time()).split(".")[0] + str(time.time()).split(".")[1][0:3]
        # print(time_s)   # 1683335343675
 
        # 无需device_code版本
        url = f"http://floor.huluxia.com/user/signin/ANDROID/4.1.8?platform=2&gkey=000000&app_version=4.2.0.5&versioncode=20141475&market_id=floor_web&_key={_key}&phone_brand_type=OP&cat_id={cat_id}&time={time_s}"
 
        # 使用split方法按照'&'字符分割URL
        params = url.split('&')
        # 遍历分割后的字符串列表，找到cat_id和time参数
        cat_id1 = None
        time1 = None
        for param in params:
            if 'cat_id' in param:
                cat_id1 = param.split('=')[1]
            elif 'time' in param:
                time1 = param.split('=')[1]
 
        # 将cat_id和time和不变的voice_code组合成一个字符串
        sign = md5('cat_id' + cat_id1 + 'time' + time1 + 'fa1c28a5b62e79c3e63d9030b6142e4b')
        # print("30de847e271b50b342ae95fab5cdc4e4")
        # print(sign)
        data = {
            "sign": sign  # 动态sign
        }
        headers = {
            "Accept-Encoding": "identity",
            "Host": "floor.huluxia.com",
            'User-Agent': 'okhttp/3.8.1',
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "37"
        }
        response_res = requests.post(url=url, headers=headers, data=data)
        # 打印请求的url
        # print(response_res.request.url)
        # 打印请求的参数
        # print(response_res.request.body)
        # 打印请求后返回的结果
        # print(response_res.json())
        dic = response_res.json()
        # 获取签到的状态，状态：0为失败，1为成功。
        status = dic['status']
        tt = "\t"
        if status == 1:
            continueDays = dic['continueDays']  # 连续签到天数
            experienceVal = dic['experienceVal']  # 本次签到经验
            number += 1  # 每次签到成功就+1，最后记总成功次数。
            msg = f'版块ID为{cat_id}{tt}签到状态：成功{tt}获得{experienceVal}点经验/已连签{continueDays}天{tt}第{number}次签到成功！'
            # print(msg)
        else:
            msg = f'版块ID为{cat_id}{tt}签到状态：失败{tt}你的_key已失效或此版块可能已经不存在！'
        print(msg)
        time.sleep(2)  # 稍做延时，太快会异常。
    # 获取结果：累计连续签到天数及本次签到共获得多少经验点数。
    print(f"\n签到结果：此账号已连续签到{continueDays}天，此次签到共成功获{experienceVal * number}点经验！继续加油哦！")
    input("签到已完成！请按回车键结束...")
    text = f"\n签到结果：此账号已连续签到{continueDays}天，此次签到共成功获{experienceVal * number}点经验！继续加油哦！"
  
def tgBotNotify():
            global text
            url = 'https://api.telegram.org/bot' + TG_BOT_TOKEN + '/sendMessage'
            headers = {'Content-type': "application/x-www-form-urlencoded"}
            body = 'chat_id=' + TG_USER_ID + '&text=' + urllib.parse.quote(text)+ '\n\n'  + '&disable_web_page_preview=true'
            response = json.dumps(requests.post(url, data=body, headers=headers).json(), ensure_ascii=False)
            data = json.loads(response)
            if data['ok']:
                print('\nTelegram发送通知消息完成\n')
            elif data['error_code'] == 400:
                print('\n请主动给bot发送一条消息并检查接收用户ID是否正确。\n')
            elif data['error_code'] == 401:
                print('\nTelegram bot token 填写错误。\n')
            else:
                print('\nTelegram bot发送通知调用API失败！！\n')
                print(data)
# main函数
def main():
    os.system("mode con cols=75 lines=40")  # 设置打开控制台大小
    print("============================原创作者：佚名RJ==============================")
    print("============================工具使用及抓包教程============================")
    print("在葫芦侠3楼输入用户名和密码然后去打开抓包工具后再回到葫芦侠再点击登录,登录")
    print("成功后从抓包数据响应返回的用户信息中找_key字段输入到软件中即可！")
    print("==============================使用需特别注意==============================")
    print("===========手机端每次退出账号再重新登录后_key会失效发生变化哦！===========")
    # 签到
    signin()
    tgBotNotify()
 
 
# 主函数调用
if __name__ == '__main__':
    main()
