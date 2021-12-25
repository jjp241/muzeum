import psycopg2
import psycopg2.extras

import sql_scripts

TABLE_NAMES = ['artysta', 'galeria', 'eksponat', 'instytucja',\
               'magazynowanie', 'wypozyczenie', 'wystawienie']

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


def form_to_values(form_dict):
   TO_INT = ['id', 'wysokosc', 'szerokosc', 'waga', 'artysta_id']

   for col in TO_INT:
      if col in form_dict:
         form_dict[col] = int(form_dict[col])

   return tuple(list(form_dict.values())[:-1])


def add_to_db(table, values):
   cur, con, connection = get_cursor()

   script = f'INSERT INTO {table} VALUES {values};'
   cur.execute(script)
   con.commit()
