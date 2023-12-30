import json
from pprint import pprint

from flask import Flask, request
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest,
    TextMessage, ImagemapMessage, ImagemapBaseSize, MessageImagemapAction, ImagemapArea
)

from setting import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET

handler = WebhookHandler(CHANNEL_SECRET)
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

app = Flask(__name__)


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    handler.handle(body, signature)

    json_data = json.loads(body)
    pprint(json_data)

    reply_token = json_data['events'][0]['replyToken']
    user_message = json_data['events'][0]['message']

    if user_message.get('text') == '圖片地圖':
        image_width = 1040
        image_height = 300

        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[
                        TextMessage(
                            text='歡迎使用圖片地圖'
                        ),
                        ImagemapMessage(
                            base_url='https://i.imgur.com/Yz2yzve.jpg',
                            alt_text='這是圖片地圖',
                            base_size=ImagemapBaseSize(width=image_width, height=image_height),
                            actions=[
                                MessageImagemapAction(
                                    text='你點選了紅色區塊！',
                                    area=ImagemapArea(
                                        x=0,
                                        y=0,
                                        width=int(image_width * 0.25),
                                        height=image_height
                                    )
                                ),
                                MessageImagemapAction(
                                    text='你點選了黃色區塊！',
                                    area=ImagemapArea(
                                        x=int(image_width * 0.25),
                                        y=0,
                                        width=int(image_width * 0.25),
                                        height=image_height
                                    )
                                ),
                                MessageImagemapAction(
                                    text='你點選了綠色區塊！',
                                    area=ImagemapArea(
                                        x=int(image_width * 0.5),
                                        y=0,
                                        width=int(image_width * 0.25),
                                        height=image_height
                                    )
                                ),
                                MessageImagemapAction(
                                    text='你點選了藍色區塊！',
                                    area=ImagemapArea(
                                        x=int(image_width * 0.75),
                                        y=0,
                                        width=int(image_width * 0.25),
                                        height=image_height
                                    )
                                )
                            ]
                        )
                    ]
                )
            )

    return 'OK'


if __name__ == '__main__':
    app.run()
