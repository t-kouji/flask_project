from flask  import Flask,render_template,request
import json

#アプリオブジェクトの作成
app = Flask(__name__)

def get_profile():
    #jsonファイルの書き込み
    file_json = "data/profile.json"
    with open(file_json,encoding='utf-8') as prof:
        json_str = prof.read()
    
    #json形式から辞書型へ変換
    prof_dict = json.loads(json_str)
    return prof_dict

#ルーティング
@app.route('/')
def hello():
    name = "Hello World"
    return name

# @app.route('/profile')
# def profile():
#     return "name:Kouji Tanaka  address:Tokyo"

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

@app.route('/get')
def get():
    #GETリクエストを格納。nにGETで取得した値を格納し、get.htmlの{{na}}に渡す。
    n = request.args.get("name") #.get("hoge")ここのhogeは『URL?パラメータ名=値』の所のパラメータ名の部分。
    return render_template('get.html',title='Flask GET request!',na = n)

@app.route('/profile')
def profile():
    prof_dict = get_profile()
    return render_template('profile.html',title= "json",user=prof_dict)

@app.route('/edit')
def edit():
    prof_dict = get_profile()
    return render_template('edit.html',title= "json")

if __name__ == "__main__":
    app.run(debug=True)