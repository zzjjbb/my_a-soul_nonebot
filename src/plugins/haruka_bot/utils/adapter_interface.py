from typing import Union
from nonebot.adapters.mirai2 import Bot
from nonebot.adapters.mirai2.message import MessageChain as Message
from .compatible import MessageSegment
from nonebot.adapters.mirai2 import MessageEvent, GroupMessage as GroupMessageEvent, FriendMessage as _fm, TempMessage as _tm
from nonebot.adapters.mirai2.event import NewFriendRequestEvent
from nonebot.adapters.mirai2.exception import ActionFailed, NetworkError
from nonebot.adapters.mirai2 import GROUP_ADMIN, GROUP_OWNER
PrivateMessageEvent = Union[_fm, _tm]
