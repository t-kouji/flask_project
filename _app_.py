from flask  import Flask,render_template,request,redirect,url_for
import json

#アプリオブジェクトの作成
app = Flask(__name__)

#プロフィール用jsonファイルのパス
file_json = "data/profile.json"

def get_profile():
    """
    "data/profile.json"の内容を取得し、json形式から辞書型へ変更
    """
    with open(file_json,encoding='utf-8') as prof:
        #jsonファイルの内容を取得
        # json_str = prof.read()
        prof_dict = json.load(prof)

        """
        ↓これでも同じ。「load」でなく「loads」
        json_str = prof.read()
        prof_dict = json.loads(json_str) 
        """
    return prof_dict

def update_profile(prof):
    #edit.htmlに紐づくプロフィールのupdateに関する関数。
    with open(file_json,"w",encoding='utf-8') as f:
        json.dump(prof,f) #json.dumpの第一引数、第二引数の関係は？
    

#ルーティング
@app.route('/')
def hello_func():
    name = "Hello World"
    return name

# @app.route('/profile')
# def profile():
#     return "name:Kouji Tanaka  address:Tokyo"

@app.route('/hive')
def hive_func():
    return render_template('index.html')

@app.route('/var')
def var_func():
    msg = 'aaa'
    return render_template('var.html',_message_ = msg)

@app.route('/greeting')
def greet_func():
    greeting_list = ["good morning","hello","good evening","good night"]
    return render_template('greeting.html', list_ = greeting_list)

@app.route('/fizzbuzz')
def fizzbuzz_func():
    num = 150
    return render_template('fizzbuzz.html',number = num)

@app.route('/get')
def get_func():
    #GETリクエストを格納。nにGETで取得した値を格納し、get.htmlの{{na}}に渡す。
    if type(request.args.get("number")) == str:
        number = int(request.args.get("number"))
        if number == 2:
            judge = True
        else:
            for i in range(2,number):
                if number % i== 0:
                    judge = False
                    break
                elif number == i+1:
                    judge = True
                    break

        return render_template('prime_number.html',title='prime number',ju = judge,nu = number)


    else:
        n = request.args.get("name") #.get("hoge")ここのhogeは『URL?パラメータ名=値』の所のパラメータ名の部分。
        return render_template('get.html',title='Flask GET request!',na = n)

@app.route('/profile')
def profile_func():
    prof_dict = get_profile()
    return render_template('profile.html',title= "json",user=prof_dict)

@app.route('/edit')
def edit_func():
    prof_dict = get_profile()
    return render_template('edit.html',title= "json",user=prof_dict)

@app.route('/update',methods=['POST']) #?第二引数の書き方がよくわからん。
def update_func():
    prof_dict = get_profile()
    
    #以下でprof_dictの値を変更
    """htmlのformのデータをうけとるのにrequest.formを使えます。
    ディクショナリで、key(name)とvalue(データ)をくれます。
    参考→https://qiita.com/nagataaaas/items/3116352da186df102d96
    or https://blog.mktia.com/send-post-request-and-retrieve-it-using-python/"""
    
    prof_dict["name"] = request.form["name"]
    prof_dict['age'] = request.form["age"]
    prof_dict["sex"] = request.form["sex"]


    update_profile(prof_dict)
    # def update_profile(prof):のprofに上記でupdateしたprof_dictの値を代入し、
    # update_profile関数が実行される。


    #url_for( func_name, keyword_args )…特定の関数に対応するURLを生成するメソッド
    # return redirect(url_for("profile_func"))
    #↓でも可能。どちらがいいのかわからん。
    return render_template("profile.html",user=prof_dict)

if __name__ == "__main__":
    app.run(debug=True)