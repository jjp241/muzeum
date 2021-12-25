from flask import Flask,\
                  render_template,\
                  url_for,\
                  request,\
                  flash
import psycopg2

import sql_scripts
from utils import *

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = "2b3f12f3ef12a6c86b"


@app.route('/erd/')
def erd():
   return render_template('erd.html',
                          db_correct=check_if_tables_present())


@app.route('/script/')
def script():
   return render_template('script.html',
                          init_script=sql_scripts.DB_INIT,
                          db_correct=check_if_tables_present())


@app.route('/view/')
def view():
   cur, con, connection = get_cursor()
   db = get_whole_database()
   
   return render_template('view.html',
                          connection=connection,
                          eksponaty=db['eksponat'],
                          artysci=db['artysta'],
                          galerie=db['galeria'],
                          instytucje=db['instytucja'],
                          magazynowanie=db['magazynowanie'],
                          wystawienie=db['wystawienie'],
                          wypozyczenie=db['wypozyczenie'])


@app.route('/insert/', methods=['GET', 'POST'])
def insert():
   cur, con, connection = get_cursor()

   if request.method == 'POST':
      if request.form.get('dodaj_eksponat'):

         eksponat_form = dict(request.form)
         
         try:
            add_to_db('eksponat', form_to_values(eksponat_form))
            flash('Pomyślnie dodano eksponat!')
         except Exception as e:
            flash(e)

   db = get_whole_database()

   return render_template('insert.html',
                          connection=connection,
                          artysci=db['artysta'])


@app.route('/transfers/')
def transfers():
   return render_template('transfers.html')



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
      elif  request.form.get('sample'):
         cur.execute(sql_scripts.DB_INIT)   
         con.commit()
         cur.execute(sql_scripts.DB_SAMPLE)
         con.commit()
         flash('Utworzono bazę z przykładowymi danymi!')
         
   return render_template('start.html',
                          connection=connection,
                          tables=get_visible_tables(),
                          db_correct=check_if_tables_present())

if __name__ == "__main__":
   app.run(debug=True)

