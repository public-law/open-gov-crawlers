# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class OarPipeline:
    def process_item(self, item, _spider):  # type: ignore
        return item  # type: ignore
