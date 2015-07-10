__author__ = 'eq'
# -*- coding: utf-8 -*-
import urllib, json

#group_id = '24098940'
group_id = '67824212'

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

all_members = []
for i in range(num_iters):
    url_members = 'https://api.vk.com/method/groups.getMembers?group_id={0}&offset={1}&fields={2}'.format(group_id, offset, fields)
    response_url_members = urllib.urlopen(url_members)
    members = json.loads(response_url_members.read())['response']['users']
    for j in range(max_offset-1):
        print j, members[j].get('university_name')
    offset+=max_offset
    #print members
