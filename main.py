# https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=V 

import requests
import time
import db

class API(object):
    def __init__(self):
        self.BASE_URL = 'https://api.vk.com/method/'
        self.GROUP_ID = -20833574
        self.DOMAIN = 'bbcradio1'
        # self.ACCESS_TOKEN = '418a186148ea32f8b3dd312215900e14640e7ee206c0f3463bfd330536e552000774e195ac1a7ed2b7e6d'
        self.ACCESS_TOKEN = '943c09df5ee197c1ee9b40728b3260ce768068e0fd8f9177aade9d600f8c432a86fda77deca9f646aeedd'

    def mercyRequest(self, url):
        time.sleep(0.33)
        tries = 5
        r = None
        while tries > 0:
            r = requests.get(url).json()
            if not r.get('error'):
                break
            else:
                time.sleep(0.33)
                tries -= 1
        return r

    def addAccessTokenAndVersionAndRequest(self, url):
        url += '&access_token=' + self.ACCESS_TOKEN
        url += '&v=5.80'
        # r = requests.get(url)
        # return r.json()
        return self.mercyRequest(url)

    def getWallPosts(self, count=100, offset=0):
        url = self.BASE_URL + 'wall.get'
        url += '?domain=' + self.DOMAIN
        url += '&count=' + str(count)
        url += '&offset=' + str(offset)
        return self.addAccessTokenAndVersionAndRequest(url)

    def getPostLikes(self, post_id, owner_id, _filter='likes', offset=0, count=1):
        url = self.BASE_URL + 'likes.getList'
        url += '?type=post'
        url += '&owner_id=' + str(owner_id)
        url += '&item_id=' + str(post_id)
        url += '&filter=' + _filter
        url += '&offset=' + str(offset)
        url += '&count=' + str(count)
        return self.addAccessTokenAndVersionAndRequest(url)
 

def getDataIfSingleAudioInPost(wall_post):

    audio = None
    for attachment in wall_post['attachments']:
        a = attachment.get('audio')
        if a is None:
            continue
        else:
            if audio is None:
                audio = a
            else:
                return False, None

    if audio is None:
        return False, None

    post_id = wall_post['id']
    owner_id = wall_post['owner_id']
    artist = audio['artist']
    title = audio['title']

    return True, {'post_id':post_id, 'artist':artist, 'title':title, 'owner_id':owner_id}


if __name__ == '__main__':
    api = API()
    r = api.getWallPosts(count=100)

    items = r['response']['items']
    for item in items:
        status, res = getDataIfSingleAudioInPost(item)
        if status and 'BBC' not in res['title'] and 'BBC' not in res['artist']:
            likers = api.getPostLikes(post_id=res['post_id'], 
                owner_id=res['owner_id'], count=100)['response']['items']
            for liker in likers:
                db.createLike(liker, res['post_id'], res['owner_id'],
                    res['artist'], res['title'])
