from flask import Flask, jsonify, request
# customized modules import (사용 라이브러리들 포함)
# from db import *
from crawling import *  # db 모듈 포함

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 한글 깨짐 방지 (jsonify 사용시)


# get, post 요청 처리하기
@app.route('/')
def home():
    return 'This is the backend server for HOTKEY project__...'


# ---------------------------관리/테스트용 API-------------------------------
@app.route('/manage/accounts')
# 현재 전역변수로에 저장된 accounts테이블의 정보를 보여준다.
def show_accounts():
    global all_blocked, total_acc_info
    return jsonify({'all_blocked': all_blocked, 'total_acc_info': total_acc_info})


@app.route('/manage/sessions')
# sessions 전역변수
def show_sessions():
    global acc_inuse, sessions
    tmp1 = copy.deepcopy(acc_inuse)
    tmp2 = copy.deepcopy(sessions)
    for i in tmp1:
        del i['session']
    for i in tmp2:
        del i['session']
    return jsonify({'acc_inuse': tmp1, 'sessions': tmp2})


@app.route('/manage/test/keyword_search', methods=['GET'])  # method = GET으로해서
#http://127.0.0.1:5000/manage/test/keyword_search?keyword=hello와 같이 사용
#빈 문자열은 받을 수 없음
def keyword_search():
    status, corpus, image = single_search(request.args.get('keyword'))
    return jsonify(status, corpus)


# ---------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)  # 배포시 디버그 옵션 없애야함.
