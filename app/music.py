import requests
import urllib
from lxml import etree

class Music:
    def getMusic(self, name):
        name_urlcode = urllib.quote(name)
        url = 'http://music.163.com/#/search/m/?s=%s&type=1' % name_urlcode
        resp = requests.get(url)
        html = etree.HTML(resp.text)
        link = html.xpath('//*[@id="auto-id-cp8o3EiD60QqSENI"]/div/div/div[1]/div[2]/div/div/a/@href')[0]
        abs_link = url + link
        print abs_link
        return abs_link

music = Music()