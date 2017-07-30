from wxpy import *

import request
import json
import time

bot = Bot('bot.pkl', console_qr=True)

def weather():
	url  = "http://api.yytianqi.com/forecast7d?city=CH280800&key=esmiwq4we3k018ia"
	jsonData = request.request(url)
	jsonData = json.loads(jsonData)
	#print(jsonData)
	
	city = jsonData['data']['cityName']
	weatherinfo = jsonData['data']['list'][0]

	text = "温馨提示：今天（" + weatherinfo['date'] + "）" + city + \
		   "白天：" + weatherinfo['tq1'] + "，气温" + weatherinfo['qw1'] + "度，风力" + weatherinfo['fl1'] + weatherinfo['fx1'] + ";" +\
	       "晚间：" + weatherinfo['tq2'] + "，气温" + weatherinfo['qw2'] + "度，风力" + weatherinfo['fl2'] + weatherinfo['fx2'] + ";"

	print(text)
	bot.groups().search('贝尔乐早教-2017年')[0].send(text)
	bot.groups().search('贝尔乐成长营')[1].send(text)

def classNotice():
	monday    = """温馨提示：今天（周一）晚上7:30--8:30，请孩子们准时来上课。"""
	tuesday   = """温馨提示：今天（周二）晚上7:30--8:30，请孩子们准时来上课。"""
	wednesday = """温馨提示：今天（周三）晚上7:30--8:30，请孩子们准时来上课。"""
	thursday  = """温馨提示：今天（周四）晚上7:30--8:30，请孩子们准时来上课。"""
	friday    = """温馨提示：今天（周五）晚上7:30--8:30，请孩子们准时来上课。"""
	saturday  = """温馨提示：今天（周六）早上9:00--10:30，请孩子们准时来上课。"""
	sunday    = """祝大家周末愉快！"""

	now      = int(time.time())
	nowArray = time.localtime(now)

	message = ""
	week    = nowArray.tm_wday

	if week == 0:
		message = monday
		pass
	elif week == 1:
		message = tuesday
		pass
	elif week == 2:
		message = wednesday
		pass
	elif week == 3:
		message = thursday
		pass
	elif week == 4:
		message = friday
		pass
	elif week == 5:
		message = saturday
		pass
	elif week == 6:
		message = sunday
		pass

	print(message)
	bot.groups().search('贝尔乐成长营')[1].send(message)
	pass