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
#
#     https://spidermon.readthedocs.io/


REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
SPIDERMON_ENABLED = False

# TODO: Re-enable after fixing to be aware of different spiders.
# SPIDERMON_SPIDER_CLOSE_MONITORS = ("public_law.monitors.SpiderCloseMonitorSuite",)

BOT_NAME = "public_law"
SPIDER_MODULES = ["public_law.spiders"]
NEWSPIDER_MODULE = "public_law.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "..."
ROBOTSTXT_OBEY = True


# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5

#
# Crawlera Best Practices.
#

DOWNLOAD_TIMEOUT = 600

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 4

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False
# TELNETCONSOLE_USERNAME = ...
# TELNETCONSOLE_PASSWORD = ...

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'public_law.middlewares.OarSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #   'public_law.middlewares.OarDownloaderMiddleware': 543,
    "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 1,
    'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610,
}

ZYTE_SMARTPROXY_ENABLED = True
VAR = "ZYTE_SMARTPROXY_APIKEY"
if VAR in os.environ:
    ZYTE_SMARTPROXY_APIKEY = os.environ[VAR]
ZYTE_SMARTPROXY_URL = "http://api.zyte.com:8011"

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }
EXTENSIONS = {
    # "spidermon.contrib.scrapy.extensions.Spidermon": 500,
}


# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {"public_law.pipelines.OarPipeline": 300}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.25
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 4
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


#
# In development mode only, set the sensitive and environment-
# dependent configuration values via env  variables. On development
# machines, set `SCRAPY_DEVELOPMENT_MODE` to make this work. This
# isn't necessary, however, to develop and run the spiders.
#
if "PUBLAW_SCRAPY_DEVELOPMENT_MODE" in os.environ:
    SPIDERMON_TELEGRAM_SENDER_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    SPIDERMON_TELEGRAM_RECIPIENTS = os.environ["TELEGRAM_BOT_GROUP_ID"]
    LOG_LEVEL = os.environ["PUBLAW_SCRAPY_LOG_LEVEL"]
    USER_AGENT = os.environ["PUBLAW_SCRAPY_USER_AGENT"]
