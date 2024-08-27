import sys
import os
import datetime
import time
from dotenv import load_dotenv
load_dotenv()

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    TextMessage,
    PushMessageRequest,
    TemplateMessage,
    Template,
    MessageAction,
    ConfirmTemplate
)
from linebot.v3.webhook import WebhookParser

# Environment variables, you should setup in your .env file
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
group_id = os.getenv('LINE_GROUP_ID', None)
personal_id = os.getenv('LINE_PERSONAL_ID', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
    
parser = WebhookParser(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)
def pushMsg(msg):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        msg = [TemplateMessage(
            type="template",
            alt_text=msg,
            template=ConfirmTemplate(
                type="confirm",
                text=msg,
                actions=[MessageAction(label="吃", text="吃"), MessageAction(label="不吃", text="不吃")]
            )
        )]
        line_bot_api.push_message(
            PushMessageRequest(
                to=group_id,
                messages=msg
            )
        )
def setTimer():
    lunch_notify_time = datetime.time(11, 00, 0)
    dinner_notify_time = datetime.time(17, 30, 0)
    while True:
        now = datetime.datetime.now()
        if now >= datetime.datetime.combine(now.date(), dinner_notify_time):
            alarm_time = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), lunch_notify_time)
            msg = "要吃午餐嗎(11:30)"
        elif now < datetime. datetime.combine(now.date(), lunch_notify_time):
            alarm_time = datetime.datetime.combine(now.date(), lunch_notify_time)
            msg = "要吃午餐嗎(11:30)"
        else:
            alarm_time = datetime.datetime.combine(now.date(), dinner_notify_time)
            msg = "要吃晚餐嗎(18:00)"
        time.sleep((alarm_time - now).total_seconds())
        pushMsg(msg)
    
def initCheck():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            PushMessageRequest(
                to=personal_id,
                messages=[TextMessage(text="Container start...")]
            )
        )

if __name__ == "__main__":
    initCheck()
    setTimer()