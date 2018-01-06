from flask import Flask
from flask import request
from flask import jsonify
from StockPredict import main
import json
 
app = Flask(__name__)

@app.route('/')
def hello_world():
  symbol = request.args.get('symbol')
  compname = request.args.get('compname')
  val, rank = main(symbol)
  json_dict = {}
  json_dict['val'] = val
  json_dict['rank'] = rank
  #return json.dumps(json_dict)
  return jsonify(json_dict)
  
  
  

if __name__ == '__main__':
    app.run()