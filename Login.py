#coding:utf-8
import SysuUEMS

if __name__ == "__main__":
    netId=u"netId"
    passWord=u"passwd"
    SysuUEMS.login(netId,passWord)
    SysuUEMS.saveLoginInfo()