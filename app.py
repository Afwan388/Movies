import os
from os.path import join, dirname
from dotenv import load_dotenv 
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests 
from bs4 import BeautifulSoup

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    url = 'https://www.imdb.com/title/tt0068646/?ref_=ext_shr_lnk'

    headers = {'User-Agent' : 'Mozila/5.0 (Windows NT 10.0; Win64; x64)App'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    name_description = soup.select_one('meta[name="description"]')
    

    image = og_image['content']
    title = og_title['content']
    description = name_description['content']
    doc = {
        'image' : image,
        'title' : title,
        'description' : description,
        'star' : star_receive,
        'comment' : comment_receive,   
    }
    db.movies.insert_one(doc)
    return jsonify({'msg': 'POST requests'})

@app.route('/movie', methods=['GET'])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies': movie_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)