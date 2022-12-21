from flask import Flask, jsonify, g, send_from_directory
from flask_cors import CORS
# customized modules import (사용 라이브러리들 포함)
from crawling import *
from db import *
from analyze import *
import os
import shutil
# from visualization import *
from preprocess import *
import time
import unicodedata

app = Flask(__name__)
CORS(app)
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
    # 대소문자 구분, 띄어쓰기 예외처리필요
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
    returnstatus = {'keyword': '', 'imagenum': 0, 'get_image': True,
                    'topic_num': 0, 'sent_result': [], 'status': True}
    bf = datetime.now()
    print("analyze API 실행")
    status, keyword, imagenum = get_image(tid)
    returnstatus['keyword'] = keyword
    returnstatus['imagenum'] = imagenum
    if not status:
        returnstatus['get_image'] = False
    print("1. get_image :", status)
    status, keyword, corpus = get_corpus(tid)
    if not status:
        print("get_corpus 실패.. return False")
        returnstatus['status'] = False
        return (jsonify(returnstatus))
    print("2. get_corpus :", status)
    ##################
    corpus = unicodedata.normalize('NFC', corpus)  # 자모음 분리현상 해결
    corpus = corpus.replace('⠀', '')
    corpus = corpus.replace('ㅤ', '')
    corpus = corpus.replace('　', '')
    # spt : spamfiltered plaintext
    spt, status = spam_filter(corpus)
    if not status:
        print("전처리 실패.. return False")
        returnstatus['status'] = False
        return (jsonify(returnstatus))
    try:
        tpt = data_tokenize(plain_structurize(
            spt), setMorphemeAnalyzer('okt'))  # 스팸필터링된 spt로 token화된 pt생성
    except:
        print("전처리 실패.. return False")
        returnstatus['status'] = False
        return (jsonify(returnstatus))
    print("3. preprocess, spam_filtering : True")
    ################
    status = wordcloud(
        tpt, wc_filename='./images/visualization/wordcloud/'+keyword+'.png')
    if not status:
        print('wordcloud 생성 중 에러...')
        returnstatus['status'] = False
        return (jsonify(returnstatus))
    print("4. wordcloud :", status)
    status = barplot(
        tpt, bp_filename='./images/visualization/barplot/'+keyword+'.png')
    if not status:
        print('barplot 생성 중 에러..')
        returnstatus['status'] = False
        return (jsonify(returnstatus))
    print("5. barplot :", status)
    ################
    status, lda_result, topic_num = sklda(
        spt, filedir='./images/visualization/lda_results/', keyword=keyword)
    returnstatus['topic_num'] = topic_num
    if not status:
        print('LDA 분석 중 에러..')
        returnstatus['status'] = False
        return (jsonify(returnstatus))
    print("6. lda :", status)
    ################
    status = network(
        spt, lda_result, saveDir='./templates/networks/', saveFilename=keyword, lineSplit=True)
    if not status:
        print('네트워크 생성 중 에러..')
        returnstatus['status'] = False
        return (jsonify(returnstatus))
    print("7. network :", status)
    ###############
    sent_result, status = sent_analysis(spt, saveDir='./images/visualization/sent_results/',
                                        fileName=keyword)
    returnstatus['sent_result'] = sent_result
    if not status:
        print('Error during sent_analysis...')
        returnstatus['status'] = False
        return (jsonify(returnstatus))
    print("8. sentiment analysis :", status)
    print("분석 완료, 총 소요시간 :", datetime.now()-bf)
    return jsonify(returnstatus)


@app.route('/network/<name>')
def network_ex(name):
    print('네트워크 불러오기...')
    filename = './templates/networks/'+name
    with open(filename, 'r') as fp:
        html = fp.read()
    return html

# 네트워크 불러올때 js 파일 제공


@app.route('/network/lib/<a>/<b>')
def js(a, b):
    filedir = './lib/'+a+'/'+b
    with open(filedir, 'r', encoding='utf-8-sig') as fp:
        file = fp.read()
    return file


@app.route('/images/<path1>/<path2>/<fileName>')
def sendimg(path1, path2, fileName):
    # images내부의 디렉토리를 포함한 filepath를 입력으로 받아 파일을 전송
    # directory=' 이미지의 파일 위치', filename='출력할 파일 이름'
    if path1 == 'top_imgs':
        return send_from_directory('images/top_imgs', fileName)
    else:
        try:
            return send_from_directory('images/'+path1+'/'+path2, fileName)
        except:
            return jsonify('file not found')
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


@app.route('/manage/delete_results')
def del_img():
    dir_path = './images/top_imgs'
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # 폴더 포함, 내부 파일 모두 삭제
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    dir_path = './images/visualization/barplot'
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # 폴더 포함, 내부 파일 모두 삭제
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    dir_path = './images/visualization/wordcloud'
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # 폴더 포함, 내부 파일 모두 삭제
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    dir_path = './images/visualization/lda_results'
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # 폴더 포함, 내부 파일 모두 삭제
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    dir_path = './images/visualization/sent_results'
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # 폴더 포함, 내부 파일 모두 삭제
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    dir_path = './templates/networks'
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # 폴더 포함, 내부 파일 모두 삭제
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return jsonify(1)


@app.route('/manage/keyword_search/enforce/<keyword>')
def enforce_search(keyword):
    g.thread = 'manage/keyword_search/enforce'
    # 대소문자 구분, 띄어쓰기 예외처리필요
    print('keyword_search 실행, enforce = True')
    status, tid = single_search(keyword, True)
    return jsonify({'status': status, 'tid': tid})


@app.route('/manage/t_search/<keyword>')
def search2(keyword):
    status, tid = t_search(keyword)
    return jsonify({'status': status, 'tid': tid})


# ---------------------------------------------------------------------
if __name__ == '__main__':
    # 배포시 디버그 옵션 없애야함, 크롤링 시 debug 옵션 False로 해두기..
    app.run(host='0.0.0.0', port=5000, debug=True)
