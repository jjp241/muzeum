from flask import Flask,\
                  render_template,\
                  url_for,\
                  request,\
                  flash
import psycopg2

import sql_scripts
from utils import get_cursor

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = "2b3f12f3ef12a6c86b"


@app.route('/erd/')
def erd():
   return render_template('erd.html')


@app.route('/script/')
def script():
   return render_template('script.html',
                          init_script=sql_scripts.DB_INIT)


@app.route('/', methods=['GET', 'POST'])
def index():
   cur, con, connection = get_cursor()

   if request.method == 'POST':
      if request.form.get('create'):
         cur.execute(sql_scripts.DB_INIT)   
         con.commit()
         flash('Pomyślnie utworzono bazę!')
      elif  request.form.get('drop'):
         cur.execute(sql_scripts.DROP_DB)
         con.commit()
         flash('Tabele usunięte!')

   visible_tables = []

   if connection:
      cur.execute(sql_scripts.LIST_TABLES)   

      visible_tables = cur.fetchall()
      visible_tables = list(sum(visible_tables, ())) # dziwna sztuczka na "spłasczenie listy"

   return render_template('start.html',
                          connection=connection,
                          tables=visible_tables)

if __name__ == "__main__":
   app.run(debug=True)

