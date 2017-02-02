#!/usr/bin/python
#
#   Copyright 2016 Nur Hussein (hussein@unixcat.org)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import re
import sys
import random
import subprocess
import json
from PyLyrics import *
from alchemyapi import AlchemyAPI
from PyLyrics import *
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
from flickrapi import FlickrAPI

from local_settings import *

# Create Flickr object

flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
extras = 'url_o'

# Create the AlchemyAPI object
alchemyapi = AlchemyAPI()


def getFlickrPic(keyword):
    wallcandidate = flickr.photos.search(
        text=keyword, per_page=5, extras=extras, sort='interestingness-desc', license='2,3,4,5,6,7')
    photos = wallcandidate['photos']

    choice = random.randint(0, len(photos['photo']) - 1)
    pick = photos['photo'][choice]

    wides = {k: v for k, v in pick.iteritems() if (
        'height_o' in k or 'width_o' in k)}

    if int(wides['width_o']) >= 1280 and int(wides['height_o']) >= 900:
        return pick['url_o']
    else:
        return "None"


def getKeywords(lyrics):
    words = []

    response = alchemyapi.keywords('text', lyrics, {'sentiment': 1})

    if response['status'] == 'OK':
        for keyword in response['keywords']:
            words.append(keyword['text'].encode('utf-8'))
    
    return words


def getEntities(lyrics):
    entities = []

    response = alchemyapi.entities('text', lyrics, {'sentiment': 1})

    if response['status'] == 'OK':
        for entity in response['entities']:
            entities.append(entity['text'].encode('utf-8'))

    return entities


def getWebLyrics(artist, song_title):
    try:
        lyrics = PyLyrics.getLyrics(artist, song_title)
        if lyrics.find("data-image-key") < 0:
            return lyrics
        else:
            return song_title

    except ValueError:
        return song_title


def buildSearchString(song_title, song_keywords):
    # x = random.randint(0, 100)

    # if x < 33:
    #     return song_title
    # else:
    #     flickr_search_string = random.choice(song_keywords)
    #     return flickr_search_string
    flickr_search_string = random.choice(song_keywords)
    return flickr_search_string



if len(sys.argv) < 2:
    sys.exit(1)
else:
    song = ' '.join([str(foo) for foo in sys.argv[1:]])


# removes things in square brackets and parenthesis

song = re.sub(r'\(.*?\)', "", song)
song = re.sub(r'\[.*?\]', "", song)
artist, song_title = song.split(' - ')

print(song)
print("---")
song_lyrics = getWebLyrics(artist, song_title)
print(song_lyrics)

print(getKeywords(song_lyrics))
print(getEntities(song_lyrics))

song_keywords = getKeywords(song_lyrics) + getEntities(song_lyrics)

song_keywords = list(set(song_keywords) - set(STOPWORDS))


search_string = buildSearchString(song_title, song_keywords)

print("---")
print("Using search string:" + search_string)

url = getFlickrPic(search_string)
print("Flickr url: " + url)

subprocess.call(['./setwalluri.sh', url])
subprocess.call(['./setwall.sh'])
