from requests import get, post, Session
from urllib import parse
import json
from datetime import datetime, timedelta
import emoji
import time
import pymysql
import random
import copy
from db import *

# total_acc_info, acc_info, sessions 생성코드 (전역 변수로 활용)
# total_acc_info를 DB로부터 받아와서 리턴하는 로직
def gen_total_acc():
    conn, cur = access_db()
    acc_info = []
    cur.execute('select * from accounts')
    all_blocked = True
    for row in cur.fetchall():
        tmp = dict()
        tmp['id'] = row['id']
        tmp['pw'] = row['pw']
        tmp['user_agent'] = row['user_agent']
        tmp['blocked'] = True if row['blocked'] == 1 else False
        tmp['up_date'] = row['up_date']
        if not tmp['blocked']:  # 하나라도 blocked라면
            all_blocked = False
        acc_info.append(tmp)
    close_db(conn)
    return acc_info, all_blocked

# 현재 가지고 있는(변화된) total_acc_info를 DB에 업데이트하는 로직
def to_db_total_acc():
    global total_acc_info, all_blocked

    conn, cur = access_db()
    all_blocked = True
    for row in total_acc_info:
        cur.execute('update accounts set blocked=(%s), up_date=(%s) where id=(%s);',
                    (1 if row['blocked'] == True else 0, str(time.strftime('%Y-%m-%d %H:%M:%S')), row['id']))
        if row['blocked'] == False:
            all_blocked = False
    close_db(conn)

### 매우 중요!!! 초기 할당 코드 (전역변수 할당 코드)
total_acc_info, all_blocked = gen_total_acc() #all_blocked : 계정이 전부 막혔는지, single_search()에서 활용!! -> 다 막혔으면 서비스가 안됨.
sessions = [
    {
    'session' : Session(),
    'inuse' : False,
     'last_time' : 0,
     'logout': 0,
     'usage' : 0,
     'orig_idx' : i#total_acc_info에서의 index
    } for i in range(len(total_acc_info))
]
acc_inuse = list() #사용중인 세션의 account index
####여기까지 초기 할당

### all_blocked인 경우에 30분~1시간 정도 주기적으로 로그인 시도(+로그아웃)해보면서 total_acc_info랑 all_blocked수정하기
# =>  주기적으로 다음 코드 실행
# 주기적으로 실행할 코드
def check_avail():
    global all_blocked
    for row in total_acc_info:
        h, session, status = login(row['id'], row['pw'])
        print(row['id'], row['pw'], status)
        if status == 0:  # 로그인 성공시
            row['blocked'] = False
            all_blocked = False
        time.sleep(random.randint(2, 10))
        logout(session)
        time.sleep(random.randint(7, 10))

    to_db_total_acc()

#헤더생성함수 => 1201기준, 서비스전에는 반드시 로직 변경해야함!!
def gen_header(): #header에 app_id랑 user-agent만 기본적으로 넣어주는 함수
    #user-agent id별로 바꾸는 로직 필요!! 나중에!!
    header = dict()
    header['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'
    header['x-ig-app-id'] = '936619743392459'
    return header

#로그인함수
def login(id, pw):
    # 새로운 헤더, 세션 생성 (새로운 세션 리턴)
    # 헤더, 세션, status를 리턴
    # status = 0 : success , 1 : checkpoint_needed 에러 (수동 인증 필요) 2 : incorrect pw 에러 (임시 차단) 3. CSRF 에러 (IP문제) 4. 그 외

    header, session = gen_header(), Session()

    resp = session.get('https://www.instagram.com/data/manifest.json', headers=header)
    header['x-csrftoken'] = session.cookies.get('csrftoken')
    #url = 'https://i.instagram.com/api/v1/web/accounts/login/ajax/'
    url = 'https://www.instagram.com/api/v1/web/accounts/login/ajax/'
    params = {'enc_password': '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(
        int(datetime.now().timestamp()), pw), 'username': id, 'optIntoOneTap': 'false'}

    resp = session.post(url, data=params, headers=header)  # 로그인 요청
    header['x-csrftoken'] = session.cookies.get('csrftoken')
    if resp.status_code == 400:
        print('Login Error : checkpoint_needed (수동 인증 필요) ...', id, pw)
        print(resp.text)
        return header, session, 1
    elif resp.status_code == 403:
        print('Login Error : CSRF error (IP 문제) ,,, ', id, pw)
        print(resp.text)
        return header, session, 3
    elif resp.status_code == 200:
        if not (resp.json()['authenticated']):
            print('Login Error : incorrect pw (계정 임시 차단 혹은 pw인증 에러)...', id, pw)
            print(resp.json())
            return header,session,2
        else:
            print('Login Successful : ', id, pw)
            return header, session, 0
    else:
        print('Login Error : unknown,,, response status code:', resp.status_code, id, pw)
        print(resp.text)
        return header, session, 4

#로그아웃 함수
def logout(session):
    # session을 input으로, output으로 status만..
    # status True : success, False : failure
    url = 'https://www.instagram.com/api/v1/web/accounts/logout/ajax/'
    header = gen_header()
    header['x-csrftoken'] = session.cookies.get('csrftoken')  # 재설정
    params = {'one_tap_app_login': 0, 'user_id': session.cookies.get('ds_user_id')}
    resp = session.post(url, data=params, headers=header)

    try:
        if resp.json()['status'] == 'ok':
            print('successfully logged out...')
            return True
        else:
            print('!! logout error...')
    except:
        print('logout error...')
    # print(resp.status_code, resp.content)

    return False

#최근 게시물 수집 함수
def hot_key_instagram_recent(query, session, max_page=40):
    # input : query, session
    # return (status, recent_list, timestamp, image_list)
    # status = 0 : success, 1 : 크롤링 중 문제 발생 (CSRF error), code는 200 , 2 : 400error - 계정에 checkpoint 필요
    # 3 : 검열 혹은 페이지 x,  4 : 그 외, 5 : 인스타그램에서 최근 게시물을 제공하지 않는 태그 ( len(recent_list[0]) == 0 )
    postcnt = 0  # 포스트 수 카운팅, 300개 되면 stop.
    timestamp = 0

    before = datetime.now()
    recent_list = list()
    image_list = list()

    headers = gen_header()
    url = 'https://i.instagram.com/api/v1/tags/web_info/?tag_name={}'.format(parse.quote(query))
    headers['x-csrftoken'] = session.cookies.get('csrftoken')  # 재설정
    headers['referer'] = 'https://www.instagram.com/explore/tags/{}/'.format(parse.quote(query))
    resp = session.get(url, headers=headers)

    if (resp.status_code == 404):
        print('Crawling error : 검열되는 해시태그이거나 해당 태그를 담은 페이지가 존재하지 않습니다.')
        print('response code : ', 404)
        return (3, recent_list, timestamp, image_list)

    elif (resp.status_code != 200):  # 응답 에러
        if (resp.status_code == 400):
            print('Crawling error : checkpoint needed 의심')
            print(resp.text)
            return (2, recent_list, timestamp, image_list)
        print('Crawling error : unknown..., resp.code :', resp.status_code)
        print(resp.text)
        return (4, recent_list, timestamp, image_list)  # 계정바꿔서 재시도

    # 첫페이지 응답 정상인경우

    ################################################# 비정상입력 예외처리
    try:
        resource = resp.json()
    except:
        print("Crawling error : 응답 코드는 정상이나, 비정상적인 데이터 형식 반환됨")  # 크롤링 밴 의심..
        return (1, recent_list, timestamp, image_list)
    #################################################

    # recent 돌기

    # print('\n최근 게시물: 1페이지....')
    recent_list.append([])
    image_list.append([])
    for i in resource['data']['recent']['sections']:  # 0~8
        for k in i['layout_content']['medias']:
            if (k['media']['caption'] != None):
                if 'text' in k['media']['caption'].keys():
                    recent_list[0].append(
                        emoji.demojize(k['media']['caption']['text']))  # 이모티콘 제거 ###########################
                    timestamp = max(timestamp, k['media']['caption'][
                        'created_at_utc'])  # 최신 포스트의 현재 시간 1669098438 ##############################
                    ###--------------------------1123 추가
                    #######################################################################
                    try:
                        image_list[0].append(k['media']['image_versions2']['candidates'][0]['url'])  # 포스트의 이미지 URL 
                    except:
                        image_list[0].append(k['media']['carousel_media'][0]['image_versions2']['candidates'][0]['url'])
                        # 복수의 이미지가 있는 포스트의 첫이미지 URL 
                    #########################################################
                    postcnt += 1
    print('누적 게시물 수 :', postcnt)
    time.sleep(random.uniform(1, 5))

    # recent기준 다음 페이지 관련 정보
    recent_info = {'max_id': '', 'page': '', 'isnext': False}
    if resource['data']['recent']['more_available']:
        recent_info['max_id'], recent_info['page'], recent_info['isnext'] = \
            resource['data']['recent']['next_max_id'], resource['data']['recent']['next_page'], True

    # 그 다음 페이지부터 recent 돌기
    url = 'https://i.instagram.com/api/v1/tags/{}/sections/'.format(parse.quote(query))
    data = {'max_id': recent_info['max_id'], 'page': recent_info['page'], 'surface': 'grid', 'tab': 'recent'}

    while (recent_info['isnext'] == True and data['page'] < max_page):
        # print('\n최근 게시물: {}페이지....'.format(data['page']+1))
        headers['x-csrftoken'] = session.cookies['csrftoken']  # 매번 재설정해주기
        resp = session.post(url, data=data, headers=headers)
        ########################################################################### 스크롤 시작 이후 로그인 소요 발생 시 예외 처리
        if (resp.status_code != 200):  # 응답 에러
            if (resp.status_code == 400):
                print('Crawling error : checkpoint needed 의심')
                print(resp.text)
                return (2, recent_list, timestamp, image_list)
            print('Crawling error : unknown..., resp.code :', resp.status_code)
            print(resp.text)
            return (4, recent_list, timestamp, image_list)  # 계정바꿔서 재시도
        ##########################################################################
        ################################################# 비정상입력 예외처리
        try:
            resource = resp.json()
        except:
            print("Crawling error : 응답 코드는 정상이나, 비정상적인 데이터 형식 반환됨")  # 크롤링 밴 의심..
            # print(resp.content)
            return (1, recent_list, timestamp, image_list)
        #################################################
        recent_list.append([])
        image_list.append([])
        for i in resource['sections']:  # 0~8
            for k in i['layout_content']['medias']:  # 0~2
                if (k['media']['caption'] != None):
                    if 'text' in k['media']['caption'].keys():
                        recent_list[data['page']].append(
                            emoji.demojize(k['media']['caption']['text']))  # 이모티콘 제거 ###############
                        ###--------------------------1123 추가
                        #######################################################################
                        try:
                            image_list[data['page']].append(
                                k['media']['image_versions2']['candidates'][0]['url'])  # 포스트의 이미지 URL 
                        except:
                            image_list[data['page']].append(
                                k['media']['carousel_media'][0]['image_versions2']['candidates'][0]['url'])
                            # 복수의 이미지가 있는 포스트의 첫이미지 URL 
                        #########################################################
                        postcnt += 1
                        if (postcnt >= 300):
                            print('누적 게시물 수 :', postcnt)
                            print('최근 게시물 수집 완료!')
                            print('총 소요시간 : ', datetime.now() - before, '\n\n')
                            return (0, recent_list, timestamp, image_list)

        if resource['more_available']:
            data['max_id'] = resource['next_max_id']
            data['page'] = resource['next_page']

        else:
            recent_info['isnext'] = False
        print('누적 게시물 수 :', postcnt)
        time.sleep(random.uniform(1, 5))

    if (len(recent_list[0]) == 0):
        print('인스타그램에서 최근 게시물을 제공하지 않는 태그입니다..')
        return (5, recent_list, timestamp, image_list)

    print('누적 게시물 수 :', postcnt)
    print('최근 게시물 수집 완료!')
    print('총 소요시간 : ', datetime.now() - before, '\n')
    return (0, recent_list, timestamp, image_list)

def check_session():  # 1130 코드
    # 가용가능한 세션을 검사하고 교체해서 해당 세션의 original index를 전달해줌.

    global total_acc_info, sessions, all_blocked, acc_inuse

    if len(acc_inuse) > 0:  # 이미 사용중인 세션이 있다면
        # 만료 조건 검사 후 교체(할수도 안할수도)

        for s in acc_inuse:  # 사용중인 세션에 대해
            # 해당 세션 찾기
            for idx, i in enumerate(sessions):
                if s['orig_idx'] == i['orig_idx']:
                    if i['inuse'] == True and (i['usage'] > 3 or int(datetime.now().timestamp()) - i[
                        'last_time'] > 3600):  # 3600
                        # 세션 종료(교체) 조건 충족하면 로그아웃 및 세션 종료
                        logout(i['session'])
                        i['inuse'] = False
                        i['logout'] = int(datetime.now().timestamp())
                        i['usage'] = 0
                        # acc_inuse에서 삭제
                        for i, a in enumerate(acc_inuse):
                            if a['orig_idx'] == s['orig_idx']:
                                acc_inuse.pop(i)
                                break

        if len(acc_inuse) < 2:
            # 다른 세션 로그인
            sessions.sort(key=lambda x: x['logout'])  # 로그아웃한지 오래된 순으로 정렬

            for s in sessions:
                if total_acc_info[s['orig_idx']]['blocked'] == False and s['inuse'] == False:  # 막히지 않고, 사용중이지 않은것
                    header, session, status = login(total_acc_info[s['orig_idx']]['id'],
                                                    total_acc_info[s['orig_idx']]['pw'])
                    if status != 0:  # 로그인 실패시
                        # total_acc_info에서 block으로 처리
                        total_acc_info[s['orig_idx']]['blocked'] = True
                    else:
                        # 새로운 세션 추가.
                        acc_inuse.append({'session': session, 'orig_idx': s['orig_idx']})
                        s['session'] = session
                        s['inuse'] = True
                        s['last_time'] = int(datetime.now().timestamp())
                        s['usage'] = 0
                if len(acc_inuse) >= 2:
                    break  # 최대 두개까지만 추가

    else:  # 이미 사용중인 세션이 없는경우, 가장 사용한지 오래된 세션부터 로그인
        # 사용한지 오래된 순으로 sort
        sessions.sort(key=lambda x: x['last_time'])
        for s in sessions:
            if not (total_acc_info[s['orig_idx']]['blocked']):  # 막히지 않은 계정 중에서
                # 로그인 시도
                header, session, status = login(total_acc_info[s['orig_idx']]['id'],
                                                total_acc_info[s['orig_idx']]['pw'])
                if status != 0:  # 로그인 실패시
                    # total_acc_info에서 block으로 처리
                    total_acc_info[s['orig_idx']]['blocked'] = True
                else:  # 로그인 성공시
                    s['session'] = session  # 세션 할당
                    s['inuse'] = True
                    s['last_time'] = int(datetime.now().timestamp())
                    s['logout'] = 0
                    s['usage'] = 0
                    acc_inuse.append({'session': session, 'orig_idx': s['orig_idx']})
            if len(acc_inuse) >= 2:  # 최대 두개까지 추가
                break

    # 세션 교체 끝. 계정 다 막혔는지 체크
    to_db_total_acc()  # 전체 계정정보 업데이트
    return

#메인) Single_Search Algorithm
def single_search(keyword):  # 성공여부, corpus랑 image를 반환
    # return T/F, corpus, image
    #############################DB존재여부 확인##########################################
    # db연결
    conn, cur = access_db()
    cur.execute('SELECT tid, ttable FROM is_tag NATURAL JOIN tag_info WHERE tname = (%s);', (keyword))
    res = cur.fetchall()

    # DB에 존재할 경우
    if len(res) >= 1:
        print('DB에서 해당 키워드를 찾았습니다.. keyword :', keyword)
        tid, ttable = res[0]['tid'], res[0]['ttable']
        corpus, image = '', ''
        if ttable == 1:  # s_corpus
            cur.execute('select corpus from s_corpus where tid = (%s)', (tid))
            corpus = cur.fetchall()[0]['corpus']
        elif ttable == 2:  # t_corpus
            cur.execute('select corpus from t_corpus where tid = (%s)', (tid))
            corpus = cur.fetchall()[0]['corpus']
        elif ttable == 3:  # n_corpus
            cur.execute('select corpus from n_corpus where tid = (%s)', (tid))
            corpus = cur.fetchall()[0]['corpus']
        else:
            # 예외
            print('db 접근 중 발생한 에러입니다. 재시도요망')
            conn.close()
            return (False, '', '')
        cur.execute('select image from images where tid = (%s)', (tid))
        image = cur.fetchall()[0]['image']
        conn.close()
        return (True, corpus, image)

    ########################DB에 존재하지 않을경우, 크롤링->DB적재->값 반환#####################

    global total_acc_info, sessions, acc_inuse, all_blocked
    delimiter = 'HOTKEY123!@#'

    check_session()  # 가용가능한 세션이있는지 확인
    if all_blocked:  # 전부 막혔으면
        print('가용가능한 세션이 없습니다')
        return (False, '', '')

    # acc_inuse[0]['session'], acc_inuse[1]['session']이 가용가능한 세션임
    # 세션 두개로 다 시도해봤는데 에러가 뜨면, ㅈㅈ
    # 중간에 오류나는 경우 세션 만료시키고 account block 처리할것.
    for s in copy.deepcopy(acc_inuse):  # 가용가능한 세션을 돌면서
        recent_list, image_list = [], []
        print('Currently trying with ...', total_acc_info[s['orig_idx']]['id'], total_acc_info[s['orig_idx']]['pw'])
        # hot_key_instagram_recent(query, session, max_page=40)
        # return (0, recent_list, timestamp, image_list)
        # status = 0 : success, 1 : 크롤링 중 문제 발생 (CSRF error), code는 200 , 2 : 400error - 계정에 checkpoint 필요
        # 3 : 검열 혹은 페이지 x,  4 : 그 외, 5 : 인스타그램에서 최근 게시물을 제공하지 않는 태그 ( len(recent_list[0]) == 0 )
        s['session']  # 이미 로그인 되어있음.
        print('Start Crawling... keyword :', keyword)
        status, recent_list, timestamp, image_list = hot_key_instagram_recent(keyword, s['session'])
        # status 상태 따라서 분기. 0이나 3이나 5면 계정문제 x, 1이나 2면 계정문제 o, 4는 그 외.
        if status == 0:
            # 정상적으로 크롤링에 성공한 경우
            # db에 적재하고 corpus랑 image넘겨주기
            corpus = ''
            for page in recent_list:
                for post in page:
                    corpus = corpus + delimiter + post
            cur.execute('insert into is_tag (tname) values (%s);', keyword)
            cur.execute('SELECT tid FROM is_tag ORDER BY tid DESC LIMIT 1;')
            tid = cur.fetchone()['tid']
            # n_corpus에 저장
            cur.execute('insert into tag_info (tid, ttable, up_date, time_stamp) values (%s, %s, %s, %s);',
                        (tid, 3, time.strftime('%Y-%m-%d'), timestamp))
            cur.execute('insert into n_corpus (tid, corpus) values (%s, %s);', (tid, corpus[12:]))
            # image추가하는 로직
            image = ''
            for page in image_list:
                for post in page:
                    image = image + delimiter + post
            cur.execute('insert into images (tid, image) values (%s, %s);', (tid, image[12:]))
            close_db(conn)
            ##session에서 last_time이랑 usage 정보 변경
            for i in sessions:
                if i['orig_idx'] == s['orig_idx']:
                    i['last_time'] = int(datetime.now().timestamp())
                    i['usage'] += 1
                    break

            ############(corpus, image들 전달)#############
            return (True, corpus[12:], image[12:])

        elif 1 <= status <= 2:
            # CSRF Error(IP혹은 계정 block 혹은 크롤링 block) or 계정 임시block(checkpoint필요)

            # account block됨. => block로직 (total_acc_info에서 block으로 바꾸기, sessions바꾸기, acc_info바꾸기)
            total_acc_info[s['orig_idx']]['blocked'] = True
            to_db_total_acc()  # 디비에 차단 정보 업데이트

            # session로그아웃, 세션 정보 변경
            # logout(s['session']) 자동으로 세션이 만료되므로 로그아웃할필요가 없어보임 (status가 1인 경우...)
            for i in sessions:
                if i['orig_idx'] == s['orig_idx']:
                    i['inuse'] = False
                    i['logout'] = int(datetime.now().timestamp())
                    i['usage'] = 0
                    break

            # acc_inuse에서 삭제
            for i, a in enumerate(acc_inuse):
                if a['orig_idx'] == s['orig_idx']:
                    acc_inuse.pop(i)
                    break

        elif status == 3:
            # 검열 키워드 혹은 페이지 x (404error)
            print('to client : 해당 태그는 인스타그램에서 검색이 제한되어있거나, 결과를 제공하지 않습니다. 다른 키워드를 입력하세요...')
            ##session에서 last_time이랑 usage 정보 변경
            for i in sessions:
                if i['orig_idx'] == s['orig_idx']:
                    i['last_time'] = int(datetime.now().timestamp())
                    i['usage'] += 1
                    break
            close_db(conn)
            return (False, '', '')

        elif status == 5:
            # 인스타그램에서 최근 게시물을 제공하지 않는 태그 ( len(recent_list[0]) == 0 )
            print('to client : 인스타그램에서 최근 게시물을 제공하지 않습니다. 다른 키워드를 입력하세요..')
            ##session에서 last_time이랑 usage 정보 변경
            for i in sessions:
                if i['orig_idx'] == s['orig_idx']:
                    i['last_time'] = int(datetime.now().timestamp())
                    i['usage'] += 1
                    break
            close_db(conn)
            return (False, '', '')

        else:  # status가 4인경우
            # 그 외 알수없는 에러
            print('원인을 알 수 없는 에러 입니다..')

        # 세션 교체 (while문으로 들어가서)
        time.sleep(random.uniform(5, 10))

    # 여기까지 왔으면, 가용가능한 세션을 다 썼지만 결과 도출이 되지않았음.
    print('to client : 현재 서비스가 원활하지 않습니다. 나중에 다시 시도하세요..')
    close_db(conn)
    return (False, '', '')