import matplotlib.pyplot as plt
import geopandas
import random
from shapely.geometry import Point
from matplotlib.widgets import Button
import pycountry
#got /worldflags from https://flagpedia.net

class ClickCountry:
    def __init__(self):
        self.world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
        self.win = False
        self.showmap()
        self.choosecountry()


    def newcountry(self, event):
        self.button.label.set_text("Change Country")
        self.country_series.plot(ax=self.ax)
        self.choosecountry()
        self.win = False


    def choosecountry(self):
        i = random.randint(0, len(self.world))
        self.random_countryinfo = self.world.iloc[i]
        self.country_series = self.world.iloc[i:i+1]
        self.countryname = self.random_countryinfo["name"]
        self.randomcountrygeometry = self.random_countryinfo["geometry"]
        self.iso_a3 = self.random_countryinfo["iso_a3"]
        self.flag = pycountry.countries.get(alpha_3=self.iso_a3).flag
        self.updatemap()

    def showmap(self):
        self.fig, self.ax = plt.subplots()
        self.ax = self.world.plot(ax=self.ax, linewidth=1, edgecolor="black")
        self.axbutton = self.fig.add_axes([0.75, 0.05, 0.20, 0.075])
        self.button = Button(self.axbutton, 'Change Country')
        self.button.on_clicked(self.newcountry)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.onclick)

    def updatemap(self):
        #num=f"Double Click on {self.countryname}"
        self.fig.canvas.manager.set_window_title(f"Double Click on {self.countryname} {self.flag}")
        self.ax.set(aspect=1, title=f"Double Click On The Country\nCountry: {self.countryname}")
        plt.pause(0.1)
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
            self.button.label.set_text("Play Again")
            self.win = True
        elif self.win:
            pass
        else:
            distance = self.randomcountrygeometry.distance(point) * 111
            self.ax.set(aspect=1,
                        title=f"Country: {self.countryname}\nNo, that's {countryname}.\nYou are {distance:.0f}km away.")

def main():
    game = ClickCountry()
    plt.ion()
    plt.show(block=True)
    pass


if __name__ == '__main__':
    main()
