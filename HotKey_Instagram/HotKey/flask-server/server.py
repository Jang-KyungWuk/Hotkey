from flask import Flask, jsonify, request, g, render_template
# customized modules import (사용 라이브러리들 포함)
from crawling import *
from db import *
from analyze import *
import os
import shutil
#from visualization import *
from preprocess import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 한글 깨짐 방지 (jsonify 사용시)

# single_search시, before_request (+ + showaccount, checkavail, keywordsearch(test) 시에도 사용해야함!!!)


@app.route('/')
def home():
    return 'This is the backend server for HOTKEY project__...'


@app.route('/trend_client')
def trend_client():
    trendlist = trend_crawler_client()
    return jsonify(trendlist)


@app.route('/keyword_search/<keyword>')
def keyword_search(keyword):
    g.thread = keyword
    # (true, tid), (false, tid)만 반환
    # 대소문자 구분, 띄어쓰기 예외처리해야함!!!
    print('keyword_search 실행, enforce = False, keyword :', keyword)
    status, tid = single_search(keyword)
    if not status:
        return jsonify({'status': status, 'tid': tid})
    time.sleep(2)  # DB에서 온 경우, 지나치게 빨리 return되는것을 방지 ㅠ
    print('keyword_search 완료 : 가용중 세션 로그아웃 및 DB 업로드')
    for s in g.acc_inuse:
        logout(s['session'])
        g.total_acc_info[g.mapping[s['aid']]]['in_use'] = False
    conn, cur = access_db()
    # 트랜잭션 시작
    cur.execute('set autocommit=0;')
    cur.execute('set session transaction isolation level serializable;')
    cur.execute('start transaction;')
    stat = set_accounts(cur)
    if not stat:
        set_accounts(cur)
    close_db(conn)
    # 트랜잭션끝
    return jsonify({'status': status, 'tid': tid})


@app.route('/analyze/<tid>')
def analyze(tid):
    # tid를 받아서 분석 후 결과를 jsonify해서 프론트로전달 (이미지의 경우, 경로를 react-client안에 넣어두기?)
    print("analyze API 실행")
    print("get_image 실행")
    status, images = get_image(tid)

    time.sleep(3)  # 임시 sleep => 코드 수정시 삭제
    # 임시 요청응답, images : filedir 리스트
    # 분석 결과는 json형태로전달, 1209 : images만 일단 반환

    return jsonify({'status': status, 'images': images})

# 실제 검색 -> 크롤링 -> 분석 -> 결과보여주는 API구현할때 무조건 before_search, after_search실행시켜줘야함!! + showaccount, checkavail, keywordsearch(test)
# ---------------------------관리/테스트용 API-------------------------------


@app.route('/manage/accounts')
# 현재 전역변수로 저장된 계정 정보를 보여준다.
def show_accounts():
    print('show_accounts실행')
    conn, cur = access_db()
    g.total_acc_info, g.all_blocked = get_accounts(cur)
    close_db(conn)
    return jsonify({'all_blocked': g.all_blocked, 'total_acc_info': g.total_acc_info})


@app.route('/manage/check_avail')
# 관리용 코드, 차단된 계정에 대해 차단이 풀렸는지 확인 후 DB에 반영 (매뉴얼하게 실행)
def checkavail():
    conn, cur = access_db()
    # 트랜잭션실행
    cur.execute('set autocommit=0;')
    cur.execute('set session transaction isolation level serializable;')
    cur.execute('start transaction;')  # 트랜잭션 시작
    g.total_acc_info, g.all_blocked = get_accounts(cur)
    if (g.all_blocked == -1):
        print("checkavail_get_account DB 트랜잭션 에러...")
        return jsonify(-1)
    print('check_avail 실행 :')
    check_avail()
    status = set_accounts(cur)
    if not status:
        set_accounts(cur)
    close_db(conn)
    return jsonify('check_avail()실행 후 DB 반영 완료')


@app.route('/manage/delete_image')
def del_img():
    dir_path = '../react-client/public/top_imgs'
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # 폴더 포함, 내부 파일 모두 삭제
        print('top_imgs 폴더 삭제..')

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print('top_imgs 폴더 생성..')
    return jsonify(1)


@app.route('/manage/test/keyword_search/enforce/<keyword>')
def keyword_search2(keyword):
    # 대소문자 구분, 띄어쓰기 예외처리해야함!!!
    print('keyword_search 실행, enforce = True')
    status, tid = single_search(keyword, True)
    return jsonify({'status': status, 'tid': tid})

# 네트워크 불러오기


@app.route('/manage/test/network/<name>')
def network_ex(name):
    # 네트워크 예시보여주기
    print('네트워크 불러오기...')
    filename = './templates/networks/'+name
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

# 워드클라우드 테스트 -> 마스크 이미지, 경로 설정등 해줘야함..


@app.route('/manage/test/test')
def tttt():
    status, result = LDA_test()
    return jsonify({'status': status, 'result': result})

# top 이미지 받아오는 로직


@app.route('/manage/test/test2/<query>')
def ttttt(query):
    status, images = top_image(query)
    if not status:
        print('image못받아왔음')
        return jsonify(0)
    for idx, url in enumerate(images):
        filename = query+str(idx)
        save_path = '../react-client/src/top_imgs/'+filename+'.jpg'
        request.urlretrieve(url, save_path)
    return jsonify(1)


# ---------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=False)  # 배포시 디버그 옵션 없애야함, 크롤링 시 debug 옵션 False로 해두기..
