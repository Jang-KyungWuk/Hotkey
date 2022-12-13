from flask import Flask, jsonify, request, g, render_template
# customized modules import (사용 라이브러리들 포함)
from crawling import *
from db import *
from analyze import *
import os
import shutil
#from visualization import *
from preprocess import *
import time

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
    used_list = []
    print('keyword_search 완료 : 가용중 세션 로그아웃 및 DB 업로드')
    for s in g.acc_inuse:
        used_list.append(g.mapping[s['aid']])
        logout(s['session'])
        g.total_acc_info[g.mapping[s['aid']]]['in_use'] = False
    # 트랜잭션 시작, 사용하고 남은 세션에 대해서만 업데이트를 진행
    try:
        conn, cur = access_db()
        cur.execute('set autocommit=0;')
        cur.execute('set session transaction isolation level serializable;')
        cur.execute('start transaction;')
        for idx, row in enumerate(g.total_acc_info):
            if idx in used_list:
                cur.execute('update accounts set blocked=(%s), up_date=(%s), last_used=(%s), in_use=(%s) where id=(%s);',
                            (1 if row['blocked'] == True else 0, str(time.strftime('%Y-%m-%d %H:%M:%S')), row['last_used'], 1 if row['in_use'] == True else 0, row['id']))
        close_db(conn)
    except:
        conn, cur = access_db()
        for idx, row in enumerate(g.total_acc_info):
            if idx in used_list:
                cur.execute('update accounts set blocked=(%s), up_date=(%s), last_used=(%s), in_use=(%s) where id=(%s);',
                            (1 if row['blocked'] == True else 0, str(time.strftime('%Y-%m-%d %H:%M:%S')), row['last_used'], 1 if row['in_use'] == True else 0, row['id']))
        close_db(conn)

    # 트랜잭션끝
    return jsonify({'status': status, 'tid': tid})


@app.route('/analyze/<tid>')
def analyze(tid):
    # tid를 받아서 분석 후 결과를 jsonify해서 프론트로전달 (이미지의 경우, 경로를 react-client안에 넣어두기?)
    returnstatus = {'keyword': '', 'imagenum': 0, 'get_image': True, 'get_corpus': True, 'preprocess': True, 'wordcloud': True,
                    'barplot': True, 'lda': True, 'spam_filter': True, 'network': True, 'sent_analysis': True}
    print("analyze API 실행")
    print("get_image 실행")
    status, keyword, imagenum = get_image(tid)
    returnstatus['keyword'] = keyword
    returnstatus['imagenum'] = imagenum
    if not status:
        print('get_image 중 에러발생')
        returnstatus['get_image'] = False
    print("get_corpus 실행")
    status, keyword, corpus = get_corpus(tid)
    if not status:
        print('get_corpus 중 에러발생')
        returnstatus['get_corpus'] = False
    ################
    ################
    # wc, barplot 테스트 : spam_fitering되지 않은 corpus를 인풋으로 받아 안에서 전처리
    print("전처리함수 실행")
    try:
        pt = preprocess(plaintext=corpus, sep='HOTKEY123!@#')
    except:
        print("전처리 과정 중 에러... analysis API 종료")
        for i in returnstatus.keys():
            if i not in ['get_image', 'get_corpus']:
                returnstatus[i] = False
        return jsonify(returnstatus)
    print("전처리완료.. - 반환 : 리스트 형식")
    print("wordcloud 생성 시작")
    status = wordcloud(
        pt, wc_filename='../react-client/src/visualization/wordcloud/'+keyword+'.png')
    if not status:
        print('wordcloud 생성 중 에러...')
        returnstatus['wordcloud'] = False
    print("barplot 생성 시작")
    status = barplot(
        pt, bp_filename='../react-client/src/visualization/barplot/'+keyword+'.png')
    if not status:
        print('barplot 생성 중 에러..')
        returnstatus['barplot'] = False
    ################
    ################
    # LDA 테스트 : spam_filtering되지 않은 corpus를 인풋으로 받아 안에서 전처리
    print("LDA 분석 시작... (+토픽별 워드클라우드생성)")
    # original corpus를 인풋으로 받음
    status, lda_result = sklda(
        corpus, filedir='../react-client/src/visualization/lda_results/', keyword=keyword)
    print("LDA 분석 완료")
    if not status:
        print('LDA 분석 중 에러..')
        returnstatus['lda'] = False
    ################
    ################
    # spam_filtering된 결과는 network, sentiment_analysis에 들어감
    print("전처리함수 실행")
    pt, status = spam_filter(corpus)
    if not status:
        print('Error during spam_filtering...')
        returnstatus['spam_filter'] = False
        returnstatus['network'] = False
        returnstatus['sent_analysis'] = False
    else:
        print("전처리완료.. - 반환 : 코퍼스 형식")
        ################
        ################
        # 네트워크 테스트 : spam_filtering된 plaintext를 인풋으로 받음
        print("network 생성 시작... path : ./templates/networks")
        # 스팸필터링된 plaintext와 LDA 결과값을 인풋으로 받음
        status = network(pt, lda_result, saveFilename=keyword)
        if not status:
            print('Error during network analysis...')
            returnstatus['network'] = False
        ###############
        ###############
        # 감성분석 테스트 : spam_filtering된 plaintext를 인풋으로 받음
        print("sentiment analysis 시작... path : ../react-client/src/visualization/sent_results/")
        status = sent_analysis(pt, saveDir='../react-client/src/visualization/sent_results/',
                               fileName=keyword)  # 스팸필터링된 plaintext를 인풋으로 받음
        if not status:
            print('Error during sent_analysis...')
            returnstatus['sent_analysis'] = False
    print('분석 완료!')
    return jsonify(returnstatus)

# 실제 검색 -> 크롤링 -> 분석 -> 결과보여주는 API구현할때 무조건 before_search, after_search실행시켜줘야함!! + showaccount, checkavail, keywordsearch(test)
# ---------------------------관리/테스트용 API-------------------------------


@app.route('/manage/accounts')
# 현재 전역변수로 저장된 계정 정보를 보여준다.
def show_accounts():
    print('show_accounts실행')
    conn, cur = access_db()
    g.thread = 'manage/accounts'
    g.total_acc_info, g.all_blocked = get_accounts(cur)
    close_db(conn)
    return jsonify({'all_blocked': g.all_blocked, 'total_acc_info': g.total_acc_info})


@app.route('/manage/check_avail')
# 관리용 코드, 차단된 계정에 대해 차단이 풀렸는지 확인 후 DB에 반영 (매뉴얼하게 실행)
def checkavail():
    conn, cur = access_db()
    g.thread = 'manage/check_avail'
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
    g.thread = 'manage/keyword_search/enforce'
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


@app.route('/manage/test/<tid>')
def tttt(tid):
    status, keyword, corpus = get_corpus(tid)
    if not status:
        print('get_corpus 중 에러발생')
        return jsonify(-1)
    ################
    ################
    # wc, barplot 테스트 : spam_fitering되지 않은 corpus를 인풋으로 받아 안에서 전처리
    print("전처리함수 실행")
    pt = preprocess(plaintext=corpus, sep='HOTKEY123!@#')
    print("전처리완료.. - 반환 : 리스트 형식")
    print("wordcloud 생성 시작")
    status = wordcloud(
        pt, wc_filename='../react-client/src/visualization/wordcloud/tmp.png')
    if not status:
        print('wordcloud 생성 중 에러...')
        return jsonify(-1)
    print("barplot 생성 시작")
    status = barplot(
        pt, bp_filename='../react-client/src/visualization/barplot/tmp.png')
    if not status:
        print('barplot 생성 중 에러..')
        return jsonify(-1)
    ################
    ################
    # LDA 테스트 : spam_filtering되지 않은 corpus를 인풋으로 받아 안에서 전처리
    print("LDA 분석 시작... (+토픽별 워드클라우드생성)")
    # original corpus를 인풋으로 받음
    status, lda_result = sklda(
        corpus, filedir='../react-client/src/visualization/lda_results/', keyword=keyword)
    print("LDA 분석 완료")
    if not status:
        print('LDA 분석 중 에러..')
        return jsonify(-1)
    ################
    ################
    # spam_filtering된 결과는 network, sentiment_analysis에 들어감
    print("전처리함수 실행")
    pt, status = spam_filter(corpus)
    if not status:
        print('Error during spam_filtering...')
        return jsonify(-1)
    print("전처리완료.. - 반환 : 코퍼스 형식")
    ################
    ################
    # 네트워크 테스트 : spam_filtering된 plaintext를 인풋으로 받음
    print("network 생성 시작... path : ./templates/networks")
    status = network(pt, lda_result)  # 스팸필터링된 plaintext와 LDA 결과값을 인풋으로 받음
    if not status:
        print('Error during network analysis...')
        return jsonify(-1)
    ###############
    ###############
    # 감성분석 테스트 : spam_filtering된 plaintext를 인풋으로 받음
    print("sentiment analysis 시작... path : ../react-client/src/visualization/sent_results/")
    status = sent_analysis(pt, saveDir='../react-client/src/visualization/sent_results/',
                           fileName=keyword)  # 스팸필터링된 plaintext를 인풋으로 받음
    if not status:
        print('Error during sent_analysis...')
        return jsonify(-1)
    print('분석 완료!')
    return jsonify({'status': status, 'keyword': keyword, 'corpus': corpus, 'lda_result': lda_result})

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
