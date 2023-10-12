from flask import Flask, request, redirect, render_template
import sqlite3
import random
import string

app = Flask(__name__)

# Database initialization and setup
conn = sqlite3.connect('urls.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT NOT NULL,
    short_url TEXT NOT NULL
)
''')
conn.commit()
conn.close()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form.get('long_url')
    
    # Check if the long URL already exists in the database
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT short_url FROM urls WHERE long_url = ?', (long_url,))
    row = cursor.fetchone()
    
    if row:
        short_url = row[0]
    else:
        short_url = generate_short_url()
        cursor.execute('INSERT INTO urls (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
        conn.commit()
    
    conn.close()
    return render_template('shortened.html', short_url=short_url, long_url=long_url)

@app.route('/<short_url>')
def redirect_to_original_url(short_url):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,))
    row = cursor.fetchone()
    
    if row:
        long_url = row[0]
        conn.close()
        return redirect(long_url)
    else:
        conn.close()
        return "URL not found", 404

@app.route('/list')
def list_urls():
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT short_url, long_url FROM urls')
    urls = cursor.fetchall()
    conn.close()
    return render_template('list.html', urls=urls)

if __name__ == '__main__':
    app.run()






