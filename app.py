import os
from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

REPO_URL = "https://github.com/Jebachu/viikko4-replica"


def read_visits():
    conn = mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )
    try:
        cursor = conn.cursor()
        # Read only: this page never changes the database
        cursor.execute("SELECT visits FROM counter WHERE id = 1")
        visits = cursor.fetchone()[0]
        cursor.close()
        return visits
    finally:
        conn.close()


PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Week 4 - Read-only replica</title>
  <style>
    body { max-width: 800px; margin: 40px auto; padding: 0 20px;
           font-family: sans-serif; line-height: 1.6;
           background: #121820; color: #d8e2ec; }
    h1, h2 { color: #4fc3f7; }
    a { color: #4fc3f7; }
    .banner { background: #3a2a10; border: 1px solid #f9a825;
              color: #ffd180; padding: 12px 16px; border-radius: 8px; }
    .counter { text-align: center; background: #1c2733;
               border-radius: 12px; padding: 24px; margin: 24px 0; }
    .number { font-size: 4rem; font-weight: bold; color: #4fc3f7; }
  </style>
</head>
<body>
  <h1>Server B: read-only replica</h1>
  <p class="banner">This page is a <strong>read-only replica</strong>.
     Loading it does not change the counter. The value is read from
     the local replicated database on server B.</p>
  <div class="counter">
    <div>Visitor counter replicated from server A</div>
    <div class="number">{{ visits }}</div>
  </div>
  <p>Server A (counter increases on every load):
     <a href="http://195.148.23.142/viikko2">http://195.148.23.142/viikko2</a></p>
  <p>Source code: <a href="{{ repo_url }}">{{ repo_url }}</a></p>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(PAGE, visits=read_visits(), repo_url=REPO_URL)
