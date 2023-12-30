import json
from pprint import pprint

import requests
from flask import Flask, request
from linebot.v3.webhook import WebhookHandler

from setting import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET

handler = WebhookHandler(CHANNEL_SECRET)
headers = {'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'}
reply_message_api = 'https://api.line.me/v2/bot/message/reply'

app = Flask(__name__)


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    data = request.get_data(as_text=True)
    handler.handle(data, signature)

    json_data = json.loads(data)
    pprint(json_data)

    reply_token = json_data['events'][0]['replyToken']
    user_message = json_data['events'][0]['message']

    if user_message.get('text') == '圖片地圖':
        image_width = 1040
        image_height = 300

        body = {
            'replyToken': reply_token,
            'messages': [
                {
                    'type': 'text',
                    'text': '歡迎使用圖片地圖'
                },
                {
                    'type': 'imagemap',
                    'baseUrl': 'https://i.imgur.com/Yz2yzve.jpg',
                    'altText': '這是圖片地圖',
                    'baseSize': {'width': image_width, 'height': image_height},
                    'actions': [
                        {
                            'type': 'message',
                            'text': '你點選了紅色區塊！',
                            'area': {
                                'x': 0,
                                'y': 0,
                                'width': image_width * 0.25,
                                'height': image_height
                            }
                        },
                        {
                            'type': 'message',
                            'text': '你點選了黃色區塊！',
                            'area': {
                                'x': image_width * 0.25,
                                'y': 0,
                                'width': image_width * 0.25,
                                'height': image_height
                            }
                        },
                        {
                            'type': 'message',
                            'text': '你點選了綠色區塊！',
                            'area': {
                                'x': image_width * 0.5,
                                'y': 0,
                                'width': image_width * 0.25,
                                'height': image_height
                            }
                        },
                        {
                            'type': 'message',
                            'text': '你點選了藍色區塊！',
                            'area': {
                                'x': image_width * 0.75,
                                'y': 0,
                                'width': image_width * 0.25,
                                'height': image_height
                            }
                        }
                    ]
                }
            ]
        }

        requests.post(reply_message_api, json=body, headers=headers)

    return 'OK'


if __name__ == '__main__':
    app.run()

# 圖片地圖訊息最多可以包含 50 個可點選的區塊。
