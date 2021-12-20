from flask import Flask, render_template, url_for
import psycopg2

app = Flask(__name__)

@app.route('/erd/')
def script():
   return render_template('erd.html')

@app.route('/')
def index():
   con = psycopg2.connect(host="lkdb", dbname="bd", user="scott", password="tiger")

   cur = con.cursor()
   cur.execute("SELECT * FROM naukowiec")

   rows = cur.fetchall()

   return render_template('start.html', things=rows)

if __name__ == '__main__':
   app.run(debug = True)