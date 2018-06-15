# -*- coding: utf-8 -*-

import re
import json

import requests

class GetTopic:

    def __init__(self):

        self.topics_data=[]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'x-xsrftoken': 'b2a24326-6987-4c07-9652-07d10814c696'
        }


    def get_parent_data(self):

        topics_url='https://www.zhihu.com/topics'

        response=requests.get(topics_url,headers=self.headers)

        html=response.text

        topic_list=re.findall('<li class="zm-topic-cat-item"(.*?)</li>',html,re.S)

        for topic in topic_list:

            topic_name=re.findall('<a href=".*?>(.*?)<',topic,re.S)[0]

            topic_id=re.findall('data-id="(.*?)"',topic,re.S)[0]

            self.topics_data.append({topic_id:topic_name})


    def get_sub_data(self):

        for topic in self.topics_data:

            for topic_id in topic:

                for offset in range(0,1000,20):

                    url = 'https://www.zhihu.com/node/TopicsPlazzaListV2'

                    data = {'method': 'next', 'params': '{"topic_id":%s,"offset":%s,"hash_id":""}'%(topic_id,offset)}

                    response = requests.post(url, headers=self.headers, data=data)

                    sub_list = json.loads(response.text)['msg']

                    if len(sub_list) > 0:

                        print("存在数据,继续爬取")

                        for sub in sub_list:

                            sub_name = re.findall('<strong>(.*?)</strong>', sub, re.S)[0]

                            sub_link = "https://www.zhihu.com"+re.findall('href="(.*?)"', sub, re.S)[0]

                            sub_id = re.findall('href="/topic/(.*?)"', sub, re.S)[0]

                            sub_description = re.findall('<p>(.*?)</p>', sub, re.S)[0]

                            if sub_description == '':

                                sub_description = '无话题描述'

                            else:

                                sub_description = sub_description

                            with open("all_topics.txt", "a",encoding='utf8') as f:

                                f.write("子分类话题:{},子分类话题链接:{},子分类话题ID:{},子分类话题描述:{}".format(sub_name, sub_link, sub_id,sub_description) + "\n")

                            print("子分类话题:{},子分类话题链接:{},子分类话题ID:{},子分类话题描述:{}".format(sub_name, sub_link, sub_id,sub_description))

                        print("\n")

                    else:

                        with open("all_topics.txt", "a",encoding='utf8') as f:

                            f.write("当前子分类数据已爬取完毕" + "\n" + "\n" + "\n")

                        print("当前子分类话题数据已爬取完毕")

                        break


    def testLink(self):

        for offset in range(0,200,20):

            url='https://www.zhihu.com/node/TopicsPlazzaListV2'

            data={'method':'next','params':'{"topic_id":304,"offset":20,"hash_id":""}'}

            response=requests.post(url,headers=self.headers,data=data)

            sub_list=json.loads(response.text)

            print(sub_list)

            print()

            if len(sub_list)>0:

                print("存在数据,继续爬取")

                for sub in sub_list:

                    sub_name=re.findall('<strong>(.*?)</strong>',sub,re.S)[0]

                    sub_link="https://www.zhihu.com"+re.findall('href="(.*?)"',sub,re.S)[0]

                    sub_id=re.findall('href="/topic/(.*?)"',sub,re.S)[0]

                    sub_description=re.findall('<p>(.*?)</p>',sub,re.S)[0]

                    if sub_description=='':

                        sub_description='无话题描述'

                    else:

                        sub_description=sub_description

                    print("子分类话题:{},子分类话题链接:{},子分类话题ID:{},子分类话题描述:{}".format(sub_name,sub_link,sub_id,sub_description))

                print("\n")

            else:

                print("数据已爬取完毕")

                break


    def testCase(self):

        link='https://www.zhihu.com/topic/19553732/hot'

        response=requests.get(link,headers=self.headers)

        html=response.text

        print(html)
        #print(response.status_code)


if __name__ == '__main__':

    spider=GetTopic()

    spider.testCase()

    # spider.get_parent_data()
    #
    # print(spider.topics_data)
    #
    # print(len(spider.topics_data))
    #
    # spider.get_sub_data()

    #spider.testLink()
