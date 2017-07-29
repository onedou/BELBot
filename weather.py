from wxpy import *

import request
import json

bot = Bot('bot.pkl', console_qr=True)

def weather():
	url  = "http://api.yytianqi.com/forecast7d?city=CH280800&key=esmiwq4we3k018ia"
	jsonData = request.request(url)
	jsonData = json.loads(jsonData)
	#print(jsonData)
	
	city = jsonData['data']['cityName']
	weatherinfo = jsonData['data']['list'][0]

	text = "温馨提示：今天（" + weatherinfo['date'] + "）" + city +\
		   weatherinfo['tq1'] + "转" + weatherinfo['tq2'] + "，" +\
	       weatherinfo['qw1'] + "到" + weatherinfo['qw2'] + "度，" +\
	       "吹" + weatherinfo['fl1'] + weatherinfo['fx1']

	bot.groups().search('贝尔乐早教-2017年')[0].send(text)