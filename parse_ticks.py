from matplotlib.colors import ListedColormap
from urllib import request
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import re
import datetime
import math
import os.path

class UrlFormatError (Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message
        
class EmptyDataFrameError (Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


def normailize_rating_code(x):
    conditions = {
        800: 1625, # '3rd'
        900: 1875, # '4th'
        950: 2000, # 'Easy 5th'
        1000: 2125, # '5.0'
        1100: 2375, # '5.1'
        1200: 2625, # '5.2'
        1300: 2875, # '5.3'
        1400: 3125, # '5.4'
        1500: 3375, # '5.5'
        1600: 3625, # '5.6'
        1800: 3875, # '5.7'
        1900: 3925, # '5.7+'
        2000: 4075, # '5.8-'
        2100: 4125, # '5.8'
        2200: 4175, # '5.8+'
        2300: 4325, # '5.9-'
        2400: 4375, # '5.9'
        2500: 4425} # '5.9+'
    if abs(3000 - x) <= 500: # 5.10
        x += 2000
    elif abs(5000 - x) <= 500: # 5.11
        x += 1000
    elif abs(9000 - x) <= 500: # 5.13
        x -= 1000
    elif abs(11000 - x) <= 500: # 5.14
        x -= 2000
    elif abs(12000 - x) <= 500: # 5.15
        x -= 2000
    else:
        x = conditions.get(x, x)
    return x

def download_ticks(user_url):
    # sanitize inputs
    match_string = '^((https\:\/\/)?www\.)?mountainproject\.com\/user\/([0-9]+)\/([0-9a-z\-]+)\/?$'
    match = re.match(match_string, user_url)
    if not match:
        raise UrlFormatError('Unable to parse URL. Try using a link that looks something like this: mountainproject.com/user/200683687/ray-murphy')
    user_id, username = match.group(3), match.group(4)
    tick_download_url = 'https://www.mountainproject.com/user/%s/%s/tick-export' % (user_id, username)
    filename = 'data/' + user_id + '.csv'
    if not os.path.isfile(filename):
        # TODO: handle case that tick file needs to be updated
        with request.urlopen(tick_download_url) as resp, open(filename, 'w') as f:
            f.write(resp.read().decode('utf-8'))
    return filename, username
        
def str_to_date(x):
    try:
        if type(x) == str:
            return datetime.datetime.strptime(x, "%Y-%m-%d").date()
        else:
            return x
    except ValueError as ve:
        return datetime.datetime(1970, 1, 1).date()

def get_attribute_title(s):
    return s.upper() if s == 'tr' else s.title()

def get_tick_df(config, filename):
    df = pd.read_csv(filename)
    style_types = [get_attribute_title(k) for k, v in config.get("styles", {}).items() if v]
    route_types = [get_attribute_title(k) for k, v in config.get("types", {}).items() if v]
    route_types_re = '|'.join(route_types)
    include_falls = config.get("includeFalls", False)
    start_date = config.get("dates", {}).get("start")
    end_date = config.get("dates", {}).get("end")
    if '(Blank)' in style_types:
        style_types.pop('(Blank)')
        style_types.append(numpy.nan)
    # include boulders:  'Flash', 'Send'
    columns = ['Date', 'Rating Code', 'Route Type', 'Pitches', 'Style', 'Lead Style']
    df = df.loc[df['Style'].isin(style_types), columns]
    df['Date'] = df['Date'].apply(str_to_date)
    if start_date:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ').date()
        df = df.loc[df['Date'] >= start_date ]
    if end_date:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%fZ').date()
        df = df.loc[df['Date'] <= end_date ]
    if not include_falls:
        df = df.loc[df['Lead Style'] != 'Fell/Hung']
    df = df.loc[df['Route Type'].str.contains(route_types_re, na=False, regex=True)]
    # TODO: check null
    df = df.loc[df['Rating Code'] < 20000] # filter out bouldering/ice/mixed/aid/snow
    # TODO: check null
    df = df.sort_values(by='Date', ascending=True)
    df['Normalized Rating Code'] = df['Rating Code'].apply(normailize_rating_code)
    return df

def generate_yticks(ylim_min, ylim_max):
    yticks = numpy.append(
        numpy.arange(1625, 4375+1, step=250), 
        numpy.arange(5000, 10000+1, step=1000))
    labels = numpy.array(['3rd', '4th', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', 
            '5.10', '5.11', '5.12', '5.13', '5.14', '5.15'])
    filter_arr = (ylim_min <=  yticks) & (yticks <= ylim_max)
    yticks = yticks[filter_arr]
    labels = list(labels[filter_arr])
    return yticks, labels

def get_color_info(climb_types: numpy.array):
    cmap, styles = [], []
    if 0 in climb_types:
        cmap.append('r')
        styles.append('Sport lead')
    if 1 in climb_types:
        cmap.append('b')
        styles.append('Trad lead')
    if 2 in climb_types:
        cmap.append('m')
        styles.append('Mixed lead')
    if 3 in climb_types:
        cmap.append('k')
        styles.append('Solo')
    if 4 in climb_types:
        cmap.append('y')
        styles.append('TR')
    if 5 in climb_types:
        cmap.append('c')
        styles.append('Follow') 
    N = len(cmap)
    return ListedColormap(cmap, N=N), styles
    
def get_title(username: str):
    if not username:
        return 'Rock Climbing Ticks'
    name = username.replace('-', ' ').title()
    return "%s's Rock Climbing Ticks" % name

def get_color_code(x):
    if x['Style'] == 'Solo':
        return 3
    elif x['Style'] == 'TR':
        return 4
    elif x['Style'] == 'Follow':
        return 5
    elif 'Sport' in x['Route Type'] and 'Trad' in x['Route Type']:
        return 2
    elif 'Sport' in x['Route Type']:
        return 0
    else:
        return 1

def convert_to_consecutive_indecies(s: pd.Series):
    unique_values = s.unique()
    unique_values.sort()
    mapping = dict((val, i) for i, val in enumerate(unique_values))
    return s.apply(lambda x : mapping[x])
        
def get_plot_colors(df: pd.DataFrame):
    c = df.apply(get_color_code, axis=1)
    colors, labels = get_color_info(c.unique())
    c = convert_to_consecutive_indecies(c)
    return c, colors, labels

def save_plot(df: pd.DataFrame, plot_filename, username=None):
    if df.empty:
        raise EmptyDataFrameError('empty df')
    title = get_title(username)
    x = df['Date']
    y = df['Normalized Rating Code']
    area = (df['Pitches'].apply(lambda x : math.pow(x, 0.9)) * 15)
    c, colors, labels = get_plot_colors(df)
    scatter = plt.scatter(x, y, c=c, cmap=colors, s=area, alpha=0.5) 
    ylim_min, ylim_max = plt.ylim()
    yticks, ylabels = generate_yticks(ylim_min, ylim_max)
    plt.yticks(yticks, ylabels)
    plt.xticks(rotation=30)
    plt.legend(handles=scatter.legend_elements()[0], labels=labels, loc='upper left', shadow=True)
    plt.title(title)
    plt.savefig(plot_filename)
    plt.close()
    return plot_filename

