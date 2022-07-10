import matplotlib.pyplot as plt
import geopandas
import random
from shapely.geometry import Point



world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
win = False
def choosecountry():
    random_country = world.iloc[random.randint(0, len(world))]
    return random_country
random_countryinfo = choosecountry()
countryname = random_countryinfo["name"]
randomcountrygeometry = random_countryinfo["geometry"]

fig, ax = plt.subplots(num=f"Double Click on {countryname}")
ax = world.plot(ax=ax,linewidth=1 ,edgecolor="black")
#fig.tight_layout()
world[world.name == random_countryinfo["name"]].plot(ax=ax)
coords = []

global eventcopy
def whatcountry(long : float, lat : float):
    point = Point([long, lat])
    for i,row in world.iterrows():
        if row["geometry"].contains(point):
            return row["name"]
    else:
        return "not a country"


def onclick(event):
    if not event.dblclick:
        return
    global win
    global randomcountrygeometry
    centroid = randomcountrygeometry.centroid
    global ax
    global eventcopy
    eventcopy = event
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print(event)
    print('x = %f, y = %f'%(ix, iy))
    countryname = whatcountry(ix, iy)
    global coords
    coords.append((ix, iy))
    point = Point(ix, iy)
    if randomcountrygeometry.contains(point):
        print("Victory")

        world[world.name == random_countryinfo["name"]].plot(color="red", ax=ax)
        ax.set(aspect=1, title=f"You Win! Country: {random_countryinfo['name']}")
        #random_countryinfo.plot(color="red", ax=ax)
        #ax = world.plot(ax=ax)
        plt.pause(0.1)

        #plt.show(block=True)
        win = True
    elif win == True:
        pass
    else:
        distance = randomcountrygeometry.distance(point)*111
        ax.set(aspect=1, title=f"Country: {random_countryinfo['name']}\nNo, that's {countryname}.\nYou are {distance:.0f}km away.")


ax.figure.canvas.mpl_connect('button_press_event', onclick)
ax.set(aspect=1, title=f"Double Click On The Country\nCountry: {random_countryinfo['name']}")




plt.ion()
plt.show(block=True)
