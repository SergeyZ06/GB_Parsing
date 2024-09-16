BOT_NAME = 'GB_parsing'

SPIDER_MODULES = ['GB_parsing.spiders']
NEWSPIDER_MODULE = 'GB_parsing.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.2; rv:59.0) Gecko/20100101 Firefox/59.0'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {'GB_parsing.pipelines.GbParsingPipeline': 1,
                  'GB_parsing.pipelines.MyImagesPipeline': 1}

DOWNLOAD_DELAY = 2
IMAGES_STORE = 'images'

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'log.txt'
