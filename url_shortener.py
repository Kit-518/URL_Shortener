import random
import string
import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
shortened_urls = {}


def generate_short_url():
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choice(characters) for _ in range(6))
        if short_url not in shortened_urls:
            return short_url


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['url']
        short_url = generate_short_url()
        while long_url in shortened_urls[short_url]:
            short_url = generate_short_url()
        
        shortened_urls[short_url] = long_url
        with open('urls.json', 'w') as url_file:
            json.dump(shortened_urls, url_file)
        return f"Shortened URL: {request.host_url}{short_url}"

        # return render_template('index.html', short_url=short_url)
    return render_template('index.html')


@app.route('/<short_url>')
def redirect_to_url(short_url):
    long_url = shortened_urls.get(short_url, None)
    if long_url:
        return redirect(long_url)
    else:
        return render_template('404.html')


if __name__ == '__main__':
    try:
        with open('urls.json', 'r') as url_file:
            shortened_urls = json.load(url_file)
    except FileNotFoundError:
        print("No urls.json file found. Starting with an empty database.")
    app.run(debug=True)
