import requests
import urllib
from pprint import pprint

response=requests.get("https://api.jsonbin.io/b/59d0f30408be13271f7df29c").json()
APP_ACCESS_TOKEN=response['access_token']
BASE_URL='https://api.instagram.com/v1/'



def owner_info():
    response=requests.get('%susers/self/?access_token=%s'%(BASE_URL,APP_ACCESS_TOKEN)).json()
    if response['meta']['code']==200:
        print "Username is %s" % (response['data']['username'])
        print "No of followers are:%s" % (response['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (response['data']['counts']['follows'])
        print 'No. of posts: %s' % (response['data']['counts']['media'])
    else:
        print "Code other than 200 received "

def owner_recent_post():
    response = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()
    if response['meta']['code'] == 200:
        url=response['data'][0]['images']['standard_resolution']['url']
        name=response['data'][0]['id']+'.jpg'
        urllib.urlretrieve(url,name)
        print "Download complete"
    else:
        print "Code other than 200 received "


def get_user_id(uname):
    response = requests.get('%susers/search?q=%s&access_token=%s' % (BASE_URL,uname, APP_ACCESS_TOKEN)).json()
    return response['data'][0]['id']

def user_info(uname):
    user_id=get_user_id(uname)
    response = requests.get('%susers/%s/?access_token=%s' % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if response['meta']['code'] == 200:
        print "Username is %s" % (response['data']['username'])
        print "No of followers are:%s" % (response['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (response['data']['counts']['follows'])
        print 'No. of posts: %s' % (response['data']['counts']['media'])
    else:
        print "Code other than 200 received "

def user_post(username):
    user_id = get_user_id(username)
    response = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if response['meta']['code'] == 200:
        pprint(response)
        url = response['data'][0]['images']['standard_resolution']['url']
        name = response['data'][0]['id'] + '.jpg'
        urllib.urlretrieve(url, name)
        print "Image Download complete"
        url=response['data'][0]['videos']['standard_resolution']['url']
        name=response['data'][0]['id'] + '.mp4'
        urllib.urlretrieve(url,name)
        print"Video Download complete"
    else:
        print "Code other than 200 received "


def start_bot():
    show_menu=True
    while show_menu:
        menu_choice=input("What do you want to do? 1.Get owner info\n 2.Get owner post\n 3.Get user info\n 4.Get user post\n 0.Exit\n")
        if menu_choice==1:
            owner_info()
        elif menu_choice==2:
            owner_recent_post()
        elif menu_choice==3:
            username=raw_input("Write the name of user from whom you want to fetch data:")
            user_info(username)
        elif menu_choice==4:
            username = raw_input("Write the name of user from whom you want to fetch data:")
            user_post(username)
        elif menu_choice==0:
            show_menu=False
        else:
            print "Invalid Choice "

start_bot()