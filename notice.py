from wxpy import *

import request
import json
import time
import config

bot = Bot('bot.pkl', console_qr=True)


def weather():
    url = "http://api.yytianqi.com/forecast7d?city=CH280800&key=esmiwq4we3k018ia"
    jsonData = request.request(url)
    jsonData = json.loads(jsonData)
    # print(jsonData)

    city = jsonData['data']['cityName']
    weatherinfo = jsonData['data']['list'][0]

    text = "温馨提示：今天（" + weatherinfo['date'] + "）" + city + \
           "白天：" + weatherinfo['tq1'] + "，气温" + weatherinfo['qw1'] + "度，" + weatherinfo['fl1'] + weatherinfo['fx1'] + ";" +\
           "晚间：" + weatherinfo['tq2'] + "，气温" + weatherinfo['qw2'] + \
           "度，" + weatherinfo['fl2'] + weatherinfo['fx2'] + ";"

    if bot.groups().search(config.group_prefix)[0]:
        bot.groups().search(config.group_prefix)[0].send(text)
    pass


def classNotice(*params):
    sequence = params
    now = int(time.time())
    nowArray = time.localtime(now)
    week = nowArray.tm_wday

    if(sequence == 'tomorrow'):
        if week == 6:
            week = 0
            pass
        else:
            week = week + 1
            pass

    if week == 0:
        weekStr = 'monday'
        weekDesc = '周一'
        pass
    elif week == 1:
        weekStr = 'tuesday'
        weekDesc = '周二'
        pass
    elif week == 2:
        weekStr = 'wednesday'
        weekDesc = '周三'
        pass
    elif week == 3:
        weekStr = 'thursday'
        weekDesc = '周四'
        pass
    elif week == 4:
        weekStr = 'friday'
        weekDesc = '周五'
        pass
    elif week == 5:
        weekStr = 'saturday'
        weekDesc = '周六'
        pass
    elif week == 6:
        weekStr = 'sunday'
        weekDesc = '周日'
        pass

    classNotice = getSetting('class_notice.json')

    if(sequence == 'today'):
        message = "今天（" + weekDesc + "）" + classNotice[weekStr]
        pass
    elif(sequence == 'tomorrow'):
        message = "明天（" + weekDesc + "）" + classNotice[weekStr]
        pass

    message = "温馨提示：" + message + "，请孩子们准时来上课。"

    if week == 6:
        return

    if bot.groups().search('test group')[0] and message:
        bot.groups().search('test group')[0].send(message)
    pass


def getSetting(path):
    setting = open(path, 'r')
    content = setting.read()
    setting.close()

    if content:
        return eval(content)
    else:
        return False
    pass


def setClassSetting():
    pass
