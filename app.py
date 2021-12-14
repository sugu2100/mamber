import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "rlarldyd"  #암호키 설정

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

@app.route('/')  #127.0.0.1:5000
def index():
    return render_template('index.html')

@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall()   #db에서 검색한 데이터
    conn.close()
    return render_template('memberlist.html', rs=rs)

@app.route('/member_view/<string:id>/')
def member_view(id):  #mid를 경로로 설정하고 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s' " % (id)
    cur.execute(sql)
    rs = cur.fetchone()  #해당 1개의 자료를 반환받음
    conn.close()
    return render_template('member_view.html', rs=rs)

@app.route('/register/', methods = ['GET', 'POST'])  #url 경로
def register():
    if request.method == 'POST':  # 'POST'는 반드시 대문자로 할 것
        # 자료 수집
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        #date = request.form['regDate']
        # 회원 가입
        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO member (mid, passwd, name, age) VALUES ('%s', '%s', '%s', %s) " \
             % (id, pwd, name, age)
        cur.execute(sql)   # 실행 함수
        conn.commit()      # 커밋 완료

        # 가입 후 자동 로그인
        sql = "SELECT * FROM member WHERE mid = '%s' " % (id)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        if rs:
            session['userID'] = id   # 자동 로그인시 세션 발급 필수
            return redirect(url_for('memberlist'))
    else:
        return render_template('register.html') #GET 방식

@app.route("/login/", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        # 자료 전달 받음
        id = request.form['mid']
        pwd = request.form['passwd']

        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s' " % (id, pwd)
        cur.execute(sql)
        rs = cur.fetchone() # db에서 찾은 데이터 가져옴
        conn.close()
        if rs:
            session['userID'] = id  # 세션 발급
            return redirect(url_for('index'))
        else:
            error = "아이디나 비밀번호가 일치하지 않습니다."
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/logout/')
def logout():
    #session.pop('userID')  #userID 세션 삭제
    session.clear()         # 전체의 세션 삭제
    return redirect(url_for('index'))

@app.route('/member_del/<string:id>/')   #삭제 url 생성
def member_del(id):  #mid를 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM member WHERE mid = '%s' " % (id)
    cur.execute(sql)  # 삭제 수행
    conn.commit()     # 수행 완료
    conn.close()
    return redirect(url_for('memberlist'))

@app.route('/member_edit/<string:id>/', methods = ['GET', 'POST'])
def member_edit(id):
    if request.method == "POST":
        #자료 넘겨 받음
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']

        #db 연결
        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE member SET passwd = '%s', name = '%s' , age = %s " \
              "WHERE mid = '%s' " % (pwd, name, age, id)
        cur.execute(sql)  # 실행 함수
        conn.commit()  # 커밋 완료
        conn.close()
        return redirect(url_for('member_view', id=id))  # member_view 해당 id로 이동
    else:
        # 회원 자료 가져오기
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' " % (id)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        return render_template('member_edit.html', rs=rs)

# 게시판 목록
@app.route('/boardlist/')
def boardlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board ORDER BY bno DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return render_template('boardlist.html', rs=rs)

@app.route('/writing/', methods = ['GET', 'POST'])
def writing():
    if request.method == "POST":
        #자료 전달받음
        title = request.form['title']
        content = request.form['content']
        mid = session.get('userID')  #글쓴이 - 로그인한 mid(세션 권한이 있음)

        #db에 글 추가
        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO board(title, content, mid) VALUES ('%s', '%s', '%s')" \
              % (title, content, mid)
        cur.execute(sql)
        conn.commit()
        print("게시글 추가")
        conn.close()
        return redirect(url_for('boardlist'))
    else:
        return render_template('writing.html')

# 게시글 상세보기
@app.route('/board_view/<int:bno>/')
def board_view(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board WHERE bno = %s" % (bno)
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    return render_template('board_view.html', rs=rs)

app.run(debug=True)