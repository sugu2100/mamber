import sqlite3

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

def create_table():
    conn = getconn()
    cur = conn.cursor()
    sql = """
    CREATE TABLE member(
        mid CHAR(5) PRIMARY KEY,
        passwd CHAR(8) NOT NULL,
        name TEXT NOT NULL,
        age INTEGER,
        regDate DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    cur.execute(sql)
    conn.commit()
    print("member 테이블 생성!!")
    conn.close()

def insert_member():
    conn = getconn()
    cur = conn.cursor()
    sql = "INSERT INTO member(mid, passwd, name, age) VALUES (?, ?, ?, ?)"
    cur.execute(sql, ('10002', 'm1234', '팥쥐', 19 ))
    conn.commit()
    print("멤버 추가")
    conn.close()

def select_member():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall()   #DB에서 반환된 자료
    print(rs)
    for i in rs:
        print(i[0])
    conn.close()

#create_table()  #호출
insert_member()
select_member()