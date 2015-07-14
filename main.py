__author__ = 'eq'
# -*- coding: utf-8 -*-
import urllib, json
import sys
sys.path.append('/home/eq/PycharmProjects/00_pass')
from logpass import msql_user_name, msql_user_pass
import MySQLdb

db = MySQLdb.connect('localhost', msql_user_name, msql_user_pass, 'vk_stat')
db.set_character_set('utf8')
cursor = db.cursor()
#cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
#cursor.execute('SET character_set_connection=utf8;')

#group_id = '24098940'
group_id = '67824212'
#group_id = '59142119'

offset = 0
max_offset = 1000
fields = 'bdate,sex,city,country,online,online_mobile,education,status'

#num of members
url_members = 'https://api.vk.com/method/groups.getMembers?group_id={0}'.format(group_id)
response_url_members = urllib.urlopen(url_members)
num_members = json.loads(response_url_members.read())['response']['count']

#num of iters
if num_members%max_offset == 0:
    num_iters = num_members/max_offset
else:
    num_iters = num_members/max_offset + 1

count_members = 1
for i in range(num_iters):
    url_members = 'https://api.vk.com/method/groups.getMembers?group_id={0}&offset={1}&fields={2}'.format(group_id, offset, fields)
    response_url_members = urllib.urlopen(url_members)
    members = json.loads(response_url_members.read())['response']['users']
    for member in members:
        '''
        insert = "INSERT INTO vk_stat_02 ('count_members', 'uid', 'sex', 'first_name', 'last_name', 'bdate', 'country', 'city', 'online', 'online_mobile', 'university_name', 'status') " \
         "VALUES ('%d', '%d', '%d', '%s', '%s', '%s', '%d, '%d', '%d','%d','%s','%s')" % \
                 (count_members, member.get('uid'), member.get('sex'), member.get('first_name'), member.get('last_name'), member.get('bdate'), member.get('country'), member.get('city'), member.get('online'), member.get('online_mobile'), member.get('university_name'), member.get('status'))
        '''
        insert = "INSERT INTO vk_stat (count_members, uid, sex, first_name) " \
                 "VALUES ('%d', '%d', '%d', '%s')" % \
                 (count_members, member.get('uid'), member.get('sex'), member.get('first_name'))
        try:
            cursor.execute(insert)
            db.commit()
        except:
            db.rollback()
            print('Error')
        print(count_members, member.get('first_name'))
        count_members+=1
    offset+=max_offset

db.close()
