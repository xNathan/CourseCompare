# -*- coding: utf-8 -*-

import sys
import csv
import json
import logging
import codecs
import requests
import Queue
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

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

csv_file = codecs.open('152.csv', 'rb', 'gb18030')
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
        item_dict['isMain'] = '1' if item_dict['isMain'] == u'主' else '0'
        isExist = db.course.find({'courseCode': item_dict['courseCode'],
                                  'classNO': item_dict['classNO']}).count()
        if isExist:
            logger.info('Existed {} {} {}'.format(item_dict['courseName'],
                                                  item_dict['classNO'],
                                                  item_dict['teacherName']))
        else:
            logger.info('Inserted {} {} {}'.format(item_dict['courseName'],
                                                   item_dict['classNO'],
                                                   item_dict['teacherName']))
            db.course.insert(item_dict)


def compare_data(data):
    """Check if data is the same
    Params:
        source: data from csv file
        target: data from website
    Returns:
        Bool: True for the same, False for not
    """
    data_dict = dict(zip(['major', 'courseCode', 'courseName', 'classNO',
                          'teacherName', 'credit', 'classroomType', '_',
                          'time1', 'time2', 'time3', 'totalNum',
                          'isMain'], data))
    origin_data = db.course.find_one({'courseCode': data_dict['courseCode'],
                                      'classNO': data_dict['classNO']})
    if origin_data:
        return str(origin_data['time1']) == str(data_dict['time1']) and \
            str(origin_data['time2']) == str(data_dict['time2']) and \
            str(origin_data['time3']) == str(data_dict['time3']) and \
            float(origin_data['credit']) == float(data_dict['credit']) and \
            str(origin_data['isMain']) == str(data_dict['isMain'])
    else:
        logger.warning('No data')


def main():
    csv_reader.next()
    '''
    for line in csv_reader:
        if compare_data(line):
            logger.info('Passed {} {} {}'.format(line[1], line[2], line[3]))
        else:
            logger.warn('Error {} {} {}'.format(line[1], line[2], line[3]))
    '''
    course_queue = Queue.Queue()
    course_code_list = set()
    for line in csv_reader:
        course_code_list.add(line[1])
    for code in course_code_list:
        course_queue.put(code)
    print course_queue

if __name__ == '__main__':
    main()
