# -*- coding: utf-8 -*-
import os

# Scrapy settings for oar project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

LOG_LEVEL = "INFO"

BOT_NAME = "oar"
SPIDER_MODULES = ["oar.spiders"]
NEWSPIDER_MODULE = "oar.spiders"


# Output the JSON tree as one simple JSON object.
FEED_FORMAT = "jsonlines"
FEED_URI = "stdout:"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Public.Law Parser (https://www.public.law/contact-us)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5

#
# Crawlera Best Practices. Current Plan is "C50".
#

DOWNLOAD_TIMEOUT = 600

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 5

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 3

# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True
TELNETCONSOLE_USERNAME = 'scrapy'
TELNETCONSOLE_PASSWORD = 'scrapy'

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'oar.middlewares.OarSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #   'oar.middlewares.OarDownloaderMiddleware': 543,
    "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 1,
    'scrapy_crawlera.CrawleraMiddleware': 610
}

CRAWLERA_ENABLED = True

# This breaks on Scraping Hub although it works locally. Commenting it out
# for now.
# CRAWLERA_APIKEY = os.environ['CRAWLERA_APIKEY']

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {"oar.pipelines.OarPipeline": 300}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 3.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# Enabled for development:
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"
# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.DummyPolicy"
