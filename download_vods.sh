#!/bin/bash
pushd ./vods
youtube-dl  https://www.twitch.tv/gmnaroditsky/videos   --write-info-json  --skip-download 
popd

