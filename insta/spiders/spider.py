import inspect
import scrapy
print(scrapy.__file__)
import json
import requests
from insta.items import UserItem
from insta.items import PostItem
from scrapy.spider import BaseSpider as Spider
from pprint import pprint
import csv
from instagram import client, subscriptions

'''
client_id = '7c1a0e1ecde747508933150a13da8603'
client_secret = '5cc0e027b447486e90a954bd72501e61'
redirect_uri = 'http://localhost:8515/oauth_callback'
#access_token='53112486.7c1a0e1.02ecaa1b8c9d4910a480b7fd77d2e3c7'
code ='adb646dd3517447fb3606b1593d858a7'
'''
#user_id='53112486'



class InstagramSpider(Spider):

    name = 'instagramspider'
    allowed_domains = ['instagram.com']
    start_urls = []

    def __init__(self):
        #self.start_urls = ["https://www.instagram.com/_spataru/?__a=1"]
        #self.start_urls = ["https://www.instagram.com/mona_of_green_gables/?__a=1"]
        #self.start_urls = ["https://www.instagram.com/ducks_love_sun/?__a=1"]
        self.start_urls = ["https://www.instagram.com/buzzfeed/?__a=1"]
        #self.start_urls = ["https://www.instagram.com/mona_of_green_gables/?__a=1"]
    def parse(self, response):
        
        url = u'https://api.instagram.com/oauth/access_token'
        client_id = '7c1a0e1ecde747508933150a13da8603'
        client_secret = '5cc0e027b447486e90a954bd72501e61'
        redirect_uri = 'http://localhost:8515/oauth_callback'
        access_token='53112486.7c1a0e1.02ecaa1b8c9d4910a480b7fd77d2e3c7'
        code ='e7e9dc1396b142a8a25bebf7e241c4ee'
        '''
        data = { 
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }

        response = requests.post(url, data=data)
        account_info = json.loads(response.content)
        #print account_info[0]
        #print str(account_info[0])
        pprint(account_info)
        '''
        #api = client.InstagramAPI(access_token=access_token)


        json_response = {}

        try:
            
            #api = client.InstagramAPI(access_token=access_token)
            
            #followers = []

            #pprint(api_user_recent_media(user_id=53112486, count=3))
            #pprint(api.user_followed_by(user_id=53112486))

            '''
            for p in api.user_followed_by(user_id=user_id, as_generator=True, max_pages=None):
                followers.extend(p[0])

            followers = [str(u).replace('User: ','') for u in followers]

            print len(followers), 'followers'
            print followers
            '''
            json_response = json.loads(response.body_as_unicode())
            #pprint(json_response)
            #pprint(json_response["user"])
            #print(json_response["user"]["follows"])
            #print json.dumps(json_response["user"]["media"]["nodes"][1]["comments"][1], indent=4, sort_keys=True)
            #print json.dumps(json_response["user"]["media"]["nodes"][1]["code"], indent=4, sort_keys=True)
            img_code = json_response["user"]["media"]["nodes"][1]["code"]
            img_url = 'https://www.instagram.com/p/'+ img_code + '/?__a=1'
            print(img_url)
            img_response = json.loads(requests.get(img_url).text)
            #pprint(img_response)
            #pprint(img_response["media"]["likes"].items())
            comment_count = 0
            #end_cursors = []
            image_comments = img_response
            print image_comments["media"]["comments"]["nodes"][1]["text"]
            while image_comments["media"]["comments"]["page_info"]["has_next_page"]:
                end_cursor = image_comments["media"]["comments"]["page_info"]["end_cursor"]
                print(end_cursor)
                image_comments = requests.get(img_url+"&max_id="+end_cursor).json()
                #pprint(image_comments)
                print(len(image_comments["media"]["comments"]["nodes"]))
                for i in range(len(image_comments["media"]["comments"]["nodes"])):
                    comment_count = comment_count + 1
                    print image_comments["media"]["comments"]["nodes"][i]["text"], comment_count
                end_cursor = ""
                '''
        
            for attribute, value in img_response["media"]["comments"]["nodes"].iteritems():
                print attribute, value
            '''
            print("*********************************")
            #end_cursors = []
            media_data = json_response["user"]["media"]
            has_next_page = media_data["page_info"]
            #data = json.loads(requests.get("https://www.instagram.com/buzzfeed/?__a=1").text)
            count = 0
            '''
            while data["user"]["media"]["page_info"]["has_next_page"]:
                end_cursors.append(data["user"]["media"]["page_info"]["end_cursor"])
                data = json.loads(requests.get('https://www.instagram.com/ducks_love_sun/?__a=1&max_id={}'.format(end_cursors[-1])).text)
                #pprint(data)
                
                for i in range(len(json_response["user"]["media"]["nodes"])):
                    count = count + 1
                    print json_response["user"]["media"]["nodes"][i]["likes"]["count"], count

                    #pprint(data)
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            ://www.instagram.com/p/'+ img_code + '/?__a=1'rint("8888888888888888888888888888888")
            '''
            media_count = json_response["user"]["media"]["count"]
            #for i in range(media_count):
            #    print media_data["nodes"][i]["comments"]["count"]#, nodes_data[i]["likes"]["count"], nodes_data[i]["display_src"]

        except:
            #self.logger.info('%s doesnt exist', response.url)
            print("hello")
            #pass
        if json_response["user"]["is_private"]:
            return;
        #check if the username even worked
        try:
            json_response = json_response["user"]

            item = UserItem()
            
            #test_file = open('test.csv', 'wb')

            #get User Info
            item["username"] = json_response["username"]
            item["follows_count"] = json_response["follows"]["count"]
            item["followed_by_count"] = json_response["followed_by"]["count"]
            item["is_verified"] = json_response["is_verified"]
            item["biography"] = json_response.get("biography")
            item["external_link"] = json_response.get("external_url")
            item["full_name"] = json_response.get("full_name")
            item["posts_count"] = json_response.get("media").get("count")
            
            #writer = csv.write(test_file, delimiter=",")
            #row = (json_response["username"], json_response.get("biography"))
            #writer.writerow(row)
            #test_file.close()


            #interate through each post
            item["posts"] = []

            json_response = json_response.get("media").get("nodes")
            if json_response:
                for post in json_response:
                    items_post = PostItem()
                    items_post["code"]=post["code"]
                    items_post["likes"]=post["likes"]["count"]
                    items_post["caption"]=post["caption"]
                    items_post["thumbnail"]=post["thumbnail_src"]
                    item["posts"].append(dict(items_post))

            return item
        except:
            pass
            #self.logger.info("Error during parsing %s", response.url)
