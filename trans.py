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
    cookie = 'Cookie:ll="108169"; bid=_LslisEBN28; gr_user_id=b7acf172-f530-4b03-a382-09c01f90a17f; __yadk_uid=M81oc8fkTyUkxj7WMB0FZYqi2zlqLCGR; ct=y; ps=y; ue="wanzi_xiaohan@sina.com"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1498719043%2C%22https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26411410%2Fcomments%22%5D; _ga=GA1.2.415202519.1488604443; _gid=GA1.2.554690448.1498641572; dbcl2="1430089:Lo3SaUaJbAU"; ck=mwp0; ap=1; _vwo_uuid_v2=C4FB415BDBAE700FEDA71B46BA71C580|6c375af1f081ea4fac33ce878d520c29; __utmt=1; push_noty_num=0; push_doumail_num=0; __utma=30149280.415202519.1488604443.1498655560.1498717968.34; __utmb=30149280.15.10.1498717968; __utmc=30149280; __utmz=30149280.1498717968.34.8.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmv=30149280.143; _pk_id.100001.8cb4=38793c8d2368953a.1488604431.31.1498720751.1498657369.; _pk_ses.100001.8cb4=*'
    trans = transCookie(cookie)
    print trans.stringToDict()