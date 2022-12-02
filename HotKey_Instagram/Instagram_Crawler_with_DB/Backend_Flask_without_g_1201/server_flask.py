from flask import Flask, jsonify, request
# customized modules import (사용 라이브러리들 포함)
from crawling import *  # db 모듈 포함

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 한글 깨짐 방지 (jsonify 사용시)

# get, post 요청 처리하기
@app.route('/')
def home():
    return 'This is the backend server for HOTKEY project__...'
# ---------------------------관리/테스트용 API-------------------------------
@app.route('/manage/test/keyword_search', methods=['GET'])  # method = GET으로해서
#http://127.0.0.1:5000/manage/test/keyword_search?keyword=hello와 같이 사용
#빈 문자열은 받을 수 없음
def keyword_search():
    status, corpus, image = single_search(request.args.get('keyword'))
    return jsonify(status, corpus)
@app.route('/manage/accounts')
# 현재 전역변수로 저장된 계정 정보를 보여준다.
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

@app.route('/manage/logout_all')
#현재 생성된 모든 세션 강제로 로그아웃 시키고 acc_inuse에서 없앰.
def logout_all():
    global acc_inuse, sessions
    print('before :', acc_inuse)
    for a in acc_inuse :
        for s in sessions: #해당하는 세션 찾기
            if a['orig_idx'] == s['orig_idx']:
                s['session'] = Session() #새로운 세션으로 교체
                s['inuse'] = False
                s['logout'] = int(datetime.now().timestamp())
                s['usage'] = 0
                break
    acc_inuse = list()
    print('after :', acc_inuse)
    return '가용 중인 모든 세션 로그아웃 완료'

@app.route('/manage/gen_total_acc')
#db에서 업데이트된 계정정보를 받아와 전역변수에 할당
def gentotalacc():
    global total_acc_info, all_blocked
    total_acc_info, all_blocked = gen_total_acc()
    return 'DB 계정 정보 서버 전역변수에 반영 완료'
@app.route('/manage/to_db_total_acc')
#업데이트된 전역변수를 다시 디비에 할당
def todbtotalacc():
    to_db_total_acc()
    return '서버 전역변수 DB 계정 정보에 반영 완료'

@app.route('/mange/check_avail')
#매뉴얼하게 막힌 계정이 복구되었는지 다시 확인 후 디비에 반영
def checkavail():
    check_avail()
    return ('실행완료')

# ---------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)  # 배포시 디버그 옵션 없애야함, 크롤링 시 debug 옵션 False로 해두기..
