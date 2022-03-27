## IMPORTS ##
import os
import sys
import subprocess
import json
import time

try:
    import tweepy as tp
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'tweepy'])
finally:
    import tweepy as tp

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])
finally:
    import requests
## EXTRAS ##

## CLEAR ##
def clear():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

## P == PRINT ##
def p(val=None):
    if val == None:
        print()
    else:
        print(val)

## PRINT + PREFIX ##
def p_p(val=None):
    if val == None:
        print(prefix)
    else:
        print(prefix + val)

## PRINT NONE ##
def space():
    print()

## Prints enter text and puts a blank input ##
def enter():
    space()
    p('(Press enter to continue)')
    input()

## Checks if any of the keys are none
def checkKey():
    clear()
    if consumer_key == "None" or consumer_secret == "None" or access_token == "None" or access_token_secret == "None" or consumer_key == None or consumer_secret == None or access_token == None or access_token_secret == None:
        msg = 'One or more keys arent set, please get keys from dev.twitter.com for the account you want the program to use, and then set them with [PREFIX]key[set].'.replace('[PREFIX]', prefix)
        p(msg)
        enter()
        main()
## Create Folder and data in folder ##
filename = os.path.join(os.getcwd(), 'data/help.txt')
filename2 = os.path.join(os.getcwd(), 'data/data.json')
if not os.path.exists("data"):
    os.mkdir("data")
    url = "https://raw.githubusercontent.com/tetradev/TweetDEV/master/help.txt"
    r = requests.get(url)
    f = open(filename, 'wb')
    f.write(r.content)
    f.close()
    with open(filename2, 'wb') as f2:
        f2.write('{}')
        f2.close()

## Fail safe if help.txt is modified, then it'll overwrite the file ##
with open('data/help.txt', 'wb') as file:
    r = requests.get("https://raw.githubusercontent.com/tetradev/TweetDEV/master/data/help.txt")
    if not r == open('data/help.txt', 'r').read():
        file.write(r.content)
        file.close()

## Fail safe for json files if any data gets removed ##
def jadd(item, amt, fname='data'):
    with open("data/"+fname+".json", 'r+') as file:
        if item not in json.loads(open("data/"+fname + ".json", 'r').read()):
            dat = {item: amt}
            data = json.load(file)
            data.update(dat)
            file.seek(0)
            json.dump(data, file)
            file.close()
jadd('version', 'OVERRIDE')
jadd('prefix', '--')
jadd('consumer_key', 'None')
jadd('consumer_secret', 'None')
jadd('access_token', 'None')
jadd('access_token_secret', 'None')
## GLOBAL VARS ##
vnum = "1.0.0t"
with open(filename2, 'r') as f:
    update = json.load(f)
    update["version"] = vnum  # or whatever
    f.close()
with open(filename2, "w") as f:
    json.dump(update, f)
    f.close()
data = json.loads(open(filename2, 'r+').read())
prefix = data['prefix']
consumer_key = data['consumer_key']
consumer_secret = data['consumer_secret']
access_token = data['access_token']
access_token_secret = data['access_token_secret']
version = data['version']
## Main loop ##
def main():
    global prefix
    global consumer_key
    global consumer_secret
    global access_token
    global access_token_secret
    auth = tp.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tp.API(auth)
    clear()
    p('Version: '+version)
    space()
    p_p('help for cmds')
    space()
    inp = input()
    
    if prefix+'help' == inp:
        clear()
        help = open("data/help.txt","r").read().replace('[PREFIX]', prefix)
        p(help)
        enter()
    
    if prefix+'prefix' in inp:
        if "[" in inp and "]" in inp:
            if "set" in inp:
                new_prefix = input("New Prefix: ")
                if new_prefix == "default":
                    new_prefix = '--'
                prefix = new_prefix
                with open(filename2, 'r') as f:
                    update = json.load(f)
                    update["prefix"] = prefix  # or whatever
                with open(filename2, "w") as f:
                    json.dump(update, f)
                enter()
                return
        p('Prefix: '+prefix)
        enter()
    
    if prefix+'key' in inp:
        if "[" in inp and "]" in inp:
            if "set" in inp:
                clear()
                p('(Leave blank to keep it the same)')
                new_consumer_key = input('New Consumer Key: ')
                new_consumer_secret = input('New Consumer Secret: ')
                new_access_token = input('New Access Token: ')
                new_access_token_secret = input('New Access Token Secret: ')

                if new_consumer_key == '':
                    new_consumer_key = consumer_key

                if new_consumer_secret == '':
                    new_consumer_secret = consumer_secret

                if new_access_token == '':
                    new_access_token = access_token

                if new_access_token_secret == '':
                    new_access_token_secret = access_token_secret

                consumer_key = new_consumer_key
                consumer_secret = new_consumer_secret
                access_token = new_access_token
                access_token_secret = new_access_token_secret
                enter()
                with open(filename2, 'r') as f:
                    update = json.load(f)
                    update["consumer_key"] = consumer_key
                    update["consumer_secret"] = consumer_secret
                    update["access_token"] = access_token
                    update["access_token_secret"] = access_token_secret
                with open(filename2, "w") as f:
                    json.dump(update, f)
                return
        p('Consumer Key: '+consumer_key)
        p('Consumer Secret: '+consumer_secret)
        p('Access Token: '+access_token)
        p('Access Token Secret: '+access_token_secret)
        enter()
    
    if prefix+'check_key' == inp:
        checkKey()

    if prefix+'get_user' == inp:
        clear()
        checkKey()
        name = input("Username: @")
        if name == '':
            p('Invalid Username')
            return
        user = api.get_user(screen_name=name)
        clear()
        p('ID: '+str(user.id))
        p('Username: @'+user.screen_name)
        enter()
    
    if prefix+'get_settings' == inp:
        clear()
        checkKey()
        p('JSON: '+str(api.get_settings()))
        space()
        p('Protected: '+str(api.get_settings()['protected']))
        p('Username: '+str(api.get_settings()['screen_name']))
        p('Always Use HTTPS: '+str(api.get_settings()['always_use_https']))
        p('Use Cookie Personalization: '+str(api.get_settings()['use_cookie_personalization']))
        p('Sleep Time Enabled: '+str(api.get_settings()['sleep_time']['enabled']))
        p('Sleep Time End Time: '+str(api.get_settings()['sleep_time']['end_time']))
        p('Sleep Time Start Time: '+str(api.get_settings()['sleep_time']['start_time']))
        p('Geo Enabled: '+str(api.get_settings()['geo_enabled']))
        p('Language: '+str(api.get_settings()['language']))
        p('Discoverable By Email: '+str(api.get_settings()['discoverable_by_email']))
        p('Discoverable By Phone: '+str(api.get_settings()['discoverable_by_mobile_phone']))
        p('Display Sensitive Media: '+str(api.get_settings()['display_sensitive_media']))
        p('Allow Contributor Request: '+str(api.get_settings()['allow_contributor_request']))
        p('Allow Dms From: '+str(api.get_settings()['allow_dms_from']))
        p('Allow Dm Groups From: '+str(api.get_settings()['allow_dm_groups_from']))
        p('Translator Type: '+str(api.get_settings()['translator_type']))
        enter()

    if prefix+'get_banner' == inp:
        clear()
        checkKey()
        name = input("Username: @")
        if name == '':
            p('Invalid Username')
            return
        clear()
        banner = api.get_profile_banner(screen_name=name)
        p('JSON: '+str(banner))
        space()
        p('Banners:')
        p('IPad: '+str(banner['sizes']['ipad']['url']))
        p('IPad Retina: '+str(banner['sizes']['ipad_retina']['url']))
        p('Web: '+str(banner['sizes']['web']['url']))
        p('Web Retina: '+str(banner['sizes']['web_retina']['url']))
        p('Mobile: '+str(banner['sizes']['mobile']['url']))
        p('Mobile Retina: '+str(banner['sizes']['mobile_retina']['url']))
        p('300x100: '+str(banner['sizes']['300x100']['url']))
        p('600x200: '+str(banner['sizes']['600x200']['url']))
        p('1500x500: '+str(banner['sizes']['1500x500']['url']))
        p('1080x360: '+str(banner['sizes']['1080x360']['url']))
        enter()

    if prefix+'tweet' == inp:
        clear()
        checkKey()
        text = input("Text to Tweet: ")
        rus = input('Are you sure (Y/n): ')
        clear()
        if rus == 'Y' or rus == 'y':
            api.update_status(status=text)
            p('Tweet Sent!: "'+text+'"')
        else:
            p('Not posting: "'+text+'"')
        enter()
    
    if prefix+'retweet' == inp:
        clear()
        checkKey()
        id = input("ID of tweet to retweet: ")
        rus = input('Are you sure (Y/n): ')
        clear()
        if rus == 'Y' or rus == 'y':
            api.retweet(id=id)
            p('Retweeted Post: '+str(id))
        else:
            p('Not Retweeting Post: '+str(id))
        enter()

    if prefix+'unretweet' == inp:
        clear()
        checkKey()
        id = input("ID of tweet to unretweet: ")
        rus = input('Are you sure (Y/n): ')
        clear()
        if rus == 'Y' or rus == 'y':
            api.unretweet(id=id)
            p('Unretweeted Post: '+str(id))
        else:
            p('Not Unretweeting Post: '+str(id))
        enter()

while True:
    main()