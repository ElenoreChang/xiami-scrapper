# -*- coding: utf-8 -*-
import logging
import sys,os


class TransCookie:
    cookie = None
    cookie_path = os.getcwd() + '/cookie.txt'

    def __init__(self):
        try:
            f = open(self.cookie_path, "r")
            self.cookie = f.read()
        except:
            logging.error(f'please add cookie in {self.cookie_path}')



    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        try:
            items = self.cookie.split(';')
            for item in items:
                key = item.split('=')[0].replace(' ', '')
                value = item.split('=')[1]
                itemDict[key] = value
        except:
            logging.error(f'please check cookie in {self.cookie_path}')

        return itemDict


if __name__ == "__main__":
    trans = TransCookie()

    print(trans.stringToDict())
