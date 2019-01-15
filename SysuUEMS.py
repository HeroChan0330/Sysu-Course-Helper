#coding:utf-8
import requests
import json
import os
import re
import base64
from bs4 import BeautifulSoup
import time
import Image

#cookiesTemp = cookiejar.CookieJar()
loginCookies=""
jSessionId=''
TGC=''
tempUrl=''
LYSESSIONID=''
userId=''
semesterYear=''

def downloadImage(url,fileName):
    content=requests.get(url)
    fp=open(fileName,'wb')
    fp.write(content.content)
    fp.close()

def downVertificationImage(url,fileName):#下载登录验证码
    global jSessionId
    content=requests.get(url)
    temp=content.headers['Set-Cookie']
    jSessionId=re.findall('JSESSIONID=(.*?);',temp)[0]
    fp=open(fileName,'wb')
    fp.write(content.content)
    fp.close()

def getFileContent(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def getVertification():
    requestUrl='https://cas.sysu.edu.cn/cas/captcha.jsp'
    downVertificationImage(requestUrl,"vertification.jpg")

def getLoginPageContent():
    requestUrl='https://cas.sysu.edu.cn/cas/login?service=https://uems.sysu.edu.cn/jwxt/api/sso/cas/login?pattern=student-login'
    return requests.get(requestUrl).text

def getExcution(loginPageContent):
    bs=BeautifulSoup(loginPageContent,'lxml')
    target=bs.select("input[name=execution]")
    if(len(target)>0):
        return target[0]['value']

def loginStep1(user,passwd):
    global jSessionId,loginCookies,TGC,tempUrl
    requestUrl='https://cas.sysu.edu.cn/cas/login?service=https://uems.sysu.edu.cn/jwxt/api/sso/cas/login?pattern=student-login'
    loginPageContent=getLoginPageContent()
    excution=getExcution(loginPageContent)
    getVertification()
    # os.system("vertification.jpg")
    vertifyImg=Image.open("./vertification.jpg")
    vertifyImg.show()
    print('input the captcha:')
    vertifyCode=str(raw_input())
    
    # session=requests.Session()

    formData={
        'username':user,
        'password':passwd,
        'captcha':vertifyCode,
        'execution':excution,
        '_eventId':'submit',
        'geolocation':''
    }
    #print formData
    reqHeaders={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded',
        'Host':'cas.sysu.edu.cn',
        'Referer':'https://cas.sysu.edu.cn/cas/login?service=https://uems.sysu.edu.cn/jwxt/api/sso/cas/login?pattern=student-login',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/61.0',
        'Cookie':''
    }
    reqHeaders['Cookie']+='JSESSIONID='+jSessionId+';'
    resp=requests.post(requestUrl,data=formData,headers=reqHeaders,allow_redirects=False)
    if resp.status_code!=302:
        print("bug occur")
        # return
    fp=open("temp.html","w")
    fp.write(resp.content)
    fp.close()
    tempUrl=resp.headers['Location']
    print("resp.headers")
    print(resp.headers)
    print("tempUrl")
    print(tempUrl)

    loginCookies='JSESSIONID='+jSessionId+';'+resp.headers['Set-Cookie']
    TGC=re.findall('TGC=(.*?);',resp.headers['Set-Cookie'])[0]
    # reqHeaders['Cookie']+='TGC='+TGC+';'
    # print("loginCookies")
    # print(loginCookies)
    # print("reqHeaders")
    # print(reqHeaders)


def loginStep2():
    global jSessionId,loginCookies,TGC,tempUrl,LYSESSIONID
    reqHeaders={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Host':'uems.sysu.edu.cn',
        'Pragma':'no-cache',
        'Referer':'https://cas.sysu.edu.cn/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/61.0',
        'Cookie':'',
        'DNT':'1'
    }
    resp=requests.get(tempUrl,headers=reqHeaders,allow_redirects=False)
    print("resp.headers")
    print(resp.headers)
    LYSESSIONID=re.findall('LYSESSIONID=(.*?);',resp.headers['Set-Cookie'])[0]
    print("LYSESSIONID")
    print(LYSESSIONID)
    fp=open("temp2.html","w")
    fp.write(resp.content)
    fp.close()

def loginStep3():
    global jSessionId,loginCookies,TGC,tempUrl,LYSESSIONID,userId
    reqHeaders={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Host':'uems.sysu.edu.cn',
        'Pragma':'no-cache',
        'Referer':'https://cas.sysu.edu.cn/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/61.0',
        'Cookie':'LYSESSIONID=%s'%LYSESSIONID,
        'DNT':'1'
    }
    resp=requests.get('https://uems.sysu.edu.cn/jwxt/api/sso/cas/login?pattern=student-login',headers=reqHeaders,allow_redirects=False)
    # print(resp.headers)
    userId=re.findall('user=(.*?);',resp.headers['Set-Cookie'])[0]
    print(userId)

def login(netId,passWd):
    loginStep1(netId,passWd)
    loginStep2()
    loginStep3()

def getAvator():
    global jSessionId,loginCookies,TGC,tempUrl,LYSESSIONID,userId
    reqUrl='https://uems.sysu.edu.cn/jwxt/student-status/student-info/photo'
    reqHeaders={
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Host':'uems.sysu.edu.cn',
        'Pragma':'no-cache',
        'Referer':'https://uems.sysu.edu.cn/jwxt/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/61.0',
        'Cookie':'LYSESSIONID=%s;user=%s'%(LYSESSIONID,userId),
        'DNT':'1'
    }
    resp=requests.get(reqUrl,headers=reqHeaders,allow_redirects=False)
    fp=open("avator.jpg","wb")
    fp.write(resp.content)
    fp.close()

def saveLoginInfo():
    global jSessionId,loginCookies,TGC,tempUrl,LYSESSIONID,userId
    info={"LYSESSIONID":LYSESSIONID,"user":userId}
    fp=open("info.json","w")
    json.dump(info,fp)
    fp.close()

def loadLoginInfo():
    global jSessionId,loginCookies,TGC,tempUrl,LYSESSIONID,userId
    fp=open("info.json","r")
    info=json.load(fp)
    fp.close()
    LYSESSIONID=info['LYSESSIONID']
    userId=info['user']
    if getYearTerm() is None:
        return False
    return True

def getYearTerm():
    global jSessionId,loginCookies,TGC,tempUrl,LYSESSIONID,userId,semesterYear
    reqUrl='https://uems.sysu.edu.cn/jwxt/choose-course-front-server/stuCollectedCourse/getYearTerm?t=%d'%(int(time.time()))
    reqHeaders={
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Host':'uems.sysu.edu.cn',
        'Pragma':'no-cache',
        'Referer':'https://uems.sysu.edu.cn/jwxt/mk/courseSelection/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/61.0',
        'Cookie':'LYSESSIONID=%s;user=%s'%(LYSESSIONID,userId),
        'DNT':'1',
        'lastAccessTime':str(int(time.time()*1000)),
        'X-Requested-With':'XMLHttpRequest',
        'menuId':'null',
        'moduleId':'null'
    }
    resp=requests.get(reqUrl,headers=reqHeaders)
    resJson=resp.json()
    if resJson['code']!=200:
        return None
    semesterYear=resJson['data']
    return resJson['data']

def getCourseList(pageNo,pageSize,campusId,selectedCate,selectedType):
    global jSessionId,loginCookies,TGC,tempUrl,LYSESSIONID,userId,semesterYear
    reqUrl='https://uems.sysu.edu.cn/jwxt/choose-course-front-server/classCourseInfo/course/list?t=%d'%(int(time.time()))
    reqHeaders={
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Type':'application/json;charset=utf-8',
        'Host':'uems.sysu.edu.cn',
        'Referer':'https://uems.sysu.edu.cn/jwxt/mk/courseSelection/',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/61.0',
        'Cookie':'LYSESSIONID=%s;user=%s'%(LYSESSIONID,userId),
        'DNT':'1',
        'lastAccessTime':str(int(time.time()*1000)),
    }
    formData={
        'pageNo':str(pageNo),
        'pageSize':str(pageSize),
        'param':{
            'collectionStatus':'0',
            'hiddenConflictStatus':'0',
            'hiddenSelectedStatus':'0',
            'selectedCate':selectedCate,
            'selectedType':selectedType,
            'semesterYear':semesterYear,
            'studyCampusId':campusId
        }
    }
    resp=requests.post(reqUrl,json=formData,headers=reqHeaders)
    resJson=resp.json()
    if resJson['code']!=200:
        return None
    return resJson['data']['total'],resJson['data']['rows']

def getAllCourseList(campusId,selectedCate,selectedType):
    sum=0
    courses=[]
    index=1
    totalNum,coursesTemp=getCourseList(1,10,campusId,selectedCate,selectedType)
    sum+=len(coursesTemp)
    courses+=coursesTemp
    while sum<totalNum:
        index+=1
        totalNum,coursesTemp=getCourseList(index,10,campusId,selectedCate,selectedType)
        sum+=len(coursesTemp)
        courses+=coursesTemp
    return courses

def coursesRawData2VisualData(courses):
    ret=''
    for course in courses:
        formatStr=u'课程:%s\n\tID:%s\n'%(course['courseName'],course['teachingClassId'])
        ret+=formatStr
    return ret

def getSelectedCourse():
    global jSessionId,loginCookies,TGC,tempUrl,LYSESSIONID,userId,semesterYear
    reqUrl='https://uems.sysu.edu.cn/jwxt/choose-course-front-server/selectedCourse/list?t=%d'%(int(time.time()))
    reqHeaders={
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Type':'application/json;charset=utf-8',
        'Host':'uems.sysu.edu.cn',
        'Referer':'https://uems.sysu.edu.cn/jwxt/mk/courseSelection/',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/61.0',
        'Cookie':'LYSESSIONID=%s;user=%s'%(LYSESSIONID,userId),
        'DNT':'1',
        'lastAccessTime':str(int(time.time()*1000)),
    }
    formData={
        'pageNo':'1',
        'pageSize':'20',
        'param':{
            'failureStatus':'0',
            'retiredClass':'0',
            'successStatus':'1',
            'waitingScreen':'0'
        },
        'total':'true'
    }
    resp=requests.post(reqUrl,json=formData,headers=reqHeaders)
    resJson=resp.json()
    if resJson['code']!=200:
        return None
    return resJson['data']['rows']


def selectCourse(teachingClassId,selectedCate,selectedType):
    global jSessionId,loginCookies,TGC,tempUrl,LYSESSIONID,userId,semesterYear
    reqUrl='https://uems.sysu.edu.cn/jwxt/choose-course-front-server/classCourseInfo/course/choose?t=%d'%(int(time.time()))
    reqHeaders={
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Type':'application/json;charset=utf-8',
        'Host':'uems.sysu.edu.cn',
        'Referer':'https://uems.sysu.edu.cn/jwxt/mk/courseSelection/',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/61.0',
        'Cookie':'LYSESSIONID=%s;user=%s'%(LYSESSIONID,userId),
        'DNT':'1',
        'lastAccessTime':str(int(time.time()*1000)),
    }
    formData={
        'check':'true',
        'clazzId':teachingClassId,
        'selectedCate':selectedCate,
        'selectedType':selectedType,
    }
    resp=requests.post(reqUrl,json=formData,headers=reqHeaders)
    resJson=resp.json()
    return resJson


if __name__=="__main__":
    # login(u"netId",u"passwd")
    # saveLoginInfo()
    loadLoginInfo()
    # getAvator()
    print(getYearTerm())
    selectedCourses=getSelectedCourse()
    for course in selectedCourses:
        print(u'name:%s\tid:%s'%(course['courseName'],course['teachingClassId']))