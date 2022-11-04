import base64
from typing import Union, Optional, Literal
from nonebot.adapters import mirai2
from functools import wraps


class MessageEvent:
    message_type: Literal['private', 'group']
    self_id: int
    group_id: Optional[int]
    user_id: Optional[int]
    sub_type: str

    def __init__(self, event: mirai2.MessageEvent):
        self.self_id = event.self_id
        self._mirai_event = event


class GroupMessageEvent(MessageEvent):
    __slots__ = ('self_id', 'group_id')
    message_type = 'group'

    def __init__(self, event: mirai2.GroupMessage):
        super().__init__(event)
        self.group_id = event.sender.group.id


class PrivateMessageEvent(MessageEvent):
    __slots__ = ('self_id', 'user_id', 'sub_type')
    message_type = 'private'

    def __init__(self, event: Union[mirai2.FriendMessage, mirai2.TempMessage]):
        super().__init__(event)
        self.user_id = event.sender.id
        if isinstance(event, mirai2.FriendMessage):
            self.sub_type = 'friend'
        elif isinstance(event, mirai2.TempMessage):
            self.sub_type = 'group'


class MessageSegment:
    @staticmethod
    def image(src: Union[str, bytes]):
        """only process the base64 (dynamic) or url (live) cases used in this project"""
        if isinstance(src, bytes):
            return mirai2.MessageSegment.image(base64=base64.b64encode(src).decode('ascii'))
        if src[:9] == "base64://":
            return mirai2.MessageSegment.image(base64=src[9:])
        elif src[:4] == "http":
            return mirai2.MessageSegment.image(url=src)
        else:
            print(str(src))
            return mirai2.MessageSegment.plain("[unsupported image]")

    @staticmethod
    def at(user_id: Union[int, str]):
        if user_id == 'all':
            return mirai2.MessageSegment.at_all()
        else:
            return mirai2.MessageSegment.at(int(user_id))


def event_converter(func):
    @wraps(func)
    async def func_compat(**kwargs):
        event = kwargs['event']
        if isinstance(event, mirai2.GroupMessage):
            event = GroupMessageEvent(event)
        elif isinstance(event, (mirai2.FriendMessage, mirai2.TempMessage)):
            event = PrivateMessageEvent(event)
        kwargs['event'] = event
        await func(**kwargs)

    return func_compat
