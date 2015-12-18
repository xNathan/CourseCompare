# -*- coding: utf-8 -*-

import sys
import csv
import json
import codecs
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

USER_NAME = 'YOUR_USERNAME'
PASSWORD = 'PASSWORD'
USER_NAME = '2201401213'
PASSWORD = '213021'

try:
    conn = MongoClient()
    db = conn.jufexuanke
except Exception, e:
    print e
    sys.exit(1)


csv_file = codecs.open('152.csv', 'rb')
csv_reader = csv.reader(csv_file)

s = requests.Session()

# First, log in
login_url = 'http://cas.jxufe.edu.cn/cas/login?username={}&password={}'\
            '&service=http://xfz.jxufe.edu.cn/portal/sso/login&'\
            'renew=true'.format(USER_NAME, PASSWORD)
res_url = s.get(login_url, timeout=10).url
assert res_url == 'http://xfz.jxufe.edu.cn/portal/main.xsp/page/-1'


def get_course_detail(course_code):
    """Search course detail list for speific course code and term
    Params:
        course_code
    Returns:
        A list contains all course detail lists
    """
    url = 'http://xfz.jxufe.edu.cn/portal/main.xsp/page/-2/?.a.p=aT0lMkZ4Z'\
        'npwb3J0YWwlMkZpbmZvcjRBbGwmdD1yJnM9bm9ybWFsJmVzPWRldGFjaCZtPXZpZXc'\
        '%3D&mlinkf=infor4All/index.jsp'
    data = {
        'doSearch': '查询',
        'searchBy': 'CourseCode',
        'searchContext': '',
        'term': '152',
    }
    data['searchContext'] = course_code
    response = s.post(url, data=data)
    data = response.content
    soup = BeautifulSoup(data, 'lxml')

    # Get all courses data
    courses = soup.find('table', class_='Table').find_all('tr')[1:]
    result = map(lambda x: [i.text.strip() for i in x.find_all('td')], courses)
    return result


def save_data(data):
    for item in data:
        item_dict = dict(
            zip(['courseCode', 'classNO', 'credit',
                 'courseName', 'teacherName', 'classroomType',
                 'time1', 'time2', 'time3',
                 'classroom1', 'classroom2', 'classroom3', 'totalWeek',
                 'selectedNum', 'totalNum',
                 'isMain'], item))
        isExist = db.course.find({'courseCode': item_dict['courseCode'],
                                  'classNO': item_dict['classNO']}).count()
        if isExist:
            print 'Existed', item_dict['courseName'], item_dict['classNO'], \
                item_dict['teacherName']
        else:
            print 'Insert', item_dict['courseName'], item_dict['classNO'], \
                item_dict['teacherName']
            db.course.insert(item_dict)


def main():
    csv_reader.next()
    for line in csv_reader:
        course_code = line[1]
        print course_code


if __name__ == '__main__':
    # main()
    data = get_course_detail('01013')
    save_data(data)
