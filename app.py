import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

@app.route('/')  #127.0.0.1:5000
def index():
    return render_template('index.html')
    #return "<h1>Welcome~ 방문을 환영합니다.</h1>"

@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall()   #db에서 검색한 데이터
    conn.close()
    return render_template('memberlist.html', rs=rs)

app.run(debug=True)