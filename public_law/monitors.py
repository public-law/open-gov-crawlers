# from spidermon import Monitor, MonitorSuite, monitors
# from spidermon.contrib.actions.telegram.notifiers import (
#     SendTelegramMessageSpiderFinished,
# )
# from public_law.spiders.ca.doj_glossaries import DojGlossaries


# @monitors.name("Item count")
# class ItemCountMonitor(Monitor):
#     minimum_threshold = len(DojGlossaries.start_urls)

#     @monitors.name(f"Minimum number of items ({minimum_threshold})")
#     def test_minimum_number_of_items(self):
#         item_scraped_count = getattr(self.data.stats, "item_scraped_count", 0)

#         self.assertGreaterEqual(
#             item_scraped_count,
#             self.minimum_threshold,
#         )


# class SpiderCloseMonitorSuite(MonitorSuite):

#     monitors = [
#         ItemCountMonitor,
#     ]

#     monitors_failed_actions = [SendTelegramMessageSpiderFinished]
