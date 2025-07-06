from flask import Flask, render_template
import requests, sqlite3, os

app = Flask(__name__)

DB_FILE = "chuckles.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS counter (id INTEGER PRIMARY KEY, count INTEGER)")
    c.execute("INSERT OR IGNORE INTO counter (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

def increment_counter():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE counter SET count = count + 1 WHERE id = 1")
    conn.commit()
    c.execute("SELECT count FROM counter WHERE id = 1")
    count = c.fetchone()[0]
    conn.close()
    return count

@app.route("/")
def index():
    init_db()
    joke = requests.get("https://api.chucknorris.io/jokes/random").json()["value"]
    count = increment_counter()
    return render_template("index.html", joke=joke, counter=count)

if __name__ == "__main__":
    app.run()
