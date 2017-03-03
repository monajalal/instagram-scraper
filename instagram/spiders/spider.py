import scrapy
print(scrapy.__file__)
import json
import requests
from instagram.items import UserItem
from instagram.items import PostItem
from scrapy.spider import BaseSpider as Spider
from pprint import pprint
import csv

class InstagramSpider(Spider):

    name = 'instagramspider'
    allowed_domains = ['instagram.com']
    start_urls = []

    def __init__(self):
        #self.start_urls = ["https://www.instagram.com/_spataru/?__a=1"]
        #self.start_urls = ["https://www.instagram.com/mona_of_green_gables/?__a=1"]
        self.start_urls = ["https://www.instagram.com/ducks_love_sun/?__a=1"]
    def parse(self, response):
        #get the json file
        json_response = {}
        try:
            json_response = json.loads(response.body_as_unicode())
            #pprint(json_response)
            print("monamona")
            #print(json_response["user"]["follows"])
            #print json.dumps(json_response["user"]["media"]["nodes"][1]["comments"][1], indent=4, sort_keys=True)
            #print json.dumps(json_response["user"]["media"]["nodes"][1]["code"], indent=4, sort_keys=True)
            code = json_response["user"]["media"]["nodes"][1]["code"]
            
            sub_post_url = "https://www.instagram.com/p/"+code+"/?__a=1"
            print(sub_post_url)
            sub_response = requests.get(sub_post_url).json()
            #pprint(sub_response)
            '''
            for i in range(len(sub_response["media"]["comments"]["nodes"])):
                print(sub_response["media"]["comments"]["nodes"][i]["text"])
            sub_json_data = json.loads(sub_response.body_as_unicode())
            #print("))))))((((((")
            #pprint(sub_json_data)
            #print json.dumps(sub_json_data, indent=4, sort_keys=True)
            '''
            print("*********************************")
            end_cursors = []
            media_data = json_response["user"]["media"]
            has_next_page = media_data["page_info"]
            data = json.loads(requests.get("https://www.instagram.com/ducks_love_sun/?__a=1").text)
            #pprint(data)
            count = 0
            while data["user"]["media"]["page_info"]["has_next_page"]:
                end_cursors.append(data["user"]["media"]["page_info"]["end_cursor"])
                data = json.loads(requests.get('https://www.instagram.com/ducks_love_sun/?__a=1&max_id={}'.format(end_cursors[-1])).text)
                #pprint(data)
                
                for i in range(len(json_response["user"]["media"]["nodes"])):
                    count = count + 1
                    print json_response["user"]["media"]["nodes"][i]["likes"]["count"], count

                    #pprint(data)
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            
            #pprint(has_next_page)
            #print(len(nodes_data))

            #pprint(nodes_data)
            media_count = json_response["user"]["media"]["count"]
            #for i in range(len(nodes_data)):
            print media_data["nodes"][10]["comments"]["count"]
            print("8888888888888888888888888888888")
            #for i in range(media_count):
            #    print media_data["nodes"][i]["comments"]["count"]#, nodes_data[i]["likes"]["count"], nodes_data[i]["display_src"]
            print("8888888888888888888888888888888")

        except:
            #self.logger.info('%s doesnt exist', response.url)
            
            pass
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
