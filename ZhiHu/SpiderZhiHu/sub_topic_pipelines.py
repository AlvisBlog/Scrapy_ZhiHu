# -*- coding: utf-8 -*-

import time

import pymysql

from SpiderZhiHu import settings


class SpiderzhihuPipeline(object):

    def __init__(self):

        '''初始化连接数据库'''

        print("正在为写入子话题信息连接数据库")

        time.sleep(5)

        self.connect = pymysql.connect(

            host=settings.MYSQL_HOST,port=3306,

            db=settings.MYSQL_DBNAME,user=settings.MYSQL_USER,

            passwd=settings.MYSQL_PASSWD,charset='utf8',use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

        print("数据库连接成功")



    def process_item(self, item, spider):

        sub_id=item['sub_topic_id']

        name=item['sub_topic_name']

        try:

            self.cursor.execute(
                "INSERT INTO zhihu.zhihu_sub_topic(sub_topic_id,sub_topic_name,sub_topic_link,sub_topic_description,parent_topic_id) VALUES (%s,%s,%s,%s,%s)",
                [item['sub_topic_id'], item['sub_topic_name'],item['sub_topic_link'],item['sub_topic_description'],item['parent_topic_id']])

            # 提交sql语句
            self.connect.commit()

            print("Save SubTopic Success！")

        except Exception as error:

            print("%s---%s子分类信息写入失败:%s"%(name,sub_id,error))

            with open("sub_topic.log", "a+") as f:

                f.write(time.strftime("%Y-%m-%d %H:%M:%S  ") +"%s子分类信息写入失败"%(name)+ "原因:%s" % error + "\n")

            pass

        return item
