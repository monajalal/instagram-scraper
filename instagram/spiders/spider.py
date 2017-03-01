import scrapy
print(scrapy.__file__)
import json
from instagram.items import UserItem
from instagram.items import PostItem
from scrapy.spider import BaseSpider as Spider

class InstagramSpider(Spider):

    name = 'instagramspider'
    allowed_domains = ['instagram.com']
    start_urls = []

    def __init__(self):
        self.start_urls = ["https://www.instagram.com/_spataru/?__a=1"]

    def parse(self, response):
        #get the json file
        json_response = {}
        try:
            json_response = json.loads(response.body_as_unicode())
        except:
            self.logger.info('%s doesnt exist', response.url)
            pass
        if json_response["user"]["is_private"]:
            return;
        #check if the username even worked
        try:
            json_response = json_response["user"]

            item = UserItem()

            #get User Info
            item["username"] = json_response["username"]
            item["follows_count"] = json_response["follows"]["count"]
            item["followed_by_count"] = json_response["followed_by"]["count"]
            item["is_verified"] = json_response["is_verified"]
            item["biography"] = json_response.get("biography")
            item["external_link"] = json_response.get("external_url")
            item["full_name"] = json_response.get("full_name")
            item["posts_count"] = json_response.get("media").get("count")

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
            self.logger.info("Error during parsing %s", response.url)
