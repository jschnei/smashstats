from flask import Flask, render_template, request
import json

app = Flask(__name__)
        

@app.route("/", methods=['GET', 'POST'])
def main():
    data = json.load(open('static/data/allmatches.json','r'))
    return render_template('main.html', players=data['players'])

if __name__ == "__main__":
    app.run(debug=True)