# -*- coding: utf-8 -*-
from reply import *
from lxml import etree
import re

class Meizitu:
	def __init__(self):
		self.url = 'http://www.meizitu.com/'

	def crawl(self, tag):
		resp = requests.get(self.url)
		page = resp.content
		link = re.search('href="(.*?)".*?title="%s"' % tag, page, re.S)
		print link
		resp = requests.get(link)
		page = resp.content
		html = etree.HTML(page)
		articals = []
		for i in range(10):
			link = html.xpath('//*[@id="maincontent"]/div[1]/ul/li[%s]/div/div/a/@href' % i)[0]
			link_img = html.xpath('//*[@id="maincontent"]/div[1]/ul/li[%s]/div/div/a/img')[0]
			name = html.xpath('//*[@id="maincontent"]/div[1]/ul/li[%s]/div/div/a/img/@alt' % i)[0]
			articals.append([name, name, link_img, link])
		print articals
		return reply.imgTextMsg(articals)

meizitu = Meizitu()