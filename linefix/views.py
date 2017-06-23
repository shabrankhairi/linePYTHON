import hmac
import hashlib
import base64
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from linebot import LineBotApi
from linebot.models import (TextSendMessage, ImageSendMessage, CarouselTemplate, CarouselColumn, TemplateSendMessage, MessageTemplateAction)
from linebot.exceptions import LineBotApiError

from app_properties import channel_secret, channel_access_token

# Create your views here.
@api_view(['POST'])
def callback(request):
    # Get request header and request body
    aXLineSignature = request.META.get('HTTP_X_LINE_SIGNATURE')
    print('Signature: ' + aXLineSignature)
    body = request.body
    print('Payload: ' + body)
    
    # Validate signature
    hash = hmac.new(channel_secret.encode('utf-8'),body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    
    # Exit when signature not valid
    if aXLineSignature != signature:
        return Response("X-Line-Signature is not valid")
    
    aPayload = json.loads(body)
    mEventType = aPayload['events'][0]['type']
    print('Event type: ' + mEventType)
    mSource = aPayload['events'][0]['source']['type']
    mReplyToken = aPayload['events'][0]['replyToken']

    if mEventType == 'join':
        if mSource == 'user':
            replyToUser(mReplyToken, 'Hello User')
        elif mSource == 'group':
            replyToUser(mReplyToken, 'Hello User')
        elif mSource == 'room':
            replyToUser(mReplyToken, 'Hello User')
        return Response("Event is join")

    if mEventType == 'message':
        if mSource == 'user':
            mTargetId = aPayload['events'][0]['source']['userId']
        elif mSource == 'group':
            mTargetId = aPayload['events'][0]['source']['groupId']
        elif mSource == 'room':
            mTargetId = aPayload['events'][0]['source']['roomId']

    mType = aPayload['events'][0]['message']['type']

    if mType != 'text':
        replyToUser(mReplyToken, 'Unknown message type')
        return Response("Message Type is not text")

    mText = aPayload['events'][0]['message']['text'].lower()

    if 'bot leave' in mText:
        botLeave(mTargetId, mSource)
        return Response("User want to exit")

    getMovieData(mText, mReplyToken, mTargetId)

    return Response ("Movies_Bot")

def replyToUser(reply_token, text_message):
    line_bot_api = LineBotApi(channel_access_token)
    try:
        line_bot_api.reply_message(reply_token, TextSendMessage(text=text_message))
    except LineBotApiError as e:
        print('Exception is raised')

def pushImage(target_id, poster_url):
    line_bot_api = LineBotApi(channel_access_token)
    print('Poster URL: ' + poster_url)
    try:
        line_bot_api.push_message(target_id, ImageSendMessage(original_content_url=poster_url,
                                                              preview_image_url=poster_url))
    except LineBotApiError as e:
        print('Exception is raised')

                              
    template_message = TemplateSendMessage(alt_text='Your search result', template=carousel_template)
    line_bot_api = LineBotApi(channel_access_token)
    try:
        line_bot_api.push_message(target_id, template_message)
    except LineBotApiError as e:
        print('Exception is raised')

def botLeave(target_id, source_type):
    line_bot_api = LineBotApi(channel_access_token)
    try:
        if source_type == 'room':
            line_bot_api.leave_room(target_id)
        elif source_type == 'group':
            line_bot_api.leave_group(target_id)
    except LineBotApiError as e:
        print('Exception is raised')


for event in events:
            if isinstance(event, MessageEvent):
                text = event.message.text
                if text == 'confirm':
                    confirm_template = ConfirmTemplate(text='Do it?', actions=[
                        MessageTemplateAction(label='Yes', text='Yes!'),
                        MessageTemplateAction(label='No', text='No!'),
                    ])
                    template_message = TemplateSendMessage(
                       alt_text='Confirm alt text', template=confirm_template)
                    line_bot_api.reply_message(
                       event.reply_token,
                       template_message
                    )
                elif text == 'buttons':
                    buttons_template = ButtonsTemplate(
                        title='My buttons sample', text='Hello, my buttons', actions=[
                            URITemplateAction(
                                label='Go to line.me', uri='https://line.me'),
                            PostbackTemplateAction(label='ping', data='ping'),
                            PostbackTemplateAction(
                                label='ping with text', data='ping',
                                text='ping'),
                            MessageTemplateAction(label='Translate Rice', text='米')
                        ])
                    template_message = TemplateSendMessage(
                        alt_text='Buttons alt text', template=buttons_template)
                    line_bot_api.reply_message(event.reply_token, template_message)
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                       TextSendMessage(text=event.message.text)
                    )

return HttpResponse()



