from flask import Flask, jsonify, request, g, render_template
# customized modules import (사용 라이브러리들 포함)
# from db import *
from crawling import *  # db 모듈 포함

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 한글 깨짐 방지 (jsonify 사용시)

#before_request로 전역변수 할당
@app.before_request
def getdb():
    ### g객체에 할당 코드 (전역변수 할당 코드)
    g.total_acc_info, g.all_blocked = get_accounts()  # all_blocked : 계정이 전부 막혔는지, single_search()에서 활용!! -> 다 막혔으면 서비스가 안됨.
    g.acc_inuse = list()
    print('before_request : DB정보 가져오기 성공')
    ####여기까지 초기 할당
@app.after_request
def afterrequest(response):
    print('after_request실행')
    for s in g.acc_inuse:
        logout(s['session'])
    set_accounts()
    print('all_blocked :', g.all_blocked, '\ntotal_acc_info :', g.total_acc_info)
    print('response :', response)
    return response

@app.route('/')
def home():
    return 'This is the backend server for HOTKEY project__...'

# ---------------------------관리/테스트용 API-------------------------------
@app.route('/manage/test/keyword_search/<keyword>')
def keyword_search(keyword):
    #한 글자 이상 입력하라고 client 단에서 예외처리해줘야함!! (#빈 문자열은 받을 수 없음)
    status, corpus, image = single_search(keyword)
    return jsonify(status, corpus)
@app.route('/manage/test/network')
def network_ex():
    #네트워크 예시보여주기
    return render_template('network.html')
@app.route('/manage/accounts')
# 현재 전역변수로 저장된 계정 정보를 보여준다.
def show_accounts():
    return jsonify({'all_blocked': g.all_blocked, 'total_acc_info': g.total_acc_info})
@app.route('/manage/check_avail')
#관리용 코드, 차단된 계정에 대해 차단이 풀렸는지 확인 후 DB에 반영 (매뉴얼하게 실행)
def checkavail():
    check_avail()
    return jsonify('check_avail()실행 후 DB 반영 완료')

# ---------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=False)  # 배포시 디버그 옵션 없애야함, 크롤링 시 debug 옵션 False로 해두기..