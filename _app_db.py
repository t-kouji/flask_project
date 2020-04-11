from flask  import Flask,render_template,request,redirect,url_for
import sqlite3

#アプリオブジェクトの作成
app = Flask(__name__)

def get_profile():
    """
    sqliteからデータを取り出す関数
    """
    #sqlite3のデータベースへ接続する
    conn = sqlite3.connect('profile.sqlite3')
    # sqliteを操作するカーソルオブジェクトを作成
    c = conn.cursor()
    # executeメソッドでSQL文を実行する
    for i in c.execute('select * from persons'):
        prof_dict={'name':i[1],'age':i[2],'sex':i[3]}
    # データベースへコミット。これで変更が反映される。    
    conn.commit()
    # データベースへのコネクションを閉じる。(必須)
    conn.close
    return prof_dict

def update_profile(prof):
    """
    sqliteのテーブルを更新する関数
    """
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    #c.executeの第一引数の?部分に第二引数のタプル内の値が順に入る。
    #要素が１つのタプルを生成する場合、末尾にカンマが必要
    c.execute('UPDATE persons SET name=?,age=?,sex=? WHERE id=1',
    (prof['name'],prof['age'],prof['sex']))
    conn.commit()
    conn.close()
    

#ルーティング
@app.route('/')
def hello_func():
    name = "Hello World"
    return name

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
    #GETリクエストを格納。numberにGETで取得した値を格納し、get.htmlの{{na}}に渡す。
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
    return render_template('profile.html',title= "db",user=prof_dict)

@app.route('/edit')
def edit_func():
    prof_dict = get_profile()
    return render_template('edit_.html',title= "db",edit_user = prof_dict)

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
    return redirect(url_for("profile_func"))
    #↓でも可能。ただし、edit_htmlで編集後のURLが"～/update"になる。↑は"～/profile"になる。
    # return render_template("profile.html",user=prof_dict)

if __name__ == "__main__":
    app.run(debug=True)