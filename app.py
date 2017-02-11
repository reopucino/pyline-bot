from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('zLTEtx+FKJt7lzOx+5JY3uKj+hcu8O3Hu9WAv3QcEaiBU7zGfRIWZK/IHyKCvyQz3vdACiLOKLlv71XvmYUYTLsmk/oxJ1dnyNf0bXt2xb1DKWwm3wp33X9IIta8W4Scxo8seUUtR+tGqElBNH7IPAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('08ac2ea43bf7e73eea455132f8f68fb0')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
