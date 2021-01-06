# Scrapy settings for hse project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'hse'

SPIDER_MODULES = ['hse.spiders']
NEWSPIDER_MODULE = 'hse.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64)'
# USER_AGENT = 'Alexander, bac03704@gmail.com'

# SPIDERMON_ENABLED = True

# AUTOUNIT_ENABLED = True

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# DB connection path
CONNECTION_STRING = 'sqlite:///app/posts.db'

# Logging level
LOG_LEVEL = "INFO"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 5

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16
# CONCURRENT_REQUESTS_PER_IP = 4

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # 'hse.middlewares.HseSpiderMiddleware': 543,
   'scrapy_autounit.AutounitMiddleware': 950
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    # 'hse.middlewares.HseDownloaderMiddleware': 543,
# }

# ROTATING_PROXY_LIST_PATH = 'proxies.txt' # Path that this library uses to store list of proxies
# NUMBER_OF_PROXIES_TO_FETCH = 5 # Controls how many proxies to use
#
#
# DOWNLOADER_MIDDLEWARES = {
#     'rotating_free_proxies.middlewares.RotatingProxyMiddleware': 610,
#     'rotating_free_proxies.middlewares.BanDetectionMiddleware': 620,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'spidermon.contrib.scrapy.extensions.Spidermon': 500
#    # 'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
ITEM_PIPELINES = {
   # 'hse.pipelines.DefaultValuesPipeline': 100,
   'hse.pipelines.DuplicatesPipeline': 200,
   'hse.pipelines.EmptyPostsPipeline': 300,
   'spidermon.contrib.scrapy.pipelines.ItemValidationPipeline': 400,
   'hse.pipelines.SavePostsPipeline': 500,
}

SPIDERMON_VALIDATION_MODELS = (
    'hse.validators.PostItem',
)

# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
