from flask  import Flask
from flask import render_template

#アプリオブジェクトの作成
app = Flask(__name__)

#ルーティング
@app.route('/')
def hello():
    name = "Hello World"
    return name

@app.route('/profile')
def profile():
    return "name:Kouji Tanaka  address:Tokyo"

@app.route('/hive')
def hive_func():
    return render_template('index.html')

@app.route('/var')
def var():
    msg = 'aaa'
    return render_template('var.html',_message_ = msg)

@app.route('/greeting')
def greet():
    greeting_list = ["good morning","hello","good evening","good night"]
    return render_template('greeting.html', list_ = greeting_list)

@app.route('/fizzbuzz')
def fizzbuzz():
    num = 150
    return render_template('fizzbuzz.html',number = num)

if __name__ == "__main__":
    app.run(debug=True)