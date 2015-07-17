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

#group_id = '24098940'
#group_id = '67824212'#128
group_id = '59142119'#1072

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
        #uni before '\n'
        uni = member.get('university_name')
        if member.get('university_name'):
            uni = member.get('university_name')[:10]
            if uni.find('\n'):
                uni = uni[:uni.find('\n')-1]

        insert = "INSERT INTO vk_stat (count_members, uid, sex, first_name, last_name, bdate, country, city, online, online_mobile, university_name) " \
                 "VALUES ('%d', '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                 (count_members, member.get('uid'), member.get('sex'), member.get('first_name'), member.get('last_name'), member.get('bdate'), member.get('country'), member.get('city'), member.get('online'), member.get('online_mobile'), uni)#, member.get('status'))
        try:
            cursor.execute(insert)
            db.commit()
        except:
            db.rollback()
            print('Error')
        print (count_members, member.get('uid'))
        count_members+=1
    offset+=max_offset
'''
try:
    cursor.execute('select * from vk_stat')
    read_table = cursor.fetchall()
    for line in read_table:
        print(line[10])
    print 'Line count = ', cursor.rowcount
except:
    print 'Error'
'''
db.close()
