#!/usr/bin/env python3
# coding: utf-8

'''
定义管理员群的名称

在该群内的人都将被设为管理员，
管理员在被管理的群中享有高级管理权限，可进行如踢人等的操作
注：群名为部分匹配，请尽量输入全名以保证搜索到的群的唯一性
'''
admin_group_name = 'AAAUUUUXXXX'

'''
定义被管理群的群名前缀
所有以此为前缀的群都将设为被管理的群
注：前缀大小写敏感

如：设定为'Linux中国◆'，则将自动搜索到
「Linux中国◆微信机器人群」「Linux中国◆LFS群」等以其为开头的群，
并将其设为被管理的群
'''

group_prefix = '贝尔乐实验室'

# 新人入群的欢迎语
welcome_text = '''🎉 欢迎 @{} 家长的加入贝尔乐早教！
😃 贝尔乐早教电话：0757-22115439，欧老师：13129130667，朱老师：13392227928 @平姐 @蓝色雨；
😃 欢迎关注我们的公众号"贝尔乐早教"。
'''

invite_text = """感谢您的咨询，如长时间没有回复，请加入我们微群咨询"""

'''
设置群组关键词和对应群名
* 关键词必须为小写，查询时会做相应的小写处理

关于随机加群功能：
针对同类的群有多个的场景，例如群名 LFS群1、LFS群2、LFS群3...
设置关键词字典如下：
keyword_of_group = {
"lfs":"LFS群"
}
机器人会以"LFS群"为群名搜索，搜索结果为同类群名的列表，
再从列表中随机选取一个发出加群邀请。
'''

keyword_of_group = {
    "key": "keyword group"
}

'''
地区群
'''
city_group = {
    "city": "city group"
}

alert_group = "alert group"

turing_key = 'dda82262138a4556b24ff4d210e3c09b'

# 以下为功能配置选项

'''
全局静默开关
'''
silence_mode = False
