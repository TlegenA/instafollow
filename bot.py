from time import sleep
from InstagramAPI import InstagramAPI
from random import seed
from random import sample
from random import shuffle
from random import randint


api = InstagramAPI(instagram_login, instagram_password)
api.login()

users_list = []
following_users = []
follower_users = []
my_followers = []
my_foll_followers = []

def get_my_profile_details():
    api.login() 
    api.getSelfUsernameInfo()
    result = api.LastJson
    username = result['user']['username']
    full_name = result['user']['full_name']
    profile_pic_url = result['user']['profile_pic_url']
    followers = result['user']['follower_count']
    following = result['user']['following_count']
    media_count = result['user']['media_count']

def get_my_acc_name():
    api.getSelfUsernameInfo()
    result = api.LastJson
    username = result['user']['username']
    return username

def get_my_feed():
    image_urls = []
    api.login()
    api.getSelfUserFeed()
    result = api.LastJson
    # formatted_json_str = pprint.pformat(result)
    # print(formatted_json_str)
    if 'items' in result.keys():
        for item in result['items'][0:5]:
            if 'image_versions2' in item.keys():
                image_url = item['image_versions2']['candidates'][1]['url']
                image_urls.append(image_url)




def get_likes_list(username):
    api.login()
    api.searchUsername(username)
    result = api.LastJson
    username_id = result['user']['pk'] # Get user ID
    user_posts = api.getUserFeed(username_id) # Get user feed
    result = api.LastJson
    media_id = result['items'][0]['id'] # Get most recent post
    api.getMediaLikers(media_id) # Get users who liked
    users = api.LastJson['users']
    for user in users: # Push users to list
        users_list.append({'pk':user['pk'], 'username':user['username']})
    print(users_list) 
    follow_users(users_list)  


def follow_users(users_list):
    api.login()
    api.getSelfUsersFollowing() # Get users which you are following
    result = api.LastJson
    for user in result['users']:
        following_users.append(user['pk'])
    for user in users_list:
        if not user['pk'] in following_users: # if new user is not in your following users                   
            print('Following @' + user['username'])
            #api.follow(user['pk'])
            # after first test set this really long to avoid from suspension
            sleep(20)
        else:
            print('Already following @' + user['username'])
            sleep(10)


def unfollow_users():
    #api.login()
    api.getSelfUserFollowers() # Get your followers
    result = api.LastJson
    for user in result['users']:
        follower_users.append({'pk':user['pk'], 'username':user['username']})
    followers = dict((i['pk'], i['username']) for i in follower_users)
    api.getSelfUsersFollowing() # Get users which you are following
    result = api.LastJson
    for user in result['users']:
        following_users.append({'pk':user['pk'],'username':user['username']})
    #print(following_users)
        
    for user in following_users:
        if not user['pk'] in followers: # if the user not follows you
            print('Unfollowing @' + user['username'])
            api.unfollow(user['pk'])
            # set this really long to avoid from suspension
            sleep(20) 

def isprivate_account(userid):
    #api.login()
    username_info = api.getUsernameInfo(userid)
    sleep(randint(4, 9))
    is_private = api.LastJson
    return(is_private['user']['is_private'])

def isbusiness_account(userid):
    username_info = api.getUsernameInfo(userid)
    is_bisiness = api.LastJson
    sleep(randint(4, 9))
    #print('username ' + user['username'] + ' business account : {}'.format(is_bisiness['user']['is_business']))
    return(is_bisiness['user']['is_business'])

def like_and_follow():
    api.getSelfUserFollowers() # Get users which you are following
    result = api.LastJson
    for user in result['users']:
        my_followers.append({'pk':user['pk'],'username':user['username']})

    shuffle(my_followers) # перемещиваем список
    api.getSelfUserFollowers() # Get your followers
    result = api.LastJson
    for user in result['users']:
        follower_users.append({'pk':user['pk'], 'username':user['username']})
    followers = dict((i['pk'], i['username']) for i in follower_users)
    count_foll_followers = 0
    for user in my_followers:
        print(' Начинаем работать с подписчиками пользователя: '+ user['username'])
        api.getUserFollowers(user['pk'])
        result = api.LastJson
        sleep(randint(8, 20))
        count_foll_followers = len(result['users'])
        counter = len(result['users'])
        print('Количество подписчиков: ' + str(count_foll_followers))
        for item in result['users']:
            if (not isprivate_account(item['pk']) and item['pk'] not in followers and item['username'] != get_my_acc_name()):
                print(item['username'])
                my_foll_followers.append({'pk':item['pk'],'username':item['username']})
                sleep(randint(4, 9))
                print('Счетчик: ' + str(counter))
                if(int(counter) % 3 == 0): # выбираем каждого 3го
                    user_posts = api.getUserFeed(item['pk']) # Get user feed
                    result = api.LastJson
                    print('У пользователя ' + str(len(result['items'])) + ' постов')
                    if len(result['items'])>2:
                        media_id0 = result['items'][0]['id'] # Get most recent post
                        #print(media_id0)
                        media_id1 = result['items'][1]['id'] # Get most recent post
                        print('Ставим лайки на последние 2 фото пользователю: ' + item['username'])
                        api.like(media_id0) # лайк на последнюю публикацию
                        sleep(randint(6, 15))
                        api.like(media_id1) # лайк на предпоследнюю публикацию
                        # sleep(randint(20, 30))
                        # print('Подписываемся на пользователя: ' + item['username'])
                        # api.follow(item['pk']) # подписываемся на пользователя
                        sleep(randint(9, 20))
                counter = counter - 1    
def main():  
    #get_my_profile_details()
    #unfollow_users()
    
    #api.login()
    #unfollow_users()
    like_and_follow()
    

if __name__ == '__main__':  
    main()  