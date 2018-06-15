# -*- coding: utf-8 -*-

import time

import pymysql

from SpiderZhiHu import settings


class SpiderzhihuPipeline(object):

    def __init__(self):

        '''初始化连接数据库'''

        print("正在为写入父话题信息连接数据库")

        time.sleep(5)

        self.connect = pymysql.connect(

            host=settings.MYSQL_HOST,port=3306,

            db=settings.MYSQL_DBNAME,user=settings.MYSQL_USER,

            passwd=settings.MYSQL_PASSWD,charset='utf8',use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

        print("数据库连接成功")

    def process_item(self, item, spider):

        try:

            self.cursor.execute(
                "insert into zhihu.zhihu_parent_topic(parent_topic_id, parent_topic_name) VALUES (%s,%s)", [item['parent_topic_id'], item['parent_topic_name']])

            # 提交sql语句
            self.connect.commit()

            print("Save ParentTopic Success！")

        except Exception as error:

            pass

        return item

