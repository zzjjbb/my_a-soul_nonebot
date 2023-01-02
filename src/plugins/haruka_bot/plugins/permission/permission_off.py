from typing import Union

from nonebot import on_command
from ...utils import GroupMessageEvent
from ...utils import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER

from ...database import DB as db
from ...utils import group_only, to_me
from ...utils.compatible import event_converter

permission_off = on_command(
    "关闭权限",
    rule=to_me(),
    permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER,
    priority=5,
)
permission_off.__doc__ = """关闭权限"""

permission_off.handle()(group_only)


@permission_off.handle()
@event_converter
async def _(event: GroupMessageEvent):
    """关闭当前群权限"""
    if await db.set_permission(event.group_id, False):
        await permission_off.finish("已关闭权限，所有人均可操作")
    await permission_off.finish("权限已经关闭了，所有人均可操作")
