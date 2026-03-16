from flask import Flask
import random
app = Flask(__name__)


@app.route('/')
def hello_gjmst():
    return 'Hello, GJMST!'


@app.route('/hello/<name>')
def hello_name(name):
    return f'Hello, {name}!'


students = ['한별','시환','재윤','현준','태란','성호']
@app.route('/random-hello')
def hello_random():
    return f'Hello, {random.choice(students)}!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9720)
