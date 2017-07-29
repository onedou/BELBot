#!/usr/bin/env python3
# coding: utf-8

from wxpy import *
from config import *
from wxpy.utils import start_new_thread

import re
import time
import os
import platform
import trigger

isSend   = 0
nextSend = None

'''
使用 cache 来缓存登陆信息，同时使用控制台登陆
'''
console_qr = (False if platform.system() == 'Windows' else True)
bot        = Bot('bot.pkl', console_qr=console_qr)

bot.messages.max_history = 0

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
    re.compile(r'invited "(.+)" to the group chat'),
)

'''
管理员群及被管理群初始化
'''
admin_puids = (
    'cc7ee5e3',
	'7fb8f362',
)

def fresh_groups():
    global groups, admin_group
    # 格式化被管理群 Groups
    try:
        groups = list(filter(lambda x: x.name.startswith(group_prefix), bot.groups(update = True).search(group_prefix)))
    except:
        print("查找被管理群出错！请检查被管理群前缀（group_prefix）是否配置正确")
        quit()

'''
定义需要管理的群
群的PUID 可以通过 执行 export_puid.py 生成 data 文件，在data 文件中获取
'''
group_puids = (
    '9595f885',
)
    # 格式化管理员群 Admin_group
    try:
        admin_group = ensure_one(bot.groups(update = True).search(admin_group_name))
    except:
        print("查找管理员群出错！请检查管理群群名（admin_group_name）是否配置正确")
        print("现将默认设置为只有本帐号为管理员")
        admin_group = None
# 格式化 Group
groups = list(map(lambda x: bot.groups().search(puid=x)[0], group_puids))
# 格式化 Admin
admins = list(map(lambda x: bot.friends().search(puid=x)[0], admin_puids))
fresh_groups()

# 新人入群的欢迎语
welcome_text = '''🎉 欢迎 @{} 的加入！
😃 请关注我们的公众号“贝尔乐早教”，贝尔乐电话：0757-22115439，欧老师：13129130667，朱老师：13392227928 @平姐 @蓝色雨。
'''
# 远程踢人命令: 移出 @<需要被移出的人>
rp_kick = re.compile(r'^(?:移出|移除|踢出|拉黑)\s*@(.+?)(?:\u2005?\s*$)')
invite_text  = """感谢您的咨询，如长时间没有回复，请加入我们微群咨询【此消息发自贝尔乐机器人】"""

weather_text = """"""

monday_text   = """"""

tueday_text   = """"""

thursday_text = """"""

# 下方为函数定义

def get_time():
    return str(time.strftime("%Y-%m-%d %H:%M:%S"))
'''
机器人消息提醒设置
'''
keyword_of_group = {
    "bel":"贝尔乐早教-2017年",
}

alert_level = 30 # DEBUG: 10, INFO: 20, WARNING: 30, ERROR: 40, FATAL: 50
if alert_group:
    try:
        alert_receiver = ensure_one(bot.groups().search(alert_group))
    except:
        print("警报群设置有误，请检查群名是否存在且唯一")
        alert_receiver = bot.file_helper
else:
    alert_receiver = bot.file_helper
logger = get_wechat_logger(alert_receiver, str(alert_level))
logger.error(str("机器人登陆成功！"+ get_time()))


'''
重启机器人
'''
def _restart():
    os.execv(sys.executable, [sys.executable] + sys.argv)

'''
地区群

'''
city_group = {
    "佛山":"贝尔乐早教-2017年",
}

'''
状态汇报
'''
def status():
    status_text = get_time() + " 机器人目前在线,共有好友 【" + str(len(bot.friends())) + "】 群 【 " + str(len(bot.groups())) + "】"
    return status_text

female_group=""

'''
定时报告进程状态
'''
def heartbeat():
    while bot.alive:
        time.sleep(3600)
        # noinspection PyBroadException
        try:
            logger.error(status())
        except ResponseError as e:
            if 1100 <= e.err_code <= 1102:
                logger.critical('LCBot offline: {}'.format(e))
                _restart()

# 下方为函数定义
start_new_thread(heartbeat)

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
    return from_user in admin_group.members if admin_group else from_user == bot.self

'''
远程踢人命令
'''
def remote_kick(msg):
    if msg.type is TEXT:
        match = rp_kick.search(msg.text)
        if match:
            name_to_kick = match.group(1)

            if not from_admin(msg):
                if not silence_mode:
                    return '感觉有点不对劲… @{}'.format(msg.member.name)
                else:
                    return

            member_to_kick = ensure_one(list(filter(
                lambda x: x.name == name_to_kick, msg.sender.members)))
            if member_to_kick  == bot.self:
                return '无法移出 @{}'.format(member_to_kick.name)
            if member_to_kick in admin_group.members:
                return '无法移出 @{}'.format(member_to_kick.name)

            logger.error(get_time() + str(" 【"+member_to_kick.name + "】 被 【"+msg.member.name+"】 移出 【" + msg.sender.name+"】"))
            try:
                member_to_kick.set_remark_name("[黑名单]-"+get_time())
            except:
                logger.error(get_time() + str("为 【" + member_to_kick.name + "】 设置黑名单时出错"))

            if member_to_kick in msg.sender:
                msg.sender.remove_members(member_to_kick)
                kick_info = '成功移出 @{}'.format(member_to_kick.name)
            else:
                kick_info = '@{} 已不在群中'.format(member_to_kick.name)

            for ready_to_kick_group in  groups:
                if member_to_kick in ready_to_kick_group:
                    ready_to_kick_group.remove_members(member_to_kick)
                    ready_to_kick_group.send(str("【" + member_to_kick.name + "】 因其在 【" + msg.sender.name + "】 的行为被系统自动移出"))
                    logger.error(get_time()+ str("【"+member_to_kick.name + "】 被系统自动移出 " +  ready_to_kick_group.name))

            return kick_info


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
    from random import randrange
    group = bot.groups().search(keyword_of_group[keyword])
	print(keyword)
	print(keyword_of_group[keyword])
    if len(group) > 0:
        for i in range(0, len(group)):
            if user in group[i]:
                content = "您已经加入了 {} [微笑]".format(group[i].nick_name)
                user.send(content)
                return
        if len(group) == 1:
            target_group = group[0]
        else:
            index = randrange(len(group))
            target_group = group[index]
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
		user.send(invite_text)
@bot.register(Friend, msg_types=TEXT)
def exist_friends(msg):
    if msg.sender.name.find("黑名单") != -1:
        return "您已被拉黑！"
    else:
        if msg.text.lower() in keyword_of_group.keys():
            invite(msg.sender, msg.text.lower())
			invite_always(msg.sender)
        else:
            return invite_text

# 管理群内的消息处理
@bot.register(groups, except_self=False)
def wxpy_group(msg):
    ret_msg = remote_kick(msg)
    if ret_msg:
        return ret_msg
    elif msg.is_at and not silence_mode:
        if turing_key :
            tuling = Tuling(api_key=turing_key)
            tuling.do_reply(msg)
        else:
            return "忙着呢，别烦我！";
            pass


@bot.register(groups, NOTE)
def welcome(msg):
    name = get_new_member_name(msg)
    if name and not silence_mode:
        return welcome_text.format(name)

@bot.register(alert_receiver, except_self=False)
def alert_command(msg):
    if from_admin(msg):
        if msg.text == "状态":
            return status()
        elif msg.text == "重启":
            _restart()
        elif msg.text == "刷新":
            fresh_groups()
            return "群信息已更新，现有被管理群 【{}】，管理员 【{}】".format(len(groups), len(admin_group) if admin_group else 1)

trigger.trigger(isSend, nextSend)

embed()
