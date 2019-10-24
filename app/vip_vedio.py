# encoding: utf-8

import requests
import re
import json
from lxml import etree


class VipVideo:

    def __init__(self):
        self.api_list = (
            'http://api.ledboke.com/vip/?url=',
            'http://api.ledboke.com/?v=',
            'http://17kyun.com/api.php?url=',
        )
        # video_url = 'https://v.qq.com/x/cover/e0jts33la7wbnfk/m00240ny61l.html'

    def tencent(self, user_input):
        match = re.match('^(.+?)\s*(\d*)\s*$', user_input)
        if match is None:
            return None, u'输入有误！'
        name = match.group(1).strip()
        try:
            episode_num = int(match.group(2).strip())
        except ValueError:
            episode_num = 1
        url = 'https://v.qq.com/x/search/?q=%s&stag=0&smartbox_ab=' % name
        r = requests.get(url)
        html = etree.HTML(r.content)
        playlist = html.xpath('//div[@class="_playlist"]')[0]
        self.episode_urls = playlist.xpath('descendant::div/a/@href')
        if episode_num==0 or episode_num > len(self.episode_urls):
            return None, u'没有这一集！'
        return 1, self.episode_urls[episode_num-1]

    def free_url(self, user_input):
        success, vip_url = self.tencent(user_input)
        if success is None:
            return vip_url
        data = ''
        for i, api in enumerate(self.api_list):
            data += u"线路%d:\n%s\n\n" % (i+1, api+vip_url)
        data = data.strip()
        return data


if __name__ == '__main__':
    vv = VipVideo()
    print vv.free_url(u'伪装大师')
