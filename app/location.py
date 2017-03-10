import matplotlib.pyplot as plt

class Location:
    def __init__(self):
        self.latitudeList = [31.19, 40.28, 50.63]
        self.longitudeList = [121.577, 130.577, 140.588]

    def addPoint(self, latitude, longitude):
        self.latitudeList.append(latitude)
        self.longitudeList.append(longitude)

    def draw(self):
        plt.xlabel('latitude')
        plt.ylabel('longitude')
        plt.plot(self.latitudeList, self.longitudeList)
        plt.show()
        plt.savefig('app/static/trace.jpg')
