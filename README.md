# Flask_単語帳
## 概要

- [Python](https://www.python.org)（[flask](https://flask.palletsprojects.com/)）および[SQLite](https://www.sqlite.org/index.html)データベースを用いたwebアプリケーションの叩き台
- Pythonの追加パッケージはflaskのみ：`pip3 install flask`（Linux, Mac），`pip install flask`（Windows）
- データベース機能はほぼ[CRUD](https://e-words.jp/w/CRUD.html)のみ
- 教材としての使用を想定しており，基本的な仕組みを理解しやすいよう作成しているつもり
- また，ローカル環境での使用のみ想定しており，webに公開した場合の安全性などには特に留意していない
- その他，いろいろツッコミどころはあるのだろうが，気にしない
- 作成時期：2023年11〜12月頃（その前からぐだぐだいじっていたが，今の形に落ち着いたのがこの時期）

## 機能

- SQLiteデータベースへの文字列データ（単語と意味）の追加，全件表示，検索，編集，削除
- まあ，結局これしかないわけで，あとは好きに機能追加するなり改良するなりしておくれ

## 使用法

1. ビルトインwebサーバの起動：`python3 app.py`（Linux, Mac），`py app.py`（Windows）
2. ブラウザからアクセス：`http://localhost:5000/`
3. データベースファイル（data.db）は自動で作成されるので何もしないでOK
4. データの入力，編集，検索など，適当にごにょごにょして遊ぶ
5. データをリセットしたい場合は，データベースファイル（data.db）を削除すれば良い
6. サーバ停止で終了：`Ctrl-C`
7. 以上

## テスト環境

下記の環境で動作を確認

- Debian GNU/Linux 9 (Stretch), Python 3.5
- Debian GNU/Linux 12 (Bookworm), Python 3.11
- MacOS Monterey, Python 3.12
- Windows 10, Python 3.11

## 参考資料
### Website

- [とほほのFlask入門](https://www.tohoho-web.com/ex/flask.html)（とほほのWWW入門）
- [Flaskの便利な使い方まとめ](https://qiita.com/bauer/items/70abcb68d3b00d0d1794)（Qiita）
- [Pythonでちょっと使えるデスクトップ英和辞書](https://news.mynavi.jp/techplus/article/zeropython-52/)（ゼロからはじめるPython）
- [【Python】Flask入門　データベース SQLite3を使用する](https://shigeblog221.com/flask-sqlite/)（しげっちBlog）

### 書籍

- 松浦健一郎・司ゆき『[Python［完全］入門](https://www.sbcr.jp/product/4815607647/)』SBクリエイティブ, 2021.1.

### CSSファイル

staticフォルダ内のcssファイル（markdown7.css）は下記より拝借しております

- https://github.com/sinnerschrader/markdown-css/tree/master
- https://jasonm23.github.io/markdown-css-themes/

## 改良案
### データの項目を増やす

書籍管理アプリにするとか

### 簡易的な全文検索機能を付ける

app.pyの編集：下記を追加

```Python
@app.route('/full_text_search', methods=["POST"])
def full_text_search_post():
    # 検索フォームから検索する文字列termを取得
    term = request.form["term"]

    # データベースを開く
    con = get_db()
    cur = con.cursor()

    # SQLの実行：文字列termで検索する
    sql = "SELECT id,word,mean FROM items WHERE word LIKE ? OR mean LIKE ? ORDER BY id DESC LIMIT 10"
    rows = cur.execute(sql, ('%' + term + '%', '%' + term + '%'))
    data = rows.fetchall()

    # データベースを閉じる
    con.close()

    # 検索結果ページの表示
    return render_template('search.html', data = data)
```

index.htmlの編集：下記を追加

```html
    <p>
      <form action='/full_text_search'>
        <label>
          文字
          <input type="text" name="term" />
        </label>
        <button type="submit" formmethod="POST">全文検索</button>
      </form>
    </p>
```

### 冗長な部分を修正する

GETとPOSTで分かれているデコレータを統合するとか

### その他

もう何も思いつかん
