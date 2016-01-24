#!/usr/bin/python3
#coding:utf-8
import fbchat as fc
import time
import configparser as cp
import datetime
import logging
ini=cp.ConfigParser()
logging.basicConfig(filename='log.txt',level=logging.DEBUG,format='%(asctime)s %(message)s')
ini.read('RegularReport.ini')
client=fc.Client(ini['Base']['Account'],ini['Base']['Password'])
message=ini['Auto Return Follow people']['Message']
SessionID=ini['Auto Return Follow people']['SID']
FollowList=ini['Auto Return Follow people']['FollowsPeople'].split(';')
trigger_word=ini['Auto Return Follow people']['trigger_word']
RegularExecTime=ini['Base']['RegularExecTime']
ExcCircle=int(ini['Base']['ExcCircle(sec)'])
mode=ini['Base']['mode']
DeepSleep=int(ini['Base']['DeepSleep(hour)'])*3600
last_exc_day_flag=0
while True:
	logging.info('Start to rest(%d sec)'%ExcCircle)
	time.sleep(ExcCircle)
	logging.info('Wake up(from rest %d sec)'%ExcCircle)
	if last_exc_day_flag==time.strftime('%D'):
		logging.info('Today is Finish')
		continue
	now=time.strftime('%H:%M')
	if mode=='Auto Return Follow people':
		logging.info('Getting ChatInfo')
		chat_room=client.getGroupThreadInfo(SessionID,0)
		logging.info('Successed get ChatInfo')
		for i in chat_room:
			if datetime.date.fromtimestamp(int(i.__dict__['timestamp'])/1000).strftime('%m/%d') != time.strftime('%m/%d'):
				logging.info('Today Nobody Chat')
				break
			if i.__dict__['author_email'] in FollowList and trigger_word in i.__dict__['body']:
				logging.info('Find %s say %s,sendGroup message'%(client.getUsers(i.__dict__['author_email'])[0],i.__dict__['body']))
				client.sendGroup(SessionID,message)
				logging.info('Successed sendGroup')
				last_exc_day_flag=time.strftime('%D')
				logging.info('Mark flag,start to Deep Sleep')
				time.sleep(DeepSleep)
				logging.info('Wark up from Deep Sleep')
				break
