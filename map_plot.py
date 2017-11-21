import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd
import matplotlib.patheffects as path_effects
import os
import fnmatch
import matplotlib.colors as colors

plot_connections = False


def plot_groups_csv(idir, bm):
    colors = ['red', 'green', 'blue', 'yellow', 'brown', 'black', 'navy', 'pink', 'cyan']
    groups_ids = []
    for i, file in enumerate(fnmatch.filter(os.listdir(idir), '*.csv')):
        df = pd.read_csv(idir + file, sep=',')
        names = df['id'].values
        lons = df['lon'].values
        lats = df['lat'].values

        bmlons, bmlats = bm(lons, lats)
        center_lon, center_lat, center_name = bmlons[0], bmlats[0], names[0]
        groups_ids.append(center_name)
        for name, bmlon, bmlat in zip(names, bmlons, bmlats):
            print(file, center_name, name)
            if name != center_name and plot_connections:
                bm.plot([center_lon, bmlon], [center_lat, bmlat], color=colors[i])
            bm.scatter(bmlon, bmlat, color='red', s=50)
        bm.scatter(center_lon, center_lat, color='red', s=50)
        print(groups_ids)
    return groups_ids


def get_point_size(p):
    # split points size
    size_dict = {
        p < 25: 20,
        25 <= p < 50: 50,
        50 <= p < 75: 80,
        p >= 75: 150
    }
    return size_dict[True]


def plot_stations():
    use_color = True
    use_size = True
    need_annotate = True
    need_groups = True
    point_scale = 4

    idir = r'input/'
    df = pd.read_csv(idir + 'gaps_all_init.csv', sep=';')  # main dataset

    mis_perc = df['total_mis_perc'].values
    c = df['gaps_number'].values
    need_stations = df['station_id'].values

    bm = Basemap(projection='npstere', boundinglat=60, lon_0=270, resolution='l')  # World sphere
    bm.bluemarble(alpha=0.3)
    bm.drawmeridians(np.arange(10., 351., 20.), labels=[True, True, True, True])
    bm.drawparallels(np.arange(60, 90, 20.), labels=[1, 1, 1, 1])

    bm.drawcoastlines()
    lats = df['lat'].values
    lons = df['lon'].values

    if use_color and use_size:
        print('use_color and use_size')
        cmap_name = 'rainbow'
        cmap1 = plt.get_cmap(cmap_name)

        points_size = [get_point_size(p) * point_scale for p in mis_perc]
        bmlons, bmlats = bm(lons, lats)
        bm_scatter_plot = bm.scatter(bmlons, bmlats, s=points_size, c=c, cmap=cmap1, edgecolors='black',
                                     norm=colors.PowerNorm(gamma=1/2.))
        cbar = bm.colorbar(bm_scatter_plot, location='right', pad="5%", ticks=[100, 500, 1200, 2000, 3000, 4000])
        # cbar.locator = ticker.MaxNLocator(nbins=20)
        cbar.update_ticks()
        cbar.set_label('number of gaps')

        # circles magic
        l1 = plt.scatter([], [], s=point_scale * 20, facecolor='none', edgecolors='black')
        l2 = plt.scatter([], [], s=point_scale * 50, facecolor='none', edgecolors='black')
        l3 = plt.scatter([], [], s=point_scale * 80, facecolor='none', edgecolors='black')
        l4 = plt.scatter([], [], s=point_scale * 150, facecolor='none', edgecolors='black')

        labels = [f'<{i}' if i != 100 else f'>75' for i in [25, 50, 75, 100]]
        leg = plt.legend([l1, l2, l3, l4], labels, ncol=4, frameon=True, fontsize=11,
                         handlelength=2, loc=8, borderpad=1.5, handletextpad=.8, title='Total time missing %',
                         scatterpoints=1)
        leg.get_frame().set_alpha(0.9)
        if need_groups:
            groups_ids = plot_groups_csv(r'input\groups/', bm)

    elif need_groups:
        groups_ids = plot_groups_csv(r'input\groups/', bm)
        need_stations = groups_ids
    else:
        bmlons, bmlats = bm(lons, lats)
        bm_scatter_plot = bm.scatter(bmlons, bmlats, s=100, color='red')

    fontsize = 7
    for i in range(len(df)):
        station_name = df['station_id'].iloc[i]
        if station_name in need_stations[::3] and need_annotate:
            lat = df['lat'].iloc[i]
            lon = df['lon'].iloc[i]
            lon, lat = bm(lon, lat)
            perc = df['total_mis_perc'].iloc[i]
            # txt = plt.gca().annotate(i, (lon, lat), fontsize=10, color='white')
            if station_name.startswith('22') or station_name.startswith('040'):
                if i % 5 == 0:
                    txt = plt.gca().annotate(station_name, (lon, lat), fontsize=fontsize, color='white')
            else:
                txt = plt.gca().annotate(station_name, (lon, lat), fontsize=fontsize, color='white')
            txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])
        elif need_groups:
            if station_name in groups_ids:
                lat = df['lat'].iloc[i]
                lon = df['lon'].iloc[i]
                lon, lat = bm(lon, lat)
                txt = plt.gca().annotate(station_name, (lon, lat), fontsize=fontsize, color='white')
                txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])

    plt.tight_layout()
    odir = r'output/basemap_plots/'
    plt.title('Stations Set1', bbox=dict(facecolor='white'), fontsize=8)
    plt.savefig(f'{odir}stations_map_colors.png', dpi=400)
    # plt.show()
    print(odir)


if __name__ == '__main__':
    plot_stations()
