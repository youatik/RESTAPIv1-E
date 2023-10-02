from flask import Flask, render_template, redirect, url_for
from flask import Flask, request, render_template

import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_projet')
def add_projet():
    return render_template('add_projet.html')
@app.route('/submit-form', methods=['POST'])
def submit_form():

    code = request.form.get('code')
    description = request.form.get('description')

    data = {
        "code": code,
        "description": description
    }

    response = requests.post('http://127.0.0.1:5001/v1/projets', json=data)

    if response.status_code == 200:
        return redirect(url_for('result', message='Form submitted successfully'))
    else:
        return redirect(url_for('result', message='Form submission failed. Please try again'))

@app.route('/result')
def result():
    message = request.args.get('message', 'No message provided')

    return render_template('result.html', message=message)

@app.route('/get_projet')
def get_projet():
    response = requests.get("http://127.0.0.1:5001/v1/projets")

    if response.status_code == 200:
        projects = response.json()  # Parse the JSON data

        return render_template('get_projet.html', projects=projects)
    else:
        return render_template('get_projet.html', projects=[])

@app.route('/demande_info/<nom>')
def demande_info(nom):
    response = requests.get(f'http://127.0.0.1:5001/v1/demandes/nom/{nom}')

    if response.status_code == 200:
        demande = response.json()
        return render_template('demande_info.html', demande=demande)
    else:
        return "Failed to fetch demande information", 500

if __name__ == "__main__":
    app.run(port=5002)