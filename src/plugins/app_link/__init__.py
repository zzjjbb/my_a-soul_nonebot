# import nonebot
from nonebot import get_driver

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

from nonebot.plugin import on_keyword, on_command, on_message, on_notice
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.mirai2 import Bot, MessageEvent
from nonebot.adapters.mirai2.event import FriendRecallEvent
import json

import requests
import random
import time

reply_history = {}

def record_reply(event_dict, reply_result):
    print("record event", event_dict)
    print(' '+str(reply_result['messageId']))
    reply_history[event_dict['source']['id']] = [time.time(), reply_result['messageId']]
    for key, (t, _) in list(reply_history.items()):
        if time.time() - t > 1800:
            del reply_history[key]
        else:
            break
    print("current history", reply_history)


def to_short(link):
    url = 'https://api.bilibili.com/x/share/click'
    link = str(link)
    #请求参数
    build=str(random.randint(9300,10000))
    data = {'build':build,'buvid':'qp92wvbiiwercf5au381g1bzajou85hg','oid':link,'platform':'ios','share_channel':'COPY','share_id':'public.webview.0.0.pv','share_mode':'3'}
    r = requests.post(url,data)
    reapi = json.loads(r.content)
    datalink = reapi.get('data')
    print(datalink)
    return datalink


message_test = on_keyword({'阿梓'}, rule=to_me(), priority=1)


@message_test.handle()
async def _message(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    await bot.send(event, " 啥b", at_sender=True)


command_to_short = on_command('转',priority=1)


@command_to_short.handle()
async def _echo_command_to_short(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    print(text)
    location=text.find("https://www.bilibili.com/")
    if location!=-1:
        await bot.send(event, " "+to_short(text[location:])['content'], at_sender=True)

# command_help=on_command('help',priority=1, rule=to_me())
command_help=on_command('help', priority=1)

@command_help.handle()
async def _echo_command_help(bot: Bot, event: MessageEvent):
    helpstr= '''
help:
1. bilibili小程序转url
2. "/转 https://www.bilibili.com/*" : 生成 https://b23.tv/*
    '''
    reply_result = await bot.send(event, helpstr, at_sender=True)
    record_reply(event.normalize_dict(), reply_result)

def format_short(url:str):
    if '//mp.weixin.qq.com/' in url:
        return url.split('&chksm')[0]
    if 'music.163.com/' in url:
        return url.split('&uct')[0]
    return url.split('?')[0]


message_1=on_message(priority=2, block=False)

@message_1.handle()
async def _message_1(bot:Bot, event:MessageEvent, matcher:Matcher):
    textdict = event.get_message().export()[0]
    # print(textdict)
    # print(type(textdict))
    if textdict['type']=='App':
        contentstr=textdict['content']
        # print(type(contentstr))
        content=json.loads(contentstr)
        if content.get('desc')=="新闻":
            url=content['meta']['news']['jumpUrl']
        else:
            url=content["meta"]['detail_1'].get('qqdocurl')
        if url is None:
            print('no url!')
            return

        surl=format_short(url)
        print(surl)
        reply_result = await bot.send(event, surl, at_sender=False)
        record_reply(event.normalize_dict(), reply_result)
        matcher.stop_propagation()


recall_notice=on_notice()

@recall_notice.handle()
async def _recall_reply(bot:Bot, event):
    if isinstance(event, FriendRecallEvent):
        print("recall find")
        src_id = event.normalize_dict()['message_id']
        reply_id = reply_history.get(src_id)  # is a list [time, m_id]
        if reply_id is None:
            print("recalled message has no reply record")
        else:
            # reply_id = reply_id[1]
            # print(str(src_id) + '--' + str(reply_id))
            await bot.recall(target=reply_id[1])

