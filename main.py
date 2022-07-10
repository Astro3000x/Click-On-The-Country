import matplotlib.pyplot as plt
import geopandas
import random
from shapely.geometry import Point


class ClickCountry:
    def __init__(self):
        self.world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
        self.win = False
        self.choosecountry()
        self.showmap()

    def choosecountry(self):
        i = random.randint(0, len(self.world))
        self.random_countryinfo = self.world.iloc[i]
        self.country_series = self.world.iloc[i:i+1]
        self.countryname = self.random_countryinfo["name"]
        self.randomcountrygeometry = self.random_countryinfo["geometry"]

    def showmap(self):
        self.fig, self.ax = plt.subplots(num=f"Double Click on {self.countryname}")
        self.ax = self.world.plot(ax=self.ax, linewidth=1, edgecolor="black")
        self.updatemap()
        self.ax.figure.canvas.mpl_connect('button_press_event', self.onclick)

    def updatemap(self):
        self.ax.set(aspect=1, title=f"Double Click On The Country\nCountry: {self.countryname}")

        # fig.tight_layout()
        # self.random_countryinfo["name"].plot(ax=self.ax)
        # self.world[self.world.name == self.random_countryinfo["name"]].plot(ax=self.ax)

    def whatcountry(self, long: float, lat: float):
        point = Point([long, lat])
        for i, row in self.world.iterrows():
            if row["geometry"].contains(point):
                return row["name"]
        else:
            return "not a country"

    def onclick(self, event):
        if not event.dblclick:
            return
        ix, iy = event.xdata, event.ydata
        print(event)
        print('x = %f, y = %f' % (ix, iy))
        countryname = self.whatcountry(ix, iy)
        point = Point(ix, iy)
        if self.randomcountrygeometry.contains(point):
            print("Victory")

            self.country_series.plot(color="red", ax=self.ax)
            self.ax.set(aspect=1, title=f"You Win! Country: {self.countryname}")
            # random_countryinfo.plot(color="red", ax=ax)
            # ax = world.plot(ax=ax)
            plt.pause(0.1)

            # plt.show(block=True)
            self.win = True
        elif self.win:
            pass
        else:
            distance = self.randomcountrygeometry.distance(point) * 111
            self.ax.set(aspect=1,
                        title=f"Country: {self.countryname}\nNo, that's {countryname}.\nYou are {distance:.0f}km away.")

def main():
    game = ClickCountry()
    game2 = ClickCountry()
    plt.ion()
    plt.show(block=True)
    pass


if __name__ == '__main__':
    main()
