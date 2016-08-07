#!/usr/bin/env bash
cd /home/shimon/code/929-feeds
/home/shimon/anaconda2/bin/python ./fetch.py
git add feeds
git commit -m "update feeds"
git push
echo "pushed"
