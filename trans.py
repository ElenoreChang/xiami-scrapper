# -*- coding: utf-8 -*-

class transCookie:
	
    def __init__(self, cookie):

        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}

        items = self.cookie.split(';')


        for item in items:

            key = item.split('=')[0].replace(' ', '')

            value = item.split('=')[1]

            itemDict[key] = value

        return itemDict

if __name__ == "__main__":

    cookie = 'your cookie'

    trans = transCookie(cookie)

    print(trans.stringToDict())