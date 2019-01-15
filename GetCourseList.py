#coding:utf-8
import SysuUEMS
import json

# "东校园":"5063559",
# "北校园":"5062202",
# "南校园":"5062201",
# "深圳校区":"333291143",
# "珠海校区":"5062203"

# "专选"
# "专必"
# "公选"
# "体育"
# "大英"

if __name__ == "__main__":
    campus=u"东校园"
    courseType=u"公选"
    if SysuUEMS.loadLoginInfo() is None:
        print("登录信息过期，请重新登录")
        exit
    fp=open("CampusId.json")
    campusIds=json.load(fp)
    fp.close()
    fp=open("CourseType.json")
    courseTypes=json.load(fp)
    fp.close()

    campusId=campusIds[campus]
    selectedCate=courseTypes[courseType]['selectedCate']
    selectedType=courseTypes[courseType]['selectedType']
    courses=SysuUEMS.getAllCourseList(campusId,selectedCate,selectedType)
    fp=open("courses.json","w")
    json.dump(courses,fp)
    fp.close()
    courses=SysuUEMS.coursesRawData2VisualData(courses)
    print(courses)
    fp=open("Courses.txt","w")
    fp.write(courses.encode('utf-8'))
    fp.close()