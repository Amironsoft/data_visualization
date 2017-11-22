from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

parallels = np.arange(20, 36, 2.)
meridians = np.arange(-120, -100, 2.)

lat, lon = 59.942952, 30.257746
dx = 0.2
lon_min = lon - dx
lon_max = lon + dx
lat_min = lat - dx
lat_max = lat + dx

# serverurl = 'http://osm.woc.noaa.gov/mapcache?'
# serverurl = 'http://myhost.com/mapcache/tms/1.0.0/?'
serverurl = 'http://vmap0.tiles.osgeo.org/wms/vmap0?'

layers = ['Vmap0', 'basic', 'ocean', 'ground_01', 'ground_02', 'population', 'river', 'stateboundary', 'country_01',
          'country_02', 'disp', 'inwater', 'coastline_01', 'coastline_02', 'depthcontour', 'priroad', 'secroad', 'rail',
          'ferry', 'tunnel', 'bridge', 'trail', 'CAUSE', 'clabel', 'statelabel', 'ctylabel']
need_layers = ['basic']

for layer in need_layers:
    plt.figure()
    m = Basemap(llcrnrlon=lon_min, urcrnrlat=lat_max,
                urcrnrlon=lon_max, llcrnrlat=lat_min, resolution='i', epsg=4326)
    # m.drawlsmask()
    plt.title(layer)
    m.wmsimage(serverurl, xpixels=500, verbose=True,
               layers=[layer], format='jpeg')
    m.drawcoastlines(linewidth=0.25)
    a = m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
    b = m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)
    plt.show()
    plt.close()
