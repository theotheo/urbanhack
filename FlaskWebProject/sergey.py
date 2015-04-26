# -*- coding: UTF-8 -*-
 
__author__ = 'dudevil'
 
import urllib2, json, urllib, time
import pandas as pd
token = 'b0380e57dc39211e4a1306999510b1cf3cda5947f6ba504ffa0fee79136a73dba4b27387e0a55e8614107' #Ваш токен
 
 
def get_vkCity(city):
    url = u'https://api.vk.com/method/database.getCities?%s'
    params = urllib.urlencode({
        'q': city.encode('utf-8'),
        'count': 1000,
        'country_id': 1})
 
    res = urllib2.urlopen(url % params).read()
    data = json.loads(res)
    if u'response' in data:
        return data[u'response'][0].get('cid', '-1')
    else:
        print "Something went wrong while getting city"
        print data
        return []
 
def user_search(city, uid, with_friends=True):
    url = u'https://api.vk.com/method/friends.get?%s'
    url_friends = u'https://api.vk.com/method/friends.get?%s'
    params = urllib.urlencode({
        'city': city,
        'count': 1000,
        'fields' : 'city',
        'user_id': uid})
    friends_params = {
        'count': 1000,
        'fields': 'city,universities,occupation,photo_100'}
 
    res = urllib2.urlopen(url % params).read()
    data = json.loads(res)
 
    if 'error' in data:
        print data
        print "I hope this won't happen during the presentaion."
        return []
    friends = filter(lambda x: x.get('city', -1) == city, data[u'response'][1:])
    friends2 = []
    for friend in friends:
         friends_params['user_id'] = friend[u'uid']
    #     time.sleep(.5)
         res = urllib2.urlopen(url_friends % urllib.urlencode(friends_params)).read()
         data = json.loads(res)
         if u'response' in data:
             return data[u'response'][1:]
         else:
             print data
    return friends2
 
def get_groups(group_ids):
    url = u'https://api.vk.com/method/groups.getById?%s'
    params = urllib.urlencode({
        'access_token': token,
        'group_ids' : group_ids,
        'count': 1000,
        'fields': 'city,places'})
    res = urllib2.urlopen(url % params).read()
    data = json.loads(res)
    if u'response' in data:
        return data[u'response'][1:]
    else:
        print "Something went wrong while getting groups"
        print data
        return []
 
 
def get_recommendations(uid, start, target):
    start_city = get_vkCity(start)
    target_city = get_vkCity(target)
    # 857 Dolgopa-City - МГУ
    res = user_search(start_city, uid)
    # normalize occupations and institution
    for item in res:
        if 'occupation' in item:
            item['occupation_type'] = item['occupation']['type']
            item['occupation_id'] = item['occupation'].get('id', pd.np.NAN)
        if 'universities' in item:
            pass # do something with universities

    friends2df = pd.DataFrame(res)
    work_ids = friends2df[friends2df.occupation_id.notnull() &
                          (friends2df.occupation_type == 'work')].occupation_id

    works = ','.join(map(str, work_ids.astype('int')))

    worksdf = pd.DataFrame(get_groups(works))

    grand = pd.merge(friends2df, worksdf[['gid', 'city']], how='left', left_on='occupation_id', right_on='gid', sort=False)

    return grand[grand.city_x == start_city & (grand.city_y == target_city)]