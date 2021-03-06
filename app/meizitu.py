# -*- coding: utf-8 -*-
import requests
from lxml import etree
import random
import re

class Meizitu:
    def __init__(self):
        self.url = 'http://www.mmjpg.com/'
        self.tag_list = [u'性感', u'小清新', u'刘飞儿', u'可儿', u'美胸', u'美臀', u'萌妹', u'ROSI', u'推女神', u'内衣', u'美腿', u'秀人网', u'尤果网', u'DISI', u'陆瓷', u'绮里嘉', u'第四印象']

    def crawl(self, tag_index):
        resp = requests.get(self.url)
        page = resp.content
        html = etree.HTML(page)
        path = '/html/body/div[1]/div[3]/a[%d]/@href' % (tag_index+1)
        tag_url = html.xpath(path)[0]
        resp = requests.get(tag_url)
        page = resp.content
        result = re.search('class="page.*?class="info.*?(\d+).*?</em>', page)
        page_count = result.group(1)
        nPage = random.randint(1, int(page_count))
        tag_url = tag_url + '/' + str(nPage)
        resp = requests.get(tag_url)
        page = resp.content
        html = etree.HTML(page)
        articals = []
        num = len(html.xpath('/html/body/div[3]/div[1]/ul/li'))
        if num > 8:
            length = 8
        else:
            length = num
        n_list = random.sample(range(num), length)
        for index, i in enumerate(range(length)):
            n = n_list[index]
            link_p = '/html/body/div[3]/div[1]/ul/li[%d]/a/@href' % (n+1)
            link = html.xpath(link_p)[0]
            link_img_p = '/html/body/div[3]/div[1]/ul/li[%d]/a/img/@src' % (n+1)
            link_img = html.xpath(link_img_p)[0]
            name_p = '/html/body/div[3]/div[1]/ul/li[%d]/a/img/@alt' % (n+1)
            name = html.xpath(name_p)[0]
            articals.append([name, name, link_img, link])
        return articals

