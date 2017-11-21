import os
import folium
import pandas as pd
from folium.plugins import HeatMap


if __name__ == '__main__':
    lat, lon = 59.942952, 30.257746  # St. Petersburg
    spb = folium.Map(location=[lat, lon], zoom_start=10)
    df = pd.read_csv(r'input/spb_cafe.tsv', sep='\t', na_values='None')
    df.dropna(subset=['lat', 'lon'], inplace=True)
    lats = df['lat'].values
    lons = df['lon'].values
    vals = df['mean_price_num'].values

    xnew = pd.read_csv(r'input/xnew.tsv', sep=' ', header=None).values
    ynew = pd.read_csv(r'input/ynew.tsv', sep=' ', header=None).values
    znew = pd.read_csv(r'input/znew.tsv', sep=' ', header=None).values
    n, m = znew.shape
    heat_mas = [[ynew[i, j], xnew[i, j], znew[i][j]] for i in range(n) for j in range(m)]

    for i, row in df.iterrows():
        folium.Marker([row.lat, row.lon], popup=f"{row['name']}, {row['mean_price_num']}").add_to(spb)
    # HeatMap(heat_mas, radius=10).add_to(spb)
    # spb.save("output/spb_cafe_heat.html")
    spb.save("output/spb_cafe.html")
