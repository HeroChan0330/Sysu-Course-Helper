#coding:utf-8
import SysuUEMS
import json


if __name__ == "__main__":
    if SysuUEMS.loadLoginInfo() is None:
        print("登录信息过期，请重新登录")
        exit
    print(SysuUEMS.selectCourse('1080280610107842560','11','4')['message'])