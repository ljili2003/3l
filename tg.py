import requests
import time
import hmac
import hashlib
import base64
import json
import os
import urllib.parse

# telegram
    if os.environ.get('TG_BOT_TOKEN'):
        TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
    if os.environ.get('TG_USER_ID'):
        TG_USER_ID = os.environ['TG_USER_ID']
def tgBotNotify(self, text, desp):
        if sendNotify.TG_BOT_TOKEN != '' or sendNotify.TG_USER_ID != '':

            url = 'https://api.telegram.org/bot' + sendNotify.TG_BOT_TOKEN + '/sendMessage'
            headers = {'Content-type': "application/x-www-form-urlencoded"}
            body = 'chat_id=' + sendNotify.TG_USER_ID + '&text=' + urllib.parse.quote(
                text) + '\n\n' + urllib.parse.quote(desp) + '&disable_web_page_preview=true'
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
        else:
            print('\n您未提供Bark的APP推送BARK_PUSH，取消Bark推送消息通知\n')
            pass
