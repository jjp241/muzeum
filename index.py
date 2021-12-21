from flask import Flask, render_template, url_for
import psycopg2

app = Flask(__name__, static_url_path='')

@app.route('/erd/')
def erd():
   return render_template('erd.html')

@app.route('/script/')
def script():
   return render_template('script.html')

def has_no_empty_params(rule):
   defaults = rule.defaults if rule.defaults is not None else ()
   arguments = rule.arguments if rule.arguments is not None else ()
   return len(defaults) >= len(arguments)

@app.route('/')
def index():
   links = []
   for rule in app.url_map.iter_rules():
      if "GET" in rule.methods and has_no_empty_params(rule):
         url = url_for(rule.endpoint, **(rule.defaults or {}))
         links.append((url, rule.endpoint))

   return render_template('start.html', links=links)

if __name__ == '__main__':
   app.run(debug = True)

