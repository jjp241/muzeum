import psycopg2

def get_cursor():
   ''' Zwraca parę: kursor, con, stan połączenia '''
   try:
      con = psycopg2.connect(host="lkdb", dbname="bd", user="scott", password="tiger")
      cur = con.cursor()
      return cur, con, True 
   except:
      return None, None, False 