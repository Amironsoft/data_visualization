import pandas as pd
from bokeh.plotting import figure, show, gridplot, save, output_file
from bokeh.io import output_notebook
import numpy as np

output_notebook()
tools = 'reset,xwheel_pan,xwheel_zoom,ywheel_zoom,pan,save'


def calc_dd_rean(row, u_name, v_name):
    # Calculate DD by U and V wind components
    if row[u_name] != np.NaN and row[v_name] != np.NaN:
        u = row[u_name]
        v = row[v_name]
        dd = np.arctan2(-u, -v) / np.pi * 180
        if dd < 0:
            dd += 360
        return dd
    else:
        return np.NaN


def get_p(station_id, station_name, pq, df_list, p_first):
    # return bokeh figure
    if p_first:
        p = figure(title=fr"{pq} {station_id} {station_name}", tools=tools, x_axis_type='datetime',
                   active_scroll='xwheel_zoom', x_range=p_first.x_range)  # assume common x axis
    else:
        p = figure(title=fr"{pq} {station_id} {station_name}", tools=tools, x_axis_type='datetime',
                   active_scroll='xwheel_zoom')
    color_dict = {'obs': 'blue', 'wrf': 'red', 'obs_noaa': 'red', 'obs_rp5': 'green', 'era': 'green'}
    for source_name, df in df_list:
        p.line(df.index, df[pq].values, legend=source_name, line_color=color_dict[source_name])
    p.legend.click_policy = "hide"
    return p


def get_df(ifile):
    df = pd.read_csv(ifile, sep=',')
    cols = df.columns
    if 'T' in cols:  # suggest obs
        df.index = pd.to_datetime(df['Date'])
        df.rename(columns={'T': 't2m', 'P': 'PSFC', 'U10M': 'u_10m', 'V10M': 'v_10m'}, inplace=True)
    elif 'u_10m' in cols:  # suggest wrf
        df.index = pd.to_datetime(df['time'])
        df['PSFC'] /= 100
        df['Ff'] = (df['u_10m'] ** 2 + df['v_10m'] ** 2) ** 0.5
        df['DD'] = df[['u_10m', 'v_10m']].apply(calc_dd_rean, args=('u_10m', 'v_10m',), axis=1)
    return df


if __name__ == '__main__':
    start = '2012-01-01'
    end = '2017-12-31'

    idir_obs = r'input/obs/'
    idir_wrf = r'input/wrf/'
    idir_era = r'input/era/'

    df_stations_all = pd.read_csv(r'input/points.tsv', sep='\t')
    df_stations_all['ind'] = list(range(len(df_stations_all)))

    global_id_list = df_stations_all['id'].values
    for global_id in global_id_list:
        row = df_stations_all[df_stations_all['id'] == global_id].iloc[0]
        ind = row['ind']
        station_name = row['name']
        print(global_id, station_name, ind)
        file_obs = rf'{idir_obs}{global_id}.csv'
        file_wrf = rf'{idir_wrf}wrf.{ind}.csv'
        file_era = rf'{idir_era}era.{ind}.csv'
        df_obs = get_df(file_obs)
        df_era = get_df(file_era)
        df_wrf = get_df(file_wrf)

        df_obs = df_obs.loc[start: end]
        df_wrf = df_wrf.loc[start: end]
        df_era = df_era.loc[start: end]

        p_first = None
        p_list = []
        for pq in ['PSFC', 't2m', 'u_10m', 'v_10m', 'Ff', 'DD']:
            p = get_p(global_id, station_name, pq, [['obs', df_obs], ['wrf', df_wrf], ['era', df_era]], p_first)
            if not p_first:
                p_first = p
            p_list.append(p)
        p_grid = [[p_list[0], p_list[1]], [p_list[2], p_list[3]], [p_list[4], p_list[5]]]
        layout = gridplot(p_grid)
        # show(layout)
        odir = r'output/bokeh_plots/'
        output_file(f'{odir}{global_id}.{station_name}.new.html', title='comparison')
        save(layout)
