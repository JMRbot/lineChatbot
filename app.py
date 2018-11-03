from flask import Flask, request, abort,render_template

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

line_bot = LineBotApi('yuCYPIH8MkXSXXN40IjevZHk2ib+axg5hbsDQ5F0hefQo86EE3sjci1J8fM8BjwUwtSC9rPi5nNP4AmduZAbY8pAWGVrY2Lmh/nDAbEkWdulw6txnanvLL0U3gEQ6dxc+7CLPMFQ26UPPUynmnurYQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('962ec561c6812dacfb9c4e916de5f428')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if userText != "":
        from ai import Chatbot
        chat = Chatbot(userText)
    return str(chat)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    tokenID = "{}".format(event.reply_token)
    content = "{}".format(event.message.text)
    print("line_message : ",content)
    if content != "":
        from ai import Chatbot
        chat = Chatbot(content)
##        print("hi",chat)
        line_bot.reply_message(
            tokenID,
            TextSendMessage(text=chat)
            )
            
import os
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8000)
