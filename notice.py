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
	pass

def classNotice(msgDict):
	now      = int(time.time())
	nowArray = time.localtime(now)

	message = ""
	week    = nowArray.tm_wday

	if week == 0:
		message = msgDict['monday']
		pass
	elif week == 1:
		message = msgDict['tuesday']
		pass
	elif week == 2:
		message = msgDict['wednesday']
		pass
	elif week == 3:
		message = msgDict['thursday']
		pass
	elif week == 4:
		message = msgDict['friday']
		pass
	elif week == 5:
		message = msgDict['saturday']
		pass
	elif week == 6:
		message = msgDict['sunday']
		pass

	print(message)
	bot.groups().search('贝尔乐成长营')[1].send(message)
	pass


def classTodayMorningNotice():
	msgDict = {}

	msgDict['monday']    = "温馨提示：今天早上（周一）9:00--11:30是暑期小学生逻辑狗班上课，请孩子们准时来上课。"
	msgDict['tuesday']   = "温馨提示：今天早上（周二）9:00--11:30是暑期小学生逻辑狗班上课，请孩子们准时来上课。"
	msgDict['wednesday'] = "温馨提示：今天（周三）晚上7:30--8:30，请孩子们准时来上课。"
	msgDict['thursday']  = "温馨提示：今天（周四）晚上7:30--8:30，请孩子们准时来上课。"
	msgDict['friday']    = "温馨提示：今天（周五）晚上7:30--8:30，请孩子们准时来上课。"
	msgDict['saturday']  = "温馨提示：今天（周六）早上9:00--10:30，请孩子们准时来上课。"
	msgDict['sunday']    = "祝大家周末愉快！"

	clasNotice(msgDict)
	pass

def classTomorrowNotice():
	msgDict = {}

	msgDict['monday']    = "温馨提示：明天早上（周一）9:00--11:30是暑期小学生逻辑狗班上课，请孩子们准时来上课。"
	msgDict['tuesday']   = "温馨提示：明天早上（周二）9:00--11:30是暑期小学生逻辑狗班上课，请孩子们准时来上课。"
	msgDict['wednesday'] = "温馨提示：今天（周三）晚上7:30--8:30，请孩子们准时来上课。"
	msgDict['thursday']  = "温馨提示：今天（周四）晚上7:30--8:30，请孩子们准时来上课。"
	msgDict['friday']    = "温馨提示：今天（周五）晚上7:30--8:30，请孩子们准时来上课。"
	msgDict['saturday']  = "温馨提示：今天（周六）早上9:00--10:30，请孩子们准时来上课。"
	msgDict['sunday']    = "祝大家周末愉快！"

	clasNotice(msgDict)
	pass


