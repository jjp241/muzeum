from flask import Flask, render_template, url_for
import psycopg2

app = Flask(__name__)

@app.route('/erd/')
def script():
   return render_template('erd.html')

@app.route('/')
def index():
   return render_template('start.html')

if __name__ == '__main__':
   app.run(debug = True)