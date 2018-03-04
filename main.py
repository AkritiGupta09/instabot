#Importing the libraries
import requests
import urllib
from pprint import pprint
#Importing sentiment analyzer
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


#Link to the access token
response=requests.get("https://api.jsonbin.io/b/59d0f30408be13271f7df29c").json()
APP_ACCESS_TOKEN=response['access_token']
BASE_URL='https://api.instagram.com/v1/'


#Getting the owner information
def owner_info():
    response=requests.get('%susers/self/?access_token=%s'%(BASE_URL,APP_ACCESS_TOKEN)).json()#user's self url to get own info
    if response['meta']['code']==200:#code to successful request
        print "Username is %s" % (response['data']['username'])
        print "No of followers are:%s" % (response['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (response['data']['counts']['follows'])
        print 'No. of posts: %s' % (response['data']['counts']['media'])
    else:
        print "Code other than 200 received "

#getting the recent post of own
def owner_recent_post():
    response = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()
    if response['meta']['code'] == 200:
        #two req for urllib:url,name
        url=response['data'][0]['images']['standard_resolution']['url']#specifiying url
        name=response['data'][0]['id']+'.jpg'#specifying kind of post
        urllib.urlretrieve(url,name)
        print "Download complete"
    else:
        print "Code other than 200 received "

#to fetch userid
def get_user_id(uname):
    response = requests.get('%susers/search?q=%s&access_token=%s' % (BASE_URL,uname, APP_ACCESS_TOKEN)).json()
    return response['data'][0]['id']

#to get other users's info
def user_info(uname):
    user_id=get_user_id(uname)
    response = requests.get('%susers/%s/?access_token=%s' % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()#other user's url
    if response['meta']['code'] == 200:
        print "Username is %s" % (response['data']['username'])
        print "No of followers are:%s" % (response['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (response['data']['counts']['follows'])
        print 'No. of posts: %s' % (response['data']['counts']['media'])
    else:
        print "Code other than 200 received "

#to get other user's posts
def user_post(username):
    user_id = get_user_id(username)
    response = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL,user_id, APP_ACCESS_TOKEN)).json()
    if response['meta']['code'] == 200:
        pprint(response)#to print info in efficient way
        url = response['data'][0]['images']['standard_resolution']['url']
        name = response['data'][0]['id'] + '.jpg'
        urllib.urlretrieve(url, name)
        print "Image Download complete"
        url=response['data'][0]['videos']['standard_resolution']['url']
        name=response['data'][0]['id'] + '.mp4'#for downlaoding video
        urllib.urlretrieve(url,name)
        print"Video Download complete"
    else:
        print "Code other than 200 received "

#to get media id of any media
def get_media_id(uname):
    user_id = get_user_id(uname)
    response = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
    if response['meta']['code'] == 200:
        return response['data'][0]['id']
    else:
        print "Code other than 200 received "

#to like a post of user
def like_post(uname):
    media_id=get_media_id(uname)
    # two necessary req
    payload={"access_token":APP_ACCESS_TOKEN}#contains data
    url=BASE_URL+'media/%s/likes' %(media_id)#contains url
    response=requests.post(url,payload).json()
    if response['meta']['code']==200:
        print"Your like is done"
    else:
        print("Your like can not done")

#to comment on any post
def comment_post(uname):
    media_id=get_media_id(uname)
    comment=raw_input("What do you want to comment ?")
    payload = {"access_token": APP_ACCESS_TOKEN, "text":comment}#conatains what(text) and from whom(access_token) data has come
    url=BASE_URL+'media/%s/comments' %(media_id)
    response=requests.post(url,payload).json()
    if response['meta']['code']==200:
        print "comment done"
    else:
        print("comment cnt be done")

#to del negative comments
def delete_comment(uname):
    media_id=get_media_id(uname)
    response=requests.get("%smedia/%s/comments?access_token=%s" %(BASE_URL,media_id,APP_ACCESS_TOKEN)).json()
    if response['meta']['code']==200:
        if len(response['data'])>0:#to see if there exists any cmmnts on post or not
            for index in range(0,len(response['data'])):#loop to print cmmnts one by one for a post
                cmnt_id=response['data'][index]['id']
                cmnt_text=response['data'][index]['text']
                blob = TextBlob(cmnt_text, analyzer=NaiveBayesAnalyzer())#analyzing the commnts
                print blob.sentiment#print output of analyzation
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    print "%s"%(cmnt_text)
                    response=requests.delete("%smedia/%s/comments/%s?access_token=%s"%(BASE_URL,media_id,cmnt_id,APP_ACCESS_TOKEN)).json()
                    # url deletes the negative comments
                else:
                    print "%s"%(cmnt_text)
                    print blob.sentiment.p_pos
                    #print postive comnts n probablity
        else:
            print"No comments exits"
    else:
        print"Error"


#func to start instabot to choose from features
def start_bot():
    show_menu=True
    while show_menu:
        menu_choice=input("What do you want to do? 1.Get owner info\n 2.Get owner post\n 3.Get user info\n 4.Get user post\n 5.Like a post\n 6.Comment on a post\n 7.Delete comment\n0.Exit\n")
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
        elif menu_choice==5:
            username = raw_input("Write the name of user from whom you want to fetch data:")
            like_post(username)
        elif menu_choice==6:
            username = raw_input("Write the name of user from whom you want to fetch data:")
            comment_post(username)
        elif menu_choice==7:
            username = raw_input("Write the name of user from whom you want to fetch data:")
            delete_comment(username)
        elif menu_choice==0:
            show_menu=False
        else:
            print "Invalid Choice "

start_bot()
#calling the func