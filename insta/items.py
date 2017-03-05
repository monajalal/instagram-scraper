import scrapy
from scrapy.item import Item, Field

class UserItem(Item):    
    '''
    username = Field()
    follows_count = Field()
    followed_by_count = Field()
    is_verified = Field()
    biography = Field()
    external_link = Field()
    full_name = Field()
    posts_count = Field()
    posts = Field()
    '''
    pass

class PostItem(Item):
    '''
    code = Field()
    likes = Field()
    thumbnail = Field()
    caption = Field()
    hashtags = Field()
    '''
    pass
