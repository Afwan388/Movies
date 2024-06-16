import requests
from bs4 import BeautifulSoup
from http import client
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient


url = 'https://www.imdb.com/title/tt0068646/?ref_=ext_shr_lnk'

headers = {'User-Agent' : 'Mozila/5.0 (Windows NT 10.0; Win64; x64)App'}
data = requests.get(url,headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

og_image = soup.select_one('meta[property="og:image"]')
og_title = soup.select_one('meta[property="og:title"]')
og_description = soup.select_one('meta[property="og:description"]')

image = og_image['content']
title = og_title['content']
description = og_description['content']

print(og_image)
print(og_title)
print(og_description)