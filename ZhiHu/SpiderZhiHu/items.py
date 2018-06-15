# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Spider_zhihuParentTopic_Item(scrapy.Item):

    #父话题ID
    parent_topic_id=scrapy.Field()

    #父话题名称
    parent_topic_name=scrapy.Field()


class Spider_zhihuSubTopic_Item(scrapy.Item):

    # 子话题ID
    sub_topic_id = scrapy.Field()

    # 子话题名称
    sub_topic_name = scrapy.Field()

    # 子话题链接
    sub_topic_link = scrapy.Field()

    # 子话题描述
    sub_topic_description = scrapy.Field()

    # 关联的父话题ID
    parent_topic_id = scrapy.Field()
