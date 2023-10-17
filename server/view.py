#!/usr/bin/python3

from flask import Flask, request, make_response, jsonify
import os
import funcs
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def hello():
    return "hello"

@app.route('/trigger',methods=['GET'] )
def trigger():
    try:
        record = funcs.shadow_analysis(datetime.now())
        response = make_response(jsonify(record), 200)
        return response
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
