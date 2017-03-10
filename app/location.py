import matplotlib.pyplot as plt
import pylibmc as memcache
from math import radians, sin, cos, asin, sqrt

class Location:
    def __init__(self, openId):
        self.openId = openId

    def addPoint(self, latitude, longitude):
        mc = memcache.Client()
        loc = mc.get('loc')
        if loc == None:
            loc = {}
            mc.set('loc', loc)
        try:
            loc.get(self.openId).append([latitude, longitude])
        except:
            loc[self.openId] = []
            loc.get(self.openId).append([latitude, longitude])
        mc.set('loc', loc)

    def draw(self):
        plt.xlabel('latitude')
        plt.ylabel('longitude')
        plt.plot(self.latitudeList, self.longitudeList)
        #plt.savefig('app/static/trace.jpg')

    def calDistance(self):
        mc = memcache.Client()
        loc = mc.get('loc')
        if loc == None:
            return 'no data'
        my_loc = loc.get(self.openId, [])
        print my_loc

        for i in range(len(my_loc)-1):
            point1 = my_loc[i]
            point2 = my_loc[i+1]
            lat1, lon1, lat2, lon2 = map(radians, [point1[0], point1[1], point2[0], point2[1]])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
            c = 2 * asin(sqrt(a))
            r = 6378.137
            s = c * r
            if s < 0:
                return str(-s)
            else:
                return str(s)

    def cleanAllPoints(self):
        mc = memcache.Client()
        loc = mc.get('loc')
        if loc == None:
            return 'no data'
        loc[self.openId] = loc.get(self.openId, [])
        mc.set('loc', loc)

