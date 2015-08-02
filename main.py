__author__ = 'eq'
# -*- coding: UTF-8 -*-
import urllib2, json
import collections
from multiprocessing.dummy import Pool as ThreadPool

pool = ThreadPool(16)

#group_id = '24098940'#77000
#group_id = '67824212'#128
group_id = '92410277'#23
#group_id = '59142119'#1072
#group_id = '60305152'#2400

fw = open('statistics.txt', 'w')
url_group = 'https://api.vk.com/method/groups.getById?group_id={}'.format(group_id)
response_url_members = urllib2.urlopen(url_group)
groups_name = json.loads(response_url_members.read())['response'][0]['name']
fw.write(groups_name.encode('utf-8'))
fw.close()

offset = 0
max_offset = 1000
fields = 'bdate,sex,city,country,online,online_mobile,education,status'

#num of members
url_members = 'https://api.vk.com/method/groups.getMembers?group_id={0}'.format(group_id)
response_url_members = urllib2.urlopen(url_members)
num_members = json.loads(response_url_members.read())['response']['count']

#num of iters
if num_members%max_offset == 0:
    num_iters = num_members/max_offset
else:
    num_iters = num_members/max_offset + 1

user_number = 1
first_names = []
last_names = []
countries = []
cities = []
years = []
universities = []
statuses = []
clubs = []
url_members_subs_list = []
member_subs = []
man, woman = 0, 0
user_number_in_clubs = 1

for i in range(num_iters):
    url_members = 'https://api.vk.com/method/groups.getMembers?group_id={0}&offset={1}&fields={2}'.format(group_id, i*max_offset, fields)
    response_url_members = urllib2.urlopen(url_members)
    members = json.loads(response_url_members.read())['response']['users']

    '''
    for member in members:
        url_members_subs = 'https://api.vk.com/method/users.getSubscriptions?user_id={}'.format(member.get('uid'))
        response_url_members_subs = urllib2.urlopen(url_members_subs)
        members_subs = json.loads(response_url_members_subs.read())['response']['groups']['items']
        clubs += members_subs#.append(' '.join(str(i) for i in members_subs))
        print user_number_in_clubs#, members_subs
        user_number_in_clubs+=1

    for i in range(len(clubs)):
        clubs[i] = str(clubs[i])
        '''
    for member in members:
        url_members_subs_list.append('https://api.vk.com/method/users.getSubscriptions?user_id={}'.format(member.get('uid')))

    response_url_members_subs_list = pool.map(urllib2.urlopen, url_members_subs_list)

    for i in response_url_members_subs_list:
        for response_url_members_subs in i:
            members_response = json.loads(response_url_members_subs)
            member_subs = members_response['response']['groups']['items']
            for s in member_subs:
                clubs.append(str(s))
            #clubs.append(str(subs) for subs in member_subs)
    print clubs



    for member in members:
        #years
        if member.get('bdate') and len(member.get('bdate')) > 5:#if year exists
            years.append(member.get('bdate')[-4:])

        #first_names
        first_names.append(member.get('first_name'))

        #last_names
        if member.get('last_name') and member.get('last_name')[-1] == u'а':
            last_name = member.get('last_name')[:-1]
        else:
            last_name = member.get('last_name')
        last_names.append(last_name)

        #sex
        if member.get('sex') == 1:
            woman += 1
        elif member.get('sex') == 2:
            man += 1

        #countries
        if member.get('country'):
            countries.append(member.get('country'))

        #cites
        if member.get('city'):
            cities.append(member.get('city'))

        #universities
        if member.get('university_name'):
            universities.append(member.get('university_name'))

        #statuses
        if member.get('status'):
            statuses.append(member.get('status').lower())

        print(user_number)
        user_number+=1

print years

def print_results_to_file(data):
    data = data + '\n'
    fw = open('statistics.txt', 'a')
    fw.write(data)
    fw.close()

def counting_statistic(statistics_name, value, overlap, vk_db='', ids=''):
    stat_dict = collections.Counter()
    for i in value:
        stat_dict[i] += 1

    list_from_dict = stat_dict.items()
    list_from_dict.sort(key=lambda item: item[1], reverse=True)
    print_results_to_file(statistics_name)

    for item in list_from_dict:
        if item[1] > overlap:
            if vk_db == '':
                print_results_to_file(str(item[1]) + ' ' + item[0].encode('utf-8'))
            else:
                tmp = value_by_id(vk_db, ids, item[0])
                print_results_to_file(str(item[1]) + ' ' + tmp.encode('utf-8'))

def value_by_id(vk_db, ids, id):
    response_url = urllib2.urlopen('https://api.vk.com/method/database.{}?{}={}'.format(vk_db, ids, id))
    value = json.loads(response_url.read())['response'][0]['name']
    return value

overlap_first_names = 15
overlap_last_names = 15
overlap_years = 30
overlap_universities = 10
overlap_statuses = 3
overlap_statuses_words = 50
overlap_countries = 10
overlap_cities = 30

print_results_to_file('\n\nman: ' + str(man) + '\nwoman: ' + str(woman))

counting_statistic('\n-----first_names-----', first_names, overlap_first_names)
counting_statistic('\n-----last_names-----', last_names, overlap_last_names)
counting_statistic('\n-----years-----', years, overlap_years)
counting_statistic('\n-----universities-----', universities, overlap_universities)
counting_statistic('\n-----statuses-----', statuses, overlap_statuses)

statuses_words = ' '.join(statuses)
statuses_words_split = statuses_words.split()
counting_statistic('\n-----statuses_words-----', statuses_words_split, overlap_statuses_words)

counting_statistic('\n-----countries-----', countries, overlap_countries, vk_db='getCountriesById', ids='country_ids')
counting_statistic('\n-----cities-----', cities, overlap_cities, vk_db='getCitiesById', ids='city_ids')

overlap_clubs = 10
counting_statistic('\n-----clubs-----', clubs, overlap_clubs)