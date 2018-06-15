# -*- coding: utf-8 -*-
import scrapy
import re
import json
from SpiderZhiHu.items import Spider_zhihuParentTopic_Item,Spider_zhihuSubTopic_Item


class Spiderman001Spider(scrapy.Spider):

    name = 'Spiderman001'


    def start_requests(self):

        topics_url = 'https://www.zhihu.com/topics'

        yield scrapy.Request(url=topics_url,callback=self.parse_parent_topic)


    def parse_parent_topic(self,response):

        parent_item=Spider_zhihuParentTopic_Item()

        html = response.text

        topic_list = re.findall('<li class="zm-topic-cat-item"(.*?)</li>', html, re.S)

        for topic in topic_list:

            parent_item['parent_topic_name'] = re.findall('<a href=".*?>(.*?)<', topic, re.S)[0]

            parent_item['parent_topic_id'] = re.findall('data-id="(.*?)"', topic, re.S)[0]

            print("Get ParentTopic Success")

            yield parent_item

            sub_data_url = 'https://www.zhihu.com/node/TopicsPlazzaListV2'

            for offset in range(0, 500, 20):

                post_data = {'method': 'next', 'params': '{"topic_id":%s,"offset":%s,"hash_id":""}'%(parent_item['parent_topic_id'],offset)}

                yield scrapy.FormRequest(url=sub_data_url,meta={'id':parent_item['parent_topic_id']},formdata=post_data,callback=self.parse_sub_topic)


    def parse_sub_topic(self,response):

        #初始化item
        sub_item=Spider_zhihuSubTopic_Item()

        #响应数据
        html=response.text

        #获取上一层的父分类ID
        parent_topic_id=response.meta['id']

        #数据转换
        sub_list = json.loads(html)['msg']

        #判断数据是否为空
        if len(sub_list) > 0:

            print("\n")

            print("Start Crawl")

            #遍历提取数据
            for sub in sub_list:

                #子分类名称
                sub_item['sub_topic_name'] = re.findall('<strong>(.*?)</strong>', sub, re.S)[0]

                # 子分类链接
                sub_item['sub_topic_link'] = "https://www.zhihu.com" + re.findall('href="(.*?)"', sub, re.S)[0]

                #子分类名称ID
                sub_item['sub_topic_id'] = re.findall('href="/topic/(.*?)"', sub, re.S)[0]

                # 子分类描述
                sub_item['sub_topic_description'] = re.findall('<p>(.*?)</p>', sub, re.S)[0]

                # 关联父分类ID
                sub_item['parent_topic_id']=parent_topic_id

                #判断描述是否为空
                if sub_item['sub_topic_description'] == '':

                    sub_item['sub_topic_description'] = '无话题描述'

                else:

                    sub_item['sub_topic_description'] = sub_item['sub_topic_description']


                print("Get SubTopic Success")

                yield sub_item

                #print("子分类话题:{},子分类话题链接:{},子分类话题ID:{},子分类话题描述:{},关联父分类ID:{}".format(sub_item['sub_topic_name'], sub_item['sub_topic_link'], sub_item['sub_topic_id'], sub_item['sub_topic_description'],sub_item['parent_topic_id']))

            print("\n")

        else:

            print("获取Over")



