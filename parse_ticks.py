import matplotlib.pyplot as plt
import pandas as pd
import numpy
import re
from urllib import request

TICK_FILENAME = 'ticks.csv'
PLOT_FILENAME = 'tick_plot.png'

def download_ticks(user_url):
    # sanitize inputs
    match_string = '^((https\:\/\/)?www\.)?mountainproject\.com\/user\/([0-9]+\/[0-9a-z\-]+)\/?$'
    match = re.match(match_string, user_url)
    if not match:
        raise ValueError('URL not correctly formatted')
    user_path = match.group(3)
    tick_download_url = 'https://www.mountainproject.com/user/%s/tick-export' % user_path
    with request.urlopen(tick_download_url) as resp, open('ticks.csv', 'w') as f:
        f.write(resp.read().decode('utf-8'))

def get_tick_df():
    df = pd.read_csv(TICK_FILENAME)
    style_types = ['Lead', 'Solo', 'Flash', 'Send', numpy.nan]
    columns = ['Date', 'Rating Code', 'Route Type', 'Pitches', 'Style']
    df = df.loc[df['Style'].isin(style_types), columns]
    df = df.loc[df['Route Type'].str.contains('Trad|Sport', regex=True)]
    df = df.sort_values(by='Date', ascending=True)
    return df

def save_plot(df):
    x = df['Date']
    y = df['Rating Code']
    plt.scatter(x, y)
    plt.savefig(PLOT_FILENAME)
    return PLOT_FILENAME

