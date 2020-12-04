#!/usr/bin/env python

import requests as r
import itertools
import os
import json
from glob import glob


years = [2020]
months = [9,10,11,12]
for (yyyy,mm) in itertools.product(years,months):
    remote_base_url = 'https://api.chess.com/pub/player/senseidanya/'
    game_url = 'games/{:04}/{:02}'.format(yyyy,mm)
    print(remote_base_url + game_url)
    
    xx = r.get(remote_base_url + game_url)
    print(xx.status_code)
    if xx.status_code == 200:
        os.makedirs(os.path.dirname(game_url), exist_ok=True)
        with open(game_url + '.json','wb') as f:
            f.write(xx.content)    


