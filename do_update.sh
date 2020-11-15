#!/bin/bash

mkdir vods
mkdir games


source ~/anaconda3/bin/activate
source download_vods.sh



ipython ./FetchGames.py 
ipython ./BuildJson.py

git add ./guide.json
git commit -m "json update"
GIT_SSH_COMMAND="ssh -i ~/.ssh/danyaspeedrun" git push 

