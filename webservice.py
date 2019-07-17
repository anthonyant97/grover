from flask import Flask, render_template, request, url_for
from grover import grover
import json

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/start")
def start():
    return render_template('start.html')

@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        data = request.get_json(force=True)
        
        dataset = data['dataset']
        dataset_temp = dataset.split(',')
        target = data['target']
        if(target[0] == "'"):
            target_filter = target[1]
        else:
            target_filter = int(target)
        dataset_filter = []
        i = 0
        j = 0
        while i < len(dataset):
            if dataset[i] == "'":
                dataset_filter.append(dataset[i+1])
                i = i+2
                j = j+1
            elif dataset[i] != ",":
                data = int(dataset_temp[j])
                dataset_filter.append(data)
                i = i+len(dataset_temp[j])
                j = j+1
            i = i+1
        if target_filter in dataset_filter:
            return grover(dataset_filter, target_filter)
        raise Exception
    return json.dumps({"binary": 0, "qubit": 0, "result": 0, "found": False})
    
@app.route("/credits")
def credit():
    return render_template('credits.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002, debug=True)