from flask import Flask,\
                  render_template,\
                  url_for,\
                  request,\
                  flash,\
                  redirect
import psycopg2

import sql_scripts
from utils import *
from datetime import date

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


@app.route('/db_state/')
def db_state():
   cur, con, connection = get_cursor()
   db = get_whole_database()
   eksponaty = get_eksponaty()

   return render_template('db_state.html',
                          connection=connection,
                          eksponaty=eksponaty,
                          artysci=db['artysta'],
                          galerie=db['galeria'],
                          instytucje=db['instytucja'],
                          wystawienie=db['wystawienie'],
                          wypozyczenie=db['wypozyczenie'])


@app.route('/', methods=['GET', 'POST'])
def index():
   cur, con, connection = get_cursor()
   
   view_data = []
   try:
      view_data = get_view()
   except Exception:
      pass

   if request.method == 'POST':
      if request.form.get('login') == 'muzeum' and request.form.get('password') == 'admin':
         return redirect(url_for('admin'))
      else:
         flash('Błędny login/hasło!')

   return render_template('view.html',
                          connection=connection,
                          view_data=view_data)


@app.route('/insert/', methods=['GET', 'POST'])
def insert():
   cur, con, connection = get_cursor()

   if request.method == 'POST':
      if request.form.get('dodaj_eksponat'):
         next_eksponat_id = get_next_free_id('eksponat')
         next_artysta_id = get_next_free_id('artysta')

         eksponat_form = dict(request.form)
         print(eksponat_form)
         
         try:
            if request.form['nowy_artysta'] == 'yes':
               eksponat_form['id'] = next_eksponat_id
               eksponat_form['artysta_id'] = next_artysta_id
               add_to_artysta(eksponat_form)
               add_to_eksponat(eksponat_form)
            if request.form['nowy_artysta'] == 'no':
               eksponat_form['id'] = next_eksponat_id
               if eksponat_form['artysta_id'] == 'Artysta Nieznany':
                  eksponat_form['artysta_id'] = ''
               add_to_eksponat(eksponat_form)

            flash('Pomyślnie dodano eksponat!')
         except Exception as e:
            print(e)
            flash(e)

      if request.form.get('dodaj_galerie'):
         next_galeria_id = get_next_free_id('galeria')

         galeria_form = dict(request.form)
         galeria_form['id'] = next_galeria_id

         print(galeria_form)

         try:
            add_to_galeria(galeria_form)
            flash('Pomyślnie dodano Galerię!')
         except Exception as e:
            print(e)
            flash(e)

      if request.form.get('dodaj_instytucje'):
         next_instytucja_id = get_next_free_id('instytucja')

         instytucja_form = dict(request.form)
         instytucja_form['id'] = next_instytucja_id

         print(instytucja_form)

         try:
            add_to_instytucja(instytucja_form)
            flash('Pomyślnie dodano Instytucję!')
         except Exception as e:
            print(e)
            flash(e)
      
   db = get_whole_database()

   return render_template('insert.html',
                          connection=connection,
                          artysci=db['artysta'])


@app.route("/eksponat_transfer/<int:eksponat_id>", methods=['GET', 'POST'])
def eksponat_transfer(eksponat_id):
   cur, con, connection = get_cursor()

   if request.method == 'POST':
      if request.form.get('dodaj_wystawienie'):
         next_wystawienie_id = get_next_free_id('wystawienie')

         wystawienie_form = dict(request.form)
         wystawienie_form['id'] = next_wystawienie_id
         wystawienie_form['id_eksponatu'] = eksponat_id

         print(wystawienie_form)

         try:
            add_to_wystawienie(wystawienie_form)
            flash('Pomyślnie dodano wystawienie!')
         except Exception as e:
            print(e)
            flash(e)

      if request.form.get('dodaj_wypozyczenie'):
         next_wypozyczenie_id = get_next_free_id('wypozyczenie')

         wypozyczenie_form = dict(request.form)
         wypozyczenie_form['id'] = next_wypozyczenie_id
         wypozyczenie_form['id_eksponatu'] = eksponat_id

         print(wypozyczenie_form)

         try:
            add_to_wypozyczenie(wypozyczenie_form)
            flash('Pomyślnie dodano wypozyczenie!')
         except Exception as e:
            print(e)
            flash(e)


   db = get_whole_database()
   eksponaty_with_artysta = get_eksponaty_with_artysta()
   historia_wypozyczen = get_wypozyczenia_history(eksponat_id)
   historia_wystawien = get_wystawienia_history(eksponat_id)
   stan = get_current_state(eksponat_id, date.today())
   eksponat_name = get_eksponat_name(eksponat_id)
   print(eksponat_name)

   return render_template("eksponat_transfer.html",
                           connection=connection,
                           id=eksponat_id,
                           eksponat_name=eksponat_name,
                           eksponaty=eksponaty_with_artysta,
                           historia_wyp=historia_wypozyczen,
                           historia_wyst=historia_wystawien,
                           stan=stan,
                           artysci=db['artysta'],
                           galerie=db['galeria'],
                           instytucje=db['instytucja'],
                           wystawienie=db['wystawienie'],
                           wypozyczenie=db['wypozyczenie'])
                           



@app.route('/transfers/')
def transfers():
   cur, con, connection = get_cursor()

   eksponaty_with_artysta = get_eksponaty_with_artysta()

   return render_template('transfers.html',
                          connection=connection,
                          eksponaty=eksponaty_with_artysta)



@app.route('/admin/', methods=['GET', 'POST'])
def admin():
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

   view_data = []
   try:
      view_data = get_view()
   except Exception:
      pass
         
   return render_template('start.html',
                          connection=connection,
                          tables=get_visible_tables(),
                          db_correct=check_if_tables_present(),
                          view_data=view_data)

if __name__ == "__main__":
   app.run(debug=True)

