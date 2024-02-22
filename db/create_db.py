import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def create_db():
    conn = sqlite3.connect('mercari.sqlite3')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category_id INTEGER,
                    image_name TEXT NOT NULL,
                    FOREIGN KEY(category_id) REFERENCES categories(id)
                 )''')

    c.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                 )''')

    conn.commit()
    conn.close()

def insert_item(name, category_id, image_name):
    conn = sqlite3.connect('mercari.sqlite3')
    c = conn.cursor()

    c.execute("INSERT INTO items (name, category_id, image_name) VALUES (?, ?, ?)", (name, category_id, image_name))

    conn.commit()
    conn.close()

def search_items(keyword):
    conn = sqlite3.connect('mercari.sqlite3')
    c = conn.cursor()

    c.execute("SELECT items.name, categories.name FROM items JOIN categories ON items.category_id = categories.id WHERE items.name LIKE ?", ('%' + keyword + '%',))
    items = c.fetchall()

    conn.close()

    return items

@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    items = search_items(keyword)
    return jsonify({'items': items})

if __name__ == "__main__":
    create_db()
    insert_item("jacket", 1, "j.jpg")
    app.run(debug=True)

