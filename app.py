from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
import requests
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components 

app = Flask(__name__)
app.vars = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():

  return render_template('stock_input.html')

@app.route('/graph', methods = ['GET','POST'])
def graph():
  
  app.vars["ticker"] = request.form["ticker"].upper()
  app.vars['type'] = request.form['graph_type']
  
  api_url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=20150101&date.lt=20160101&ticker=%s&api_key=B4hUXhXNio3Rk-kJxoRd' % app.vars['ticker']
  raw_data = requests.get(api_url)
  col = []
  col_n = len(raw_data.json()['datatable']['columns'])
  for i in range(col_n): 
    col.append(raw_data.json()['datatable']['columns'][i]['name'])
  df = pd.DataFrame(np.array(raw_data.json()['datatable']['data'])[:,0:14],columns=col)  
  df = df[['ticker', 'date', 'open', 'close', 'adj_open', 'adj_close']]
  df.date = pd.to_datetime(df.date)
  x = df.date
  y = df[[app.vars['type']]]
  #output_file("graph.html", autosave = True)
  plot = figure(title='Data from Quandle WIKI set', x_axis_label='date', x_axis_type='datetime')
  plot.line(x, y)
  #save(plot)
  script, div = components(plot)
  return render_template('graph.html', script = script, div = div)


if __name__ == '__main__':
  app.debug = True
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
