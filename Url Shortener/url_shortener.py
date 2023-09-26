import sqlite3
import string
import random
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# Initialize the SQLite database     
conn = sqlite3.connect('urls.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS url_mappings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT,
        short_url TEXT
    )
''')
conn.commit()
conn.close()

# Function to generate a random short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for i in range(6))
    return short_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['original_url']

    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    # Check if the URL already exists in the database
    cursor.execute('SELECT short_url FROM url_mappings WHERE original_url = ?', (original_url,))
    existing_short_url = cursor.fetchone()

    if existing_short_url:
        conn.close()
        return render_template('index.html', short_url=existing_short_url[0])

    short_url = generate_short_url()

    # Insert the URL into the database
    cursor.execute('INSERT INTO url_mappings (original_url, short_url) VALUES (?, ?)', (original_url, short_url))
    conn.commit()
    conn.close()

    return render_template('index.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_original_url(short_url):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    # Retrieve the original URL from the database
    cursor.execute('SELECT original_url FROM url_mappings WHERE short_url = ?', (short_url,))
    original_url = cursor.fetchone()
    conn.close()

    if original_url:
        return redirect(original_url[0])
    else:
        return "Short URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
