import sqlite3
from flask import Flask,render_template,request,g

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        # データベースへの接続をFlaskのグローバル変数に保存
        g.db = sqlite3.connect('data.db')
    return g.db

@app.route('/')
def index():
    # データベースを開く
    con = get_db()
    cur = con.cursor()

    # テーブル「items」の有無を確認して存在しなければ作成する
    sql = '''\
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  word TEXT,
  mean TEXT
  )\
    '''
    cur.execute(sql)
    con.commit()

    # データベースを閉じる
    con.close()

    # トップページの表示
    return render_template('index.html')

@app.route('/all_data')
def all_data():
    # データベースを開く
    con = get_db()
    cur = con.cursor()

    # SQLを実行：データ全件表示
    sql = "SELECT * FROM items ORDER BY id DESC"
    rows = cur.execute(sql)
    data = rows.fetchall()

    # データベースを閉じる
    con.close()

    # 検索結果ページの表示
    return render_template('search.html', data = data)

@app.route('/search', methods=["POST"])
def search_post():
    # 検索フォームから検索する単語（in_word）と意味（in_mean）を取得
    in_word = request.form["in_word"]
    in_mean = request.form["in_mean"]

    # 入力データの判定：データが無ければエラーページを表示
    if not ( in_word or in_mean ):
        return render_template('error.html')

    # データベースを開く
    con = get_db()
    cur = con.cursor()

    # SQLを実行：単語（in_word）および意味（in_mean）で検索する
    sql = "SELECT * FROM items WHERE word LIKE ? AND mean LIKE ? ORDER BY id DESC LIMIT 10"
    rows = cur.execute(sql, ('%' + in_word + '%', '%' + in_mean + '%'))
    data = rows.fetchall()

    # データベースを閉じる
    con.close()

    # 検索結果ページの表示
    return render_template('search.html', data = data)

@app.route('/insert', methods=["GET"])
def insert():
    # データ入力ページの表示
    return render_template('insert.html')

@app.route('/insert', methods=["POST"])
def inserted_post():
    # データ入力ページから新規登録する単語（in_word）と意味（in_mean）を取得
    in_word = request.form["in_word"]
    in_mean = request.form["in_mean"]

    # 入力データの判定：データが無ければエラーページを表示
    if not ( in_word or in_mean ):
        return render_template('error.html')

    # データベースを開く
    con = get_db()
    cur = con.cursor()

    # SQLを実行：登録処理
    sql = "INSERT INTO items (word, mean) VALUES (?, ?)"
    cur.execute(sql, (in_word, in_mean))
    con.commit()

    # データベースを閉じる
    con.close()

    # 編集完了通知ページの表示
    return render_template('result.html')

@app.route('/update', methods=["POST"])
def update_post():
    # 検索結果ページから編集するデータの番号（in_id）を取得
    in_id = request.form["in_id"]

    # データベースを開く
    con = get_db()
    cur = con.cursor()

    # SQLを実行：番号（id）で検索する
    sql = "SELECT * FROM items WHERE id = ?"
    rows = cur.execute(sql, (in_id,))
    data = rows.fetchall()

    # データベースを閉じる
    con.close()

    # データ編集ページの表示
    return render_template('update.html', data = data)

@app.route('/updated', methods=["POST"])
def updated_post():
    # データ編集ページから更新するデータの番号（in_id）, 単語（in_word）, 意味（in_mean）を取得
    in_id = request.form["in_id"]
    in_word = request.form["in_word"]
    in_mean = request.form["in_mean"]

    # 入力データの判定：データが無ければエラーページを表示
    if not ( in_word or in_mean ):
        return render_template('error.html')

    # データベースを開く
    con = get_db()
    cur = con.cursor()

    # SQLを実行：更新処理
    sql = "UPDATE items SET word = ?, mean = ? WHERE id = ?"
    cur.execute(sql, (in_word, in_mean, in_id))
    con.commit()

    # データベースを閉じる
    con.close()

    # 編集完了通知ページの表示
    return render_template('result.html')

@app.route('/delete', methods=["POST"])
def delete_post():
    # 検索結果ページから削除するデータの番号（in_id）を取得
    in_id = request.form["in_id"]

    # データベースを開く
    con = get_db()
    cur = con.cursor()

    # SQLを実行：番号（id）で検索する
    sql = "SELECT * FROM items WHERE id = ?"
    rows = cur.execute(sql, (in_id,))
    data = rows.fetchall()

    # データベースを閉じる
    con.close()

    # データ削除ページの表示
    return render_template('delete.html', data = data)

@app.route('/deleted', methods=["POST"])
def deleted_post():
    # データ削除ページから削除するデータの番号（in_id）を取得
    in_id = request.form["in_id"]

    # データベースを開く
    con = get_db()
    cur = con.cursor()

    # SQLを実行：削除処理
    sql = "DELETE FROM items WHERE id = ?"
    cur.execute(sql, (in_id))
    con.commit()

    # データベースを閉じる
    con.close()

    # 編集完了通知ページの表示
    return render_template('result.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
