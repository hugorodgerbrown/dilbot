# coding=utf-8
from datetime import date
import logging

from flask import Flask, jsonify

from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

DILBERT_STRIP_MASK = 'http://dilbert.com/strip/%s'


def get_comic_src(url):
    """Extract comic strip img src property from a URL."""
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    images = soup.select('.img-comic-container a img')
    return images[0].attrs['src']

@app.route("/dilbot")
def today():
    url = DILBERT_STRIP_MASK % date.today().strftime('%Y-%m-%d')
    try:
        src = get_comic_src(url)
        msg = "<a href='%s'><img src='%s'></a>" % (url, src)
        color = 'green'
    except:
        msg = "Couldn't find a strip at <a href='%s'>%s</a>" % (url, url)
        color = 'red'
        app.logger.error(msg)

    payload = {
        'color': color,
        'message': msg,
        'notify': False,
        'message_format': 'html'
    }
    return jsonify(payload)

if __name__ == "__main__":
    app.run()