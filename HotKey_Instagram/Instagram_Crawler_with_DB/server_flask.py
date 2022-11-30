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

@app.route('/manage/accounts')
#현재 DB에 저장된 accounts테이블의 정보를 보여준다.
def show_accounts():
    acc_info, blocked = gen_total_acc()
    return jsonify(blocked, acc_info)

@app.route('/test') #method = GET으로해서
def search():
    status, corpus, image = single_search('한효주')
    return jsonify(status, corpus)

#---------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True) #배포시 디버그 옵션 없애야함.