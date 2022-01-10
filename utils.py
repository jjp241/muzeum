import psycopg2
import psycopg2.extras

import sql_scripts

TABLE_NAMES = ['artysta', 'galeria', 'eksponat', 'instytucja',\
               'magazynowanie', 'wypozyczenie', 'wystawienie']

EKSPONAT_FIELDS = ['id', 'tytul', 'typ', 'wysokosc', 'szerokosc', 'waga', 'artysta_id']
ARTYSTA_FIELDS = ['id', 'imie', 'nazwisko', 'rok_urodzenia', 'rok_smierci']
GALERIA_FIELDS = ['id', 'nazwa', 'liczba_sal']

def get_cursor():
   ''' Zwraca parę: kursor, con, stan połączenia '''
   try:
      con = psycopg2.connect(host="lkdb", dbname="bd", user="scott", password="tiger")
      cur = con.cursor()
      return cur, con, True 
   except:
      return None, None, False 


def get_visible_tables():
   cur, con, connection = get_cursor()

   visible_tables = []

   if connection:
      cur.execute(sql_scripts.LIST_TABLES)   

      visible_tables = cur.fetchall()
      visible_tables = list(sum(visible_tables, ())) # dziwna sztuczka na "spłasczenie listy"
   
   return visible_tables


def check_if_tables_present():
   ''' Sprawdza czy wszystkie potrzebne tabele istnieją w bazie '''
   visible_tables = get_visible_tables()

   for table_name in TABLE_NAMES:
      if table_name not in visible_tables:
         return False 
   return True
   

def get_whole_database():
   ''' Zwraca wszystkie informacje zawarte w bazie danych '''
   db = {}
   cur, con, connection = get_cursor()

   if not connection:
      return db 

   # Change cursor to retrieve dicts
   # cur = con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

   cur.execute(sql_scripts.GET_EKSPONAT)
   db.update({'eksponat': cur.fetchall()})

   cur.execute(sql_scripts.GET_ARTYSTA)
   db.update({'artysta': cur.fetchall()})

   cur.execute(sql_scripts.GET_GALERIA)
   db.update({'galeria': cur.fetchall()})

   cur.execute(sql_scripts.GET_INSTYTUCJA)
   db.update({'instytucja': cur.fetchall()})

   cur.execute(sql_scripts.GET_MAGAZYNOWANIE)
   db.update({'magazynowanie': cur.fetchall()})

   cur.execute(sql_scripts.GET_WYPOZYCZENIE)
   db.update({'wypozyczenie': cur.fetchall()})

   cur.execute(sql_scripts.GET_WYSTAWIENIE)
   db.update({'wystawienie': cur.fetchall()})

   return db


def get_eksponaty_with_artysta():
   cur, con, connection = get_cursor()

   if not connection:
      return db 
   
   cur.execute(sql_scripts.GET_EKSPONAT_WITH_ARTYSTA)
   return cur.fetchall()


def get_next_free_id(table):
   db = get_whole_database()
   if len(db[table]) == 0:
      return 1
   else:
      ids = [int(row[0]) for row in db[table]]
      return max(ids) + 1
   

def fix_form_types(form_dict):
   TO_INT = ['id', 'wysokosc', 'szerokosc', 'waga', 'artysta_id']
   TO_DATE = ['rok_urodzenia', 'rok_smierci']

   for col in form_dict:
      if type(form_dict[col]) == str and len(form_dict[col]) == 0:
         form_dict[col] = None
 
   for col in TO_INT:
      if col in form_dict and form_dict[col] is not None:
         form_dict[col] = int(form_dict[col])


def form_to_values(form_dict):
   return tuple(list(form_dict.values()))


def add_to_eksponat(form_dict):
   eksponat_dict = {field: form_dict[field] for field in EKSPONAT_FIELDS}
   fix_form_types(eksponat_dict)

   print('eksponat dict: ')
   print(eksponat_dict)

   values = form_to_values(eksponat_dict)

   cur, con, connection = get_cursor()

   cur.execute(sql_scripts.ADD_TO_EKSPONAT, values)
   con.commit()


def add_to_artysta(form_dict):
   print('add to artysta')
   artysta_dict = {field: form_dict[field] for field in ARTYSTA_FIELDS}
   artysta_dict['id'] = form_dict['artysta_id']
   fix_form_types(artysta_dict)

   print('artysta dict:')
   print(artysta_dict)
   
   values = form_to_values(artysta_dict)

   cur, con, connection = get_cursor()

   cur.execute(sql_scripts.ADD_TO_ARTYSTA, values)
   con.commit()


def add_to_galeria(form_dict):
   print('add to galeria')
   galeria_dict = {field: form_dict[field] for field in GALERIA_FIELDS}
   fix_form_types(galeria_dict)

   print(galeria_dict)

   values = form_to_values(galeria_dict)
   cur, con, connection = get_cursor()

   cur.execute(sql_scripts.ADD_TO_GALERIA, values)
   con.commit()