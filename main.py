__author__ = 'eq'
# -*- coding: UTF-8 -*-
import urllib, json
import collections

#group_id = '24098940'#77000
#group_id = '67824212'#128
group_id = '59142119'#1072
#group_id = '60305152'#2400

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
first_names = []
last_names = []
countries = []
cities = []
years = []
universities = []
statuses = []
man, woman = 0, 0

for i in range(num_iters):
    url_members = 'https://api.vk.com/method/groups.getMembers?group_id={0}&offset={1}&fields={2}'.format(group_id, i*max_offset, fields)
    response_url_members = urllib.urlopen(url_members)
    members = json.loads(response_url_members.read())['response']['users']

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

        #countries and cites
        countries.append(member.get('country'))
        cities.append(member.get('city'))

        #university
        universities.append(member.get('university_name'))

        #statuses
        if member.get('status'):
            statuses.append(member.get('status').lower())
        print count_members



        count_members+=1


print('-----------sex--------------')
print 'man: ', man, '\nwoman: ', woman


print('-----------first_names--------------')
#sorting dict
fr_first_names = collections.Counter()
for name in first_names:
    fr_first_names[name]+=1

list_fr_first_names = fr_first_names.items()

#sorting list
list_fr_first_names.sort(key=lambda item: item[1], reverse=True)
for item in list_fr_first_names:
    if item[1] > 100:
        print item[1], item[0]


print('-----------last_names--------------')
fr_last_names = collections.Counter()
for l_name in last_names:
    fr_last_names[l_name]+=1

list_fr_last_names = fr_last_names.items()

list_fr_last_names.sort(key=lambda item: item[1], reverse=True)
for item in list_fr_last_names:
    if item[1] > 100:
        print item[1], item[0]


print('-----------years--------------')
fr_years = collections.Counter()
for year in years:
    fr_years[year]+=1

list_fr_years = fr_years.items()

list_fr_years.sort(key=lambda item: item[1], reverse=True)
for item in list_fr_years:
    if item[1] > 100:
        print item[1], item[0]


print('-----------countries--------------')
fr_country = collections.Counter()
for country in countries:
    fr_country[country]+=1

list_fr_country = fr_country.items()

list_fr_country.sort(key=lambda item: item[1], reverse=True)
for item in list_fr_country:
    if item[1] > 50 and item[0] > 0:
        url_country = 'https://api.vk.com/method/database.getCountriesById?country_ids={}'.format(item[0])
        response_url_country = urllib.urlopen(url_country)
        country = json.loads(response_url_country.read())['response'][0]['name']
        print item[1], country


print('-----------cities--------------')
fr_cities = collections.Counter()
for city in cities:
    fr_cities[city]+=1

list_fr_cities = fr_cities.items()

list_fr_cities.sort(key=lambda item: item[1], reverse=True)
for item in list_fr_cities:
    if item[1] > 75 and item[0] > 0:
        url_city = 'https://api.vk.com/method/database.getCitiesById?city_ids={}'.format(item[0])
        response_url_city = urllib.urlopen(url_city)
        city = json.loads(response_url_city.read())['response'][0]['name']
        print item[1], city


print('-----------universities--------------')
fr_universities = collections.Counter()
for university in universities:
    fr_universities[university]+=1

list_fr_universities = fr_universities.items()

#sorting list
list_fr_universities.sort(key=lambda item: item[1], reverse=True)
for item in list_fr_universities:
    if item[1] > 10:
        print item[1], item[0]


print('-----------statuses--------------')
fr_statuses = collections.Counter()
for status in statuses:
    fr_statuses[status]+=1

list_fr_statuses = fr_statuses.items()

#sorting list
list_fr_statuses.sort(key=lambda item: item[1], reverse=True)
for item in list_fr_statuses:
    if item[1] > 5:
        print item[1], item[0]


print('-----------statuses_words--------------')
statuses_words = ' '.join(statuses)
statuses_words_split = statuses_words.split()

fr_statuses_words = collections.Counter()
for word in statuses_words_split:
    fr_statuses_words[word]+=1

list_fr_statuses_words = fr_statuses_words.items()

#sorting list
list_fr_statuses_words.sort(key=lambda item: item[1], reverse=True)
for item in list_fr_statuses_words:
    if item[1] > 20:
        print item[1], item[0]