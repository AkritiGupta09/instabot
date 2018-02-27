import requests
from pprint import pprint

response=requests.get("https://api.jsonbin.io/b/59d0f30408be13271f7df29c").json()
APP_ACCESS_TOKEN=response['access_token']
BASE_URL='https://api.instagram.com/v1/'

def owner_inf0():
    response=requests.get('%susers/self/?access_token=%s'%(BASE_URL,APP_ACCESS_TOKEN)).json()
    if response['meta']['code']==200:
        print "Username is %s" % (response['data']['username'])
        print "No of followers are:%s" % (response['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (response['data']['counts']['follows'])
        print 'No. of posts: %s' % (response['data']['counts']['media'])
    else:
        print "Code other than 200 received "
owner_inf0()

def owner_recent_post():
    response = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()
    if response['meta']['code'] == 200:
        print "The owner's most recent post is:%s" %(response['data'][0]['link'])
    else:
        print "Code other than 200 received "


owner_recent_post()
