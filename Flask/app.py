import json
from flask import Flask, request, render_template
from datetime import datetime
from flask import jsonify
import os

app =  Flask(__name__)
@app.route('/')
def home():
    day_of_week = datetime.today().strftime('%A')   
    current_time = datetime.now().strftime('%H:%M:%S')

    print(day_of_week)
    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)     

@app.route('/api')
def api():
    # Load the data from file.json
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'file.json')
        with open(json_path) as json_file:
            data = json.load(json_file)
            return jsonify(data)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
