# -*- coding: utf-8 -*-

import csv
import requests
from bs4 import BeautifulSoup


USER_NAME = 'YOUR_USERNAME'
PASSWORD = 'PASSWORD'

_file = file('152.csv', 'rb').read()
csv_file = csv.reader(_file)

s = requests.Session()

# First, log in
login_url = 'http://cas.jxufe.edu.cn/cas/login?username={}&password={}'\
            '&service=http://xfz.jxufe.edu.cn/portal/sso/login&'\
            'renew=true'.format(USER_NAME, PASSWORD)
res_url = s.get(login_url, timeout=10).url
assert res_url == 'http://xfz.jxufe.edu.cn/portal/main.xsp/page/-1'


def get_course_detail(course_code):
    url = 'http://xfz.jxufe.edu.cn/portal/main.xsp/page/-2/?.a.p=aT0lMkZ4Z'\
        'npwb3J0YWwlMkZpbmZvcjRBbGwmdD1yJnM9bm9ybWFsJmVzPWRldGFjaCZtPXZpZXc'\
        '%3D&mlinkf=infor4All%2Findex.jsp'
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
    for item in soup.find('table', class_='Table').find_all('tr')[1:]:
        print item


def main():
    pass

if __name__ == '__main__':
    get_course_detail('01013')
