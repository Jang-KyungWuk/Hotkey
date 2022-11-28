from flask import Flask, jsonify, request
#customized modules import (사용 라이브러리들 포함)
#from db import *
from crawling import * #db 모듈 포함

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #한글 깨짐 방지 (jsonify 사용시)

# get, post 요청 처리하기
@app.route('/')
def home():
    return 'This is the backend server for HOTKEY project__...'

@app.route('/search') #method = GET으로해서
def search():
    #single search 알고리즘 실행 => 분석
    return '검색 및 분석 결과 리턴'

#---------------------------------------------------------------------
@app.route('/login') #로그인 체크용
def dd():
    return jsonify(login('kj10522002@korea.ac.kr', 'kj76081460!')[2])

@app.route('/db') #db연결 체크용.. 임시!
def db():
    conn, cur = access_db() #db access
    cur.execute('select image from images;')
    val = cur.fetchall()
    close_db(conn) #db close
    return jsonify(val)

if __name__ == '__main__':
    app.run(debug=True)