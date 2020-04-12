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
    #prof_listを定義
    prof_list=[]
    # executeメソッドでSQL文を実行する
    for i in c.execute('select * from persons'):
        # forループの+=で追加していく。
        prof_list += [{'id':i[0],'name':i[1],'age':i[2],'sex':i[3]}]
    # データベースへコミット。これで変更が反映される。    
    conn.commit()
    # データベースへのコネクションを閉じる。(必須)
    conn.close
    return prof_list

def update_profile(prof):
    """
    sqliteのテーブルを更新する関数
    """
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    #c.executeの第一引数の?部分に第二引数のタプル内の値が順に入る。
    #要素が１つのタプルを生成する場合、末尾にカンマが必要
    c.execute('UPDATE persons SET name=?,age=?,sex=? WHERE id=?',
    (prof['name'],prof['age'],prof['sex'],prof['id'])
    )
    conn.commit()
    conn.close()

def add_profile(add_dict_):
    """
    sqliteのテーブルにデータを追加する関数
    """
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    #c.executeの第一引数の?部分に第二引数のタプル内の値が順に入る。
    #要素が１つのタプルを生成する場合、末尾にカンマが必要
    c.execute('INSERT INTO persons (name,age,sex) VALUES(?,?,?)',
    (add_dict_['name'],add_dict_['age'],add_dict_['sex'])
    )
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
    prof_list = get_profile()
    return render_template('profile.html',title= "db",prof_list=prof_list)

@app.route('/add_')
def add_(): 
    return render_template('add_.html',title= "add_profile",)

@app.route('/add_/update',methods=['POST']) #?第二引数の書き方がよくわからん。
def add_func():
    add_dict = {}
    add_dict["name"] = request.form["name"]
    add_dict['age'] = request.form["age"]
    add_dict["sex"] = request.form["sex"]
    #add_profile(add_dict_)関数の引数add_dict_に上記add_dictを代入して実行。
    add_profile(add_dict)
    #url_for( func_name, keyword_args )…特定の関数に対応するURLを生成するメソッド
    return redirect(url_for("profile_func"))

@app.route('/edit/<edit_user_id>')
def edit_func(edit_user_id):
    prof_list = get_profile()
    for d in prof_list:
        if d['id'] == int(edit_user_id):
            return render_template('edit_.html',title= "db",edit_user_dict = d)

@app.route('/edit/update/<edit_id>',methods=['POST']) #?第二引数の書き方がよくわからん。
def update_func(edit_id):
    prof_list = get_profile()
    for d in prof_list:
        if d['id'] == int(edit_id):
            d["name"] = request.form["name"]
            d['age'] = request.form["age"]
            d["sex"] = request.form["sex"]
            #update_profile(prof)関数の引数profに上記dを代入して実行。
            update_profile(d)
    #url_for( func_name, keyword_args )…特定の関数に対応するURLを生成するメソッド
    return redirect(url_for("profile_func"))

if __name__ == "__main__":
    print(get_profile())
    app.run(debug=True)