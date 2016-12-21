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
  if request.form['begin_date']:
    app.vars['begin_date'] = "".join(str(request.form['begin_date']).split("-"))
  else:
    app.vars['begin_date'] = "20000101"
  
  if request.form['end_date']:  
    app.vars['end_date'] = "".join(str(request.form['end_date']).split("-"))
  else:
    app.vars['end_date'] = "20161231"
  
  app.vars["ticker"] = request.form["ticker"].upper()
  app.vars['type'] = request.form['graph_type']
  
  api_url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=%s&date.lt=%s&ticker=%s&api_key=B4hUXhXNio3Rk-kJxoRd' % (app.vars['begin_date'], app.vars['end_date'], app.vars['ticker'])
  raw_data = requests.get(api_url)
  col = []
  col_n = len(raw_data.json()['datatable']['columns'])
  for i in range(col_n): 
    col.append(raw_data.json()['datatable']['columns'][i]['name'])
  df = pd.DataFrame(np.array(raw_data.json()['datatable']['data'])[:,:],columns=col)  
  df = df[['ticker', 'date', 'open', 'close', 'adj_open', 'adj_close']]
  df.date = pd.to_datetime(df.date)
  x = df.date
  y = df[[app.vars['type']]]
  
  plot = figure(title='Data from Quandle WIKI set', x_axis_label='date', x_axis_type='datetime')
  plot.line(x, y)
  script, div = components(plot)
  return render_template('graph.html', script = script, div = div)


if __name__ == '__main__':
  app.debug = True
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
  #app.run()
