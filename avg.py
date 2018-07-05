#!/usr/bin/python
# -*- coding: utf-8 -*-
#获取广东省内各个站点的日平均温
#数据来源于 http://q-weather.info/
import sys
import importlib
importlib.reload(sys)

import requests
import re
import json

#站点WMO编号
idlist=[57988,57989,57996,59071,59072,59074,59075,59081,59082,59087
,59088,59090,59094,59096,59097,59099,59106,59107,59109,59114,59116
,59117,59264,59268,59269,59270,59271,59276,59278,59279,59280,59284
,59285,59287,59288,59289,59290,59293,59294,59297,59298,59303,59304
,59306,59310,59312,59313,59314,59315,59316,59317,59318,59319,59324
,59456,59462,59469,59470,59471,59473,59475,59476,59477,59478,59480
,59481,59485,59487,59488,59492,59493,59500,59501,59502,59650,59653
,59654,59655,59656,59658,59659,59663,59664,59673,59750,59754]

#正则
r=[]
r.append(re.compile(r'<h1>(.*?) 站的今日实况</h1>'))
r.append(re.compile(r'02:00:00</td>\s*<td>(.*?)</td>'))
r.append(re.compile(r'08:00:00</td>\s*<td>(.*?)</td>'))
r.append(re.compile(r'14:00:00</td>\s*<td>(.*?)</td>'))
r.append(re.compile(r'20:00:00</td>\s*<td>(.*?)</td>'))
r.append(re.compile(r'<tr align="center">\s*<td>(.*?) 02:00:00</td>'))

#获取并处理数据
data = {}
t = ['station','02','08','14','20']
print("Program Start")
for j in range(len(idlist)):
    url = "http://q-weather.info/weather/"+str(idlist[j])+"/today/"
    page = requests.get(url)
    page = page.text
    d = {}
    for k in range(len(t)-1):
        d[t[k+1]] = r[k+1].findall(page)[0]
    if d['02'] != "" and d['08'] != "" and d['14'] != "" and d['20'] != "":
        avg = (float(d['02'])+float(d['08'])+float(d['14'])+float(d['20']))/4
        if avg*10-int(avg*10)>=0.5:
            avg = (int(avg*10)+1)/10
        else:
            avg = int(avg*10)/10
        d['avg']=avg
        data[r[0].findall(page)[0]] = d
    else:
        d['avg']='data-err'
    print(str(j+1)+"/"+str(len(idlist))+","+str(round((j+1)*100/len(idlist),2))+"%")
data['date']=r[5].findall(page)[0]
print("Data loaded! Start trun to json.")

#写入json
jsondata = json.dumps(data)
f=open('/home/wwwroot/default/data/avg.json','w+')
f.write(jsondata)
f.close()
print("Json written.")

#不提供文件下载
'''
recofile = open('/home/wwwroot/default/data/Day-avg-T.txt','w+')
recofile.write("Date:"+data['date']+"\n")
recofile.write("Station,t0200,t0800,t1400,t2000,avgT\n")
for key in data:
    if key!='date':
        recofile.write(key.encode("utf8")+","+data[key]['02']+","+data[key]['08']+","+data[key]['14']+","+data[key]['20']+","+str(data[key]['avg'])+"\n")
recofile.close()
print('finish')
'''
