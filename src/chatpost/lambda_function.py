import os
import json
import logging
import requests
import urllib.parse
from datetime import datetime

# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Google Chat Webhook URL
WEBHOOK_URL = os.environ['GOOGLE_CHAT_WEBHOOK_URL']
CARD_IMAGE_URL = os.environ['CARD_IMAGE_URL']

# HTTP Header
message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

# Cards Widgets detail Label
keyLabel = {
    'stateMachineArn': 'StateMachine',
    'name': 'ExecutionName',
    'status': 'Status',
}

# Message template
message = {'text': '<users/all>', 'cards': [{'header':{},'sections': [{'widgets': []}]}]}

def lambda_handler(event, context):
    """
    Google Chat Webhook にエラーイベント情報を送信する

    Parameters
    ----------
    event : json
        トリガーイベント情報
    context : json
        実行環境情報
    
    Returns
    ----------
    response : json
        POSTリクエスト実行結果
    """
    try:
        logger.info("Set Cards Info")
        message['cards'][0]['header']['title'] = 'ERROR : Step Functions'
        message['cards'][0]['header']['imageUrl'] = CARD_IMAGE_URL

        logger.info("Setting Cards Widgets from event")
        for key, val in keyLabel.items():
            if str(key) == 'stateMachineArn':
                contents = str(event['detail'][key]).split(':')[-1]
            else:
                contents = event['detail'][key]

            append_widgets(message, val, contents)

        logger.info("Load input")
        input_str =  urllib.parse.unquote_plus(event['detail']['input'])
        input = json.loads(input_str, encoding='utf-8')

        if 'Records' in input.keys():
            logger.info("Set Cards Widgets from input: S3")

            bucket_name = input['Records'][0]['s3']['bucket']['name']
            key = input['Records'][0]['s3']['object']['key']
            file_name = key.split('/')[-1]
            key_prefix = key.replace(file_name, '')
            event_name = input['Records'][0]['eventName']
            
            append_widgets(message, 'S3 BucketName', bucket_name)
            append_widgets(message, 'KeyPrefix', key_prefix)
            append_widgets(message, 'FileName', file_name)
            append_widgets(message, 'EventName', event_name)

        # https://github.com/tosh223/aws-glue-crawlflow
        elif 'CrawlerName' in input.keys():
            logger.info("Set Cards Widgets from input: Glue Crawler")
            append_widgets(message, 'CrawlerName', input['CrawlerName'])

        logger.info("Send Message to Google Chat Webhook")
        response = requests.post(
            WEBHOOK_URL,
            headers=message_headers,
            data=json.dumps(message)
        )

        return json.loads(response.text)

    except Exception as e:
        logger.exception(e, exc_info=False)
        raise e

def append_widgets(message, top_label, content):
    """
    メッセージにウィジェットを追加する

    Parameters
    ----------
    message : json
        メッセージ
    top_label : string
        ラベル
    content : string
        ウィジェット内に表示する文字列
    """
    keyVal = {'keyValue': {}}
    keyVal['keyValue']['topLabel'] = top_label
    keyVal['keyValue']['content'] = content
    keyVal['keyValue']['contentMultiline'] = 'true'

    message['cards'][0]['sections'][0]['widgets'].append(keyVal)