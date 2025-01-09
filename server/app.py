from flask import Flask, abort, flash, jsonify, redirect, render_template, request
import re
import hashlib
import redis

url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
server_address = "http://127.0.0.1:5000/"
app = Flask(__name__)
app.config.from_pyfile('instance/config.py') # Make sure you create a "instance/config.py" file to store your SECRET_KEY value
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def shorten_url():
    url = request.form.get('url')
    if(re.match(url_pattern, url)):
        hash, shortened_url = get_short_url(url)
        return render_template('index.html', hash=hash, shortened_url=shortened_url)
    flash('Invalid URL', 'error')
    return render_template('index.html')

@app.route('/<hash>', methods=['GET'])
def redirect_url(hash):
    full_url = get_full_url(hash)
    if full_url is None:
        abort(404)
    return redirect(full_url, code=302)

@app.route('/<hash>', methods=['DELETE'])
def delete_short_url(hash):
    full_url = get_full_url(hash)
    if full_url is None:
        abort(404)
    try:
        result = r.delete(hash)
    except Exception as e:
        print(f"Error deleting key '{hash}': {e}")
        return jsonify(message=f"Error deleting key '{hash}' "), 500
    if result > 0:
        return jsonify(message=f"Key '{hash}' deleted successfully"), 200
    return jsonify(message=f"Error deleting key '{hash}' "), 500

def generate_url_hash(url):
    hash_length = 8
    sha256_hash = hashlib.sha256(url.encode()).hexdigest()
    truncated_hash = sha256_hash[:hash_length]
    return truncated_hash

def get_short_url(full_url):
    hash = generate_url_hash(full_url)
    short_url = r.hget(hash, 'short_url')
    if short_url is None:
        short_url = server_address + hash
        r.hset(hash, 'full_url', full_url)
        r.hset(hash, 'short_url', short_url)
    print(short_url)
    return hash, short_url

def get_full_url(hash):
    return r.hget(hash, 'full_url')

if __name__ == '__main__':
    app.run(debug=True)