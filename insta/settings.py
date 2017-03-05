# Scrapy settings for instagram project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'insta'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['insta.spiders']
NEWSPIDER_MODULE = 'insta.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

