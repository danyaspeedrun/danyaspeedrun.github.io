#!/usr/bin/env python
# coding: utf-8

import chess
import chess.pgn
import json
import io
import pandas as pd
from glob import glob
from bs4 import BeautifulSoup
import requests as r



game_files = glob("./games/**/*.json",recursive=True)
games = []
for file in game_files:
    with open(file) as f:
        j = json.load(f)
        games += j['games']

pgn_df = pd.DataFrame([chess.pgn.read_headers(io.StringIO(x['pgn'])) for x in games])
pgn_df['dt'] = pd.to_datetime(pgn_df['UTCDate'] + ' ' + pgn_df['UTCTime'])


def extract_openings(x):
    url = x['ECOUrl']
    soup = BeautifulSoup(r.get(url).content)
    x['opening_name'] = soup.find("meta",property="og:title")['content']
    print(x['opening_name'])
    x['opening_thumbnail_orig'] = soup.find("meta",property="og:image")['content']
    x['opening_thumbnail'] = soup.find("meta",property="og:image")['content'].split('&')[0]   
    
    flip = x['Black'] == "SenseiDanya"
    if flip:
        x['opening_thumbnail'] += "&flip=true"
    return x
    

pgn_df = pgn_df.apply(extract_openings, axis=1)
pgn_df


tmp = {}
tmp['id'] = []
tmp['vod_start_posix'] = []
tmp['vod_end_posix'] = []
tmp['vod_thumb'] = []
tmp['vod_url'] = []
for fname in glob('./vods/*.json'):
    with open(fname) as f:
        vod_json = json.load(f)
        tmp['id'].append(vod_json['id'][1:])
        tmp['vod_start_posix'].append(vod_json['timestamp'])
        tmp['vod_end_posix'].append(vod_json['timestamp']+vod_json['duration'])
        tmp['vod_thumb'].append(vod_json['thumbnails'][-1]['url'])
        tmp['vod_url'].append('https://www.twitch.tv/videos/' + tmp['id'][-1])
        
vod_df = pd.DataFrame(tmp)

vod_df['vod_start'] = pd.to_datetime(vod_df['vod_start_posix'], unit='s')
vod_df['vod_end'] = pd.to_datetime(vod_df['vod_end_posix'], unit='s')
vod_df = vod_df.sort_values('vod_start')
vod_df

joined_df = pd.merge_asof(pgn_df,vod_df, direction='backward', left_on='dt', right_on='vod_start')
joined_df['vod_offset'] = (joined_df['dt']-joined_df['vod_start']).dt.total_seconds().astype('int')
joined_df['vod_link_with_offset'] = joined_df['vod_url'] + "?t=" + joined_df['vod_offset'].astype('str') + "s"
joined_df = joined_df.query('vod_end > dt')


with open('guide.json','w') as f:
    f.write(joined_df.to_json(orient='records'))




