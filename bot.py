#!/usr/bin/env python3
# coding: utf-8

from wxpy import *
import re

import trigger

isSend   = 0
nextSend = None;

'''
使用 cache 来缓存登陆信息，同时使用控制台登陆
'''
bot = Bot('bot.pkl', console_qr=True)


'''
开启 PUID 用于后续的控制
'''
bot.enable_puid('wxpy_puid.pkl')


'''
邀请信息处理
'''
rp_new_member_name = (
    re.compile(r'^"(.+)"通过'),
    re.compile(r'邀请"(.+)"加入'),
)

'''
为保证兼容，在下方admins中使用标准用法
在 admin_puids 中确保将机器人的puid 加入
机器人的puid 可以通过 bot.self.puid 获得
其他用户的PUID 可以通过 执行 export_puid.py 生成 data 文件，在data 文件中获取
'''
admin_puids = (
    'cc7ee5e3',
	'7fb8f362',
)

'''
定义需要管理的群
群的PUID 可以通过 执行 export_puid.py 生成 data 文件，在data 文件中获取
'''
group_puids = (
    '9595f885',
)

# 格式化 Group
groups = list(map(lambda x: bot.groups().search(puid=x)[0], group_puids))
# 格式化 Admin
admins = list(map(lambda x: bot.friends().search(puid=x)[0], admin_puids))

# 新人入群的欢迎语
welcome_text = '''🎉 欢迎 @{} 的加入！
😃 请关注我们的公众号“贝尔乐早教”，贝尔乐电话：0757-22115439，欧老师：13129130667，朱老师：13392227928 @平姐 @蓝色雨。
'''

invite_text  = """感谢您的咨询，如长时间没有回复，请加入我们微群咨询【此消息发自贝尔乐机器人】"""

weather_text = """"""

monday_text   = """"""

tueday_text   = """"""

thursday_text = """"""

'''
设置群组关键词和对应群名
* 关键词必须为小写，查询时会做相应的小写处理
'''
keyword_of_group = {
    "bel":"贝尔乐早教-2017年",
}

# 远程踢人命令: 移出 @<需要被移出的人>
rp_kick = re.compile(r'^(?:移出|移除|踢出|拉黑)\s*@(.+?)(?:\u2005?\s*$)')

'''
地区群
'''
city_group = {
    "佛山":"贝尔乐早教-2017年",
}

female_group=""

# 下方为函数定义

'''
条件邀请
'''
def condition_invite(user):
    if user.sex == 2:
        female_groups = bot.groups().search(female_group)[0]
        try:
            female_groups.add_members(user, use_invitation=True)
            pass
        except:
            pass
    if (user.province in city_group.keys() or user.city in city_group.keys()):
        try:
            target_city_group = bot.groups().search(city_group[user.province])[0]
            pass
        except:
            target_city_group = bot.groups().search(city_group[user.city])[0]
            pass
        try:
            if user not in target_city_group:
                target_city_group.add_members(user, use_invitation=True)
        except:
            pass

'''
判断消息发送者是否在管理员列表
'''
def from_admin(msg):
    """
    判断 msg 中的发送用户是否为管理员
    :param msg: 
    :return: 
    """
    if not isinstance(msg, Message):
        raise TypeError('expected Message, got {}'.format(type(msg)))
    from_user = msg.member if isinstance(msg.chat, Group) else msg.sender
    print(admins)
    return from_user in admins

'''
远程踢人命令
'''
def remote_kick(msg):
    if msg.type is TEXT:
        match = rp_kick.search(msg.text)
        if match:
            name_to_kick = match.group(1)

            if not from_admin(msg):
                return '感觉有点不对劲… @{}'.format(msg.member.name)

            member_to_kick = ensure_one(list(filter(
                lambda x: x.name == name_to_kick, msg.chat)))
            if member_to_kick  == bot.self:
                return '无法移出 @{}'.format(member_to_kick.name)
            if member_to_kick in admins:
                return '无法移出 @{}'.format(member_to_kick.name)

            member_to_kick.remove()
            return '成功移出 @{}'.format(member_to_kick.name)


'''
邀请消息处理
'''
def get_new_member_name(msg):
    # itchat 1.2.32 版本未格式化群中的 Note 消息
    from itchat.utils import msg_formatter
    msg_formatter(msg.raw, 'Text')

    for rp in rp_new_member_name:
        match = rp.search(msg.text)
        if match:
            return match.group(1)


my_group = "贝尔乐早教-2017年"

'''
定义邀请用户的方法。
按关键字搜索相应的群，如果存在相应的群，就向用户发起邀请。
'''
def invite(user, keyword):
	print(keyword)
	print(keyword_of_group[keyword])
	group = bot.groups().search(keyword_of_group[keyword])
	print(group)
	print(len(group))
	if len(group) > 0:
		target_group = ensure_one(group)
		if user in target_group:
			content = "您已经加入了 {} [微笑]".format(target_group.nick_name)
			user.send(content)
		else:
			try:
				target_group.add_members(user, use_invitation=True)
			except:
				user.send("邀请错误！机器人邀请好友进群已达当日限制。请您明日再试")
	else:
		user.send("该群状态有误，您换个关键词试试？")


def invite_always(user):
	print(user)
	group = bot.groups().search(my_group)
	target_group = ensure_one(group)

	if user in target_group:
		content = "您已经加入了 {} [微笑]".format(target_group.nick_name)
		user.send(content)
	else:
		try:
			target_group.add_members(user, use_invitation=True)
		except:
			user.send("邀请错误！机器人邀请好友进群已达当日限制。请您明日再试")

# 下方为消息处理

'''
处理加好友请求信息。
如果验证信息文本是字典的键值之一，则尝试拉群。
'''
@bot.register(msg_types=FRIENDS)
def new_friends(msg):
    user = msg.card.accept()
    if msg.text.lower() in keyword_of_group.keys():
        invite(user, msg.text.lower())
    else:
    	invite_always(user)
        #return invite_text

@bot.register(Friend, msg_types=TEXT)
def exist_friends(msg):
    if msg.text.lower() in keyword_of_group.keys():
        invite(msg.sender, msg.text.lower())
    else:
        invite_always(msg.sender)
        return invite_text

# 管理群内的消息处理
@bot.register(groups, except_self=False)
def wxpy_group(msg):
    ret_msg = remote_kick(msg)
    if ret_msg:
        return ret_msg
    elif msg.is_at:
        pass


@bot.register(groups, NOTE)
def welcome(msg):
    name = get_new_member_name(msg)
    if name:
        return welcome_text.format(name)


trigger.trigger(isSend, nextSend)

embed()
