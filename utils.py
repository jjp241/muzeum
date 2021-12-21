import psycopg2

def get_cursor():
   ''' Zwraca parę: kursor, stan połączenia '''
   try:
      con = psycopg2.connect(host="lkdb", dbname="bd", user="scott", password="tiger")
      cur = con.cursor()
      return cur, True 
   except:
      return None, False 