from flask import Flask, jsonify, request, g, render_template
# customized modules import (사용 라이브러리들 포함)
from crawling import *
from db import *
from analyze import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 한글 깨짐 방지 (jsonify 사용시)

# single_search시, before_request (+ + showaccount, checkavail, keywordsearch(test) 시에도 사용해야함!!!)


def before_search():
    # g객체에 할당 코드 (전역변수 할당 코드)
    # all_blocked : 계정이 전부 막혔는지, single_search()에서 활용!! -> 다 막혔으면 서비스가 안됨.
    g.total_acc_info, g.all_blocked = get_accounts()
    g.acc_inuse = list()
    print('before_search : DB 계정 정보 가져오기')
    # 여기까지 초기 할당

#single_search시, after_request


def after_search():
    print('after_search : 가용중 세션 로그아웃 및 DB 업로드')
    for s in g.acc_inuse:
        logout(s['session'])
        g.total_acc_info[g.mapping[s['aid']]]['in_use'] = False
    set_accounts()
    print('all_blocked :', g.all_blocked)


@app.route('/')
def home():
    return 'This is the backend server for HOTKEY project__...'


@app.route('/trend_client')
def trend_client():
    trendlist = trend_crawler_client()
    return jsonify(trendlist)


@app.route('/keyword_search/<keyword>')
def keyword_search(keyword):
    # (true, tid), (false, tid)만 반환
    # 대소문자 구분, 띄어쓰기 예외처리해야함!!!
    # 실행전 before_search
    before_search()
    print('keyword_search 실행, enforce = False')
    status, tid = single_search(keyword)
    # 실행 후 after_search
    after_search()
    time.sleep(2)  # DB에서 온 경우, 지나치게 빨리 return되는것을 방지 ㅠ
    return jsonify({'status': status, 'tid': tid})


@app.route('/analyze/<tid>')
def analyze(tid):
    # tid를 받아서 분석 후 결과를 jsonify해서 프론트로전달 (이미지의 경우, 경로를 react-client안에 넣어두기?)
    print("analyze API 실행")
    time.sleep(3)  # 임시 sleep => 코드 수정시 삭제
    return jsonify({'status': True, 'result': {}})  # 임시 요청응답 ㅇㅇ

# 실제 검색 -> 크롤링 -> 분석 -> 결과보여주는 API구현할때 무조건 before_search, after_search실행시켜줘야함!! + showaccount, checkavail, keywordsearch(test)
# ---------------------------관리/테스트용 API-------------------------------


@app.route('/manage/test/keyword_search/enforce/<keyword>')
def keyword_search2(keyword):
    # 대소문자 구분, 띄어쓰기 예외처리해야함!!!
    # 실행전 before_search
    before_search()
    print('keyword_search 실행, enforce = True')
    status, tid = single_search(keyword, True)
    # 실행 후 after_search
    after_search()
    return jsonify({'status': status, 'tid': tid})

# 네트워크 불러오기


@app.route('/manage/test/network/<name>')
def network_ex(name):
    # 네트워크 예시보여주기
    print('네트워크 불러오기...')
    filename = './templates/'+name
    with open(filename, 'r') as fp:
        html = fp.read()
    return html

# 네트워크 불러올때 js request 대처용 로직.. 나 천재


@app.route('/manage/test/network/lib/<a>/<b>')
def js(a, b):
    filedir = './lib/'+a+'/'+b
    with open(filedir, 'r', encoding='utf-8-sig') as fp:
        file = fp.read()
    return file


@app.route('/manage/accounts')
# 현재 전역변수로 저장된 계정 정보를 보여준다.
def show_accounts():
    # before_search실행
    before_search()
    print('show_accounts실행')
    # after_search실행
    after_search()
    return jsonify({'all_blocked': g.all_blocked, 'total_acc_info': g.total_acc_info})


@app.route('/manage/check_avail')
# 관리용 코드, 차단된 계정에 대해 차단이 풀렸는지 확인 후 DB에 반영 (매뉴얼하게 실행)
def checkavail():
    # before_search실행
    before_search()
    check_avail()
    # after_search실행
    after_search()
    return 'check_avail()실행 후 DB 반영 완료'


@app.route('/manage/test/test')
def tt():
    return 0


# ---------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)  # 배포시 디버그 옵션 없애야함, 크롤링 시 debug 옵션 False로 해두기..
