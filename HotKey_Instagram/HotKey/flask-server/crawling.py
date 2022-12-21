from flask import g
from requests import get, post, Session
from urllib import parse
import json
from datetime import datetime
import emoji
import time
import random
import copy
from db import *

# 계정 정보를 DB로부터 받아와서 리턴


def get_accounts(cur):
    print('get_accounts 실행')
    acc_info = []
    try:
        cur.execute('select * from accounts')
        print(g.thread, ": getDB - account info fetched")
        all_blocked = True
        for row in cur.fetchall():
            tmp = dict()
            tmp['aid'] = row['aid']
            tmp['id'] = row['id']
            tmp['pw'] = row['pw']
            tmp['user_agent'] = row['user_agent']
            tmp['blocked'] = True if row['blocked'] == 1 else False
            tmp['up_date'] = row['up_date']  # datetime
            tmp['last_used'] = row['last_used']  # timestamp
            # 현재 타 세션에서 사용중인지 여부
            tmp['in_use'] = True if row['in_use'] == 1 else False
            if not tmp['blocked']:  # 하나라도 차단되지 않았다면
                all_blocked = False
            acc_info.append(tmp)
    except:
        return ([], -1)
    return acc_info, all_blocked

# modified account info를 DB에 업데이트


def set_accounts(cur):
    try:
        g.all_blocked = True
        for row in g.total_acc_info:
            cur.execute('update accounts set blocked=(%s), up_date=(%s), last_used=(%s), in_use=(%s) where id=(%s);',
                        (1 if row['blocked'] == True else 0, str(time.strftime('%Y-%m-%d %H:%M:%S')), row['last_used'], 1 if row['in_use'] == True else 0, row['id']))
            if row['blocked'] == False:
                g.all_blocked = False
    except:
        return False
    return True

# 차단된 모든 계정에 대해 차단 여부를 재 확인 후 업데이트


def check_avail():
    print('check_avail 실행')
    for row in g.total_acc_info:
        if row['blocked'] == True:
            h, session, status = login(row['id'], row['pw'])
            if status == 0:  # 로그인 성공시
                row['blocked'] = False
                g.all_blocked = False
                print(row['id'], row['pw'], '차단 해제 확인')
                time.sleep(random.randint(2, 10))
                logout(session)
            time.sleep(random.randint(1, 10))

# 요청에 사용할 헤더생성함수


def gen_header():  # header에 app_id랑 user-agent 추가
    header = dict()
    header['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'
    header['x-ig-app-id'] = '936619743392459'
    return header

# 로그인함수


def login(id, pw):
    # 헤더, 세션, status를 리턴
    # status = 0 : success , 1 : checkpoint_needed 에러 (수동 인증 필요) 2 : incorrect pw 에러 (임시 차단) 3. CSRF 에러 (IP문제) 4. 그 외
    header, session = gen_header(), Session()

    resp = session.get(
        'https://www.instagram.com/data/manifest.json', headers=header)
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
            return header, session, 2
        else:
            print('Login Successful : ', id, pw)
            return header, session, 0
    else:
        print('Login Error : unknown,,, response status code:',
              resp.status_code, id, pw)
        print(resp.text)
        return header, session, 4

# 로그아웃 함수


def logout(session):
    # status True : success, False : failure
    url = 'https://www.instagram.com/api/v1/web/accounts/logout/ajax/'
    header = gen_header()
    header['x-csrftoken'] = session.cookies.get('csrftoken')  # 재설정
    params = {'one_tap_app_login': 0,
              'user_id': session.cookies.get('ds_user_id')}
    resp = session.post(url, data=params, headers=header)

    try:
        if resp.json()['status'] == 'ok':
            print('successfully logged out...')
            return True
        else:
            print('!! logout error...')
    except:
        print('logout error...')

    return False

# 최근 게시물 수집 함수


def hot_key_instagram_recent(query, session, max_page=40):
    # input : query, session
    # return (status, recent_list, timestamp, image_list)
    # status = 0 : success, 1 : 크롤링 중 문제 발생 (CSRF error), code는 200 , 2 : 400error - 계정에 checkpoint 필요
    # 3 : 검열 혹은 페이지 x,  4 : 그 외, 5 : 인스타그램에서 최근 게시물을 제공하지 않는 태그 ( len(recent_list[0]) == 0 )
    postcnt = 0  # 포스트 수 카운팅
    timestamp = 0

    before = datetime.now()
    recent_list = list()

    headers = gen_header()
    url = 'https://i.instagram.com/api/v1/tags/web_info/?tag_name={}'.format(
        parse.quote(query))
    headers['x-csrftoken'] = session.cookies.get('csrftoken')  # 재설정
    headers['referer'] = 'https://www.instagram.com/explore/tags/{}/'.format(
        parse.quote(query))
    resp = session.get(url, headers=headers)

    if (resp.status_code == 404):
        print('Crawling error : 검열되는 해시태그이거나 해당 태그를 담은 페이지가 존재하지 않습니다.')
        print('response code : ', 404)
        return (3, recent_list, timestamp)

    elif (resp.status_code != 200):  # 응답 에러
        if (resp.status_code == 400):
            print('Crawling error : checkpoint needed 의심')
            print(resp.text)
            return (2, recent_list, timestamp)
        print('Crawling error : unknown..., resp.code :', resp.status_code)
        print(resp.text)
        return (4, recent_list, timestamp)  # 계정바꿔서 재시도

    # 첫페이지 응답 정상인경우

    # 비정상입력 예외처리
    try:
        resource = resp.json()
    except:
        print("Crawling error : 응답 코드는 정상이나, 비정상적인 데이터 형식 반환됨")  # 크롤링 밴 의심..
        return (1, recent_list, timestamp)
    #################################################

    recent_list.append([])
    for i in resource['data']['recent']['sections']:  # 0~8
        for k in i['layout_content']['medias']:
            if (k['media']['caption'] != None):
                if 'text' in k['media']['caption'].keys():
                    recent_list[0].append(
                        emoji.demojize(k['media']['caption']['text']))  # 이모티콘 제거
                    timestamp = max(timestamp, k['media']['caption'][
                        'created_at_utc'])  # 최신 포스트의 현재 시간
                    postcnt += 1
    print(g.thread, ': 누적 게시물 수 :', postcnt)
    time.sleep(random.uniform(1, 5))

    # 다음 페이지 관련 정보
    recent_info = {'max_id': '', 'page': '', 'isnext': False}
    if resource['data']['recent']['more_available']:
        recent_info['max_id'], recent_info['page'], recent_info['isnext'] = \
            resource['data']['recent']['next_max_id'], resource['data']['recent']['next_page'], True

    # 그 다음 페이지부터 반복 크롤링
    url = 'https://i.instagram.com/api/v1/tags/{}/sections/'.format(
        parse.quote(query))
    data = {'max_id': recent_info['max_id'],
            'page': recent_info['page'], 'surface': 'grid', 'tab': 'recent'}

    while (recent_info['isnext'] == True and data['page'] < max_page):
        headers['x-csrftoken'] = session.cookies['csrftoken']  # csrf token 재설정
        resp = session.post(url, data=data, headers=headers)
        # 스크롤 시작 이후 로그인 소요 발생 시 예외 처리
        if (resp.status_code != 200):  # 응답 에러
            if (resp.status_code == 400):
                print('Crawling error : checkpoint needed 의심')
                print(resp.text)
                return (2, recent_list, timestamp)
            print('Crawling error : unknown..., resp.code :', resp.status_code)
            print(resp.text)
            return (4, recent_list, timestamp)  # 계정바꿔서 재시도
        # 비정상입력 예외처리
        try:
            resource = resp.json()
        except:
            # 크롤링 밴 의심..
            print("Crawling error : 응답 코드는 정상이나, 비정상적인 데이터 형식 반환됨")
            # print(resp.content)
            return (1, recent_list, timestamp)
        recent_list.append([])
        for i in resource['sections']:  # 0~8
            for k in i['layout_content']['medias']:  # 0~2
                if (k['media']['caption'] != None):
                    if 'text' in k['media']['caption'].keys():
                        recent_list[data['page']].append(
                            emoji.demojize(k['media']['caption']['text']))  # 이모티콘 제거
                        postcnt += 1
                        if (postcnt >= 300):
                            print(g.thread, ': 누적 게시물 수 :', postcnt)
                            print(g.thread, ': 최근 게시물 수집 완료!')
                            return (0, recent_list, timestamp)

        if resource['more_available']:
            data['max_id'] = resource['next_max_id']
            data['page'] = resource['next_page']

        else:
            recent_info['isnext'] = False
        print(g.thread, ': 누적 게시물 수 :', postcnt)
        time.sleep(random.uniform(1, 5))

    if (len(recent_list[0]) == 0):
        print('인스타그램에서 최근 게시물을 제공하지 않는 태그입니다..')
        return (5, recent_list, timestamp)

    print(g.thread, ': 누적 게시물 수 :', postcnt)
    print(g.thread, ': 최근 게시물 수집 완료!')
    return (0, recent_list, timestamp)


def check_session():
    # 가장 사용한지 오래된 계정부터 로그인 시도, 최대 2개의 세션 생성, True or False 반환
    conn, cur = access_db()
    print('DB 트랜잭션 시작, 계정정보 받아오기')
    cur.execute('set autocommit=0;')
    cur.execute('set session transaction isolation level serializable;')
    cur.execute('start transaction;')  # 트랜잭션 시작
    # Explicit lock, 여러 쓰레드가 동시에 같은 세션을 사용하는 것을 방지
    print(g.thread, ": 트랜잭션 선언완료")
    cur.execute('UPDATE accounts SET aid=3 WHERE aid=3;')
    print(g.thread, ": check_session, 업데이트문 실행완료")

    # g.total_acc_info설정
    g.total_acc_info, g.all_blocked = get_accounts(cur)
    # 트랜잭션 에러시..
    if (g.all_blocked == -1):
        print("(check_session_getDB) : DB 트랜잭션 에러...")
        conn.close()
        return False
    g.acc_inuse = list()
    # 사용한지 오래된 순으로 sort
    g.total_acc_info.sort(key=lambda x: x['last_used'])
    g.mapping = dict()
    for idx, acc in enumerate(g.total_acc_info):
        g.mapping[acc['aid']] = idx
        if not (acc['blocked']) and not (acc['in_use']):  # 막히지 않고 사용중이지 않은 계정 중에서
            h, session, status = login(acc['id'], acc['pw'])
            if status != 0:  # 로그인 실패시
                acc['blocked'] = True
            else:  # 로그인 성공시 세션할당
                g.acc_inuse.append({'session': session, 'aid': acc['aid']})
                acc['last_used'] = int(datetime.now().timestamp())
                acc['in_use'] = True
        if len(g.acc_inuse) >= 2:  # 최대 두개까지 추가
            break
    # 세션 생성 끝
    # 전체 계정정보 업데이트 + 사용중여부 업데이트하기 + (all_blocked 업데이트)
    status = set_accounts(cur)
    if not status:
        stat = set_accounts(cur)
        if not stat:
            print("(check_session_setDB) : DB 트랜잭션 에러...")
            conn.close()
            return False
    close_db(conn)  # 트랜잭션 끝 (commit, close)
    return True

# 성공여부와 tid를 반환. ex) (True, tid) 혹은 (False, -1)


def single_search(keyword, enforce=False):
    # DB에서만 리턴되는 경우 server.py에서의 에러 방지
    g.acc_inuse, g.total_acc_info = [], []

    # enforce => DB에 있어도 강제 크롤링 (최신화)
    if len(keyword) == 0:
        print("to client: 한 글자 이상의 키워드를 입력하세요..")
        return (False, -1)
    ############################# DB존재여부 확인##########################################
    # db연결
    conn, cur = access_db()
    cur.execute(
        'SELECT tid FROM is_tag WHERE tname = (%s);', (keyword))
    res = cur.fetchall()
    # DB에 존재할 경우
    if len(res) >= 1 and not enforce:
        print('DB에서 해당 키워드를 찾았습니다.. keyword :', keyword)
        tid = res[0]['tid']
        conn.close()
        return (True, tid)
    conn.close()  # 일단 conn.close()
    ######################## DB에 존재하지 않을경우, 크롤링->DB적재->값 반환 #####################
    delimiter = 'HOTKEY123!@#'

    status = check_session()  # 가용가능한 세션이있는지 확인, g.acc_inuse에 가용가능한 세션 정보 할당
    if not status:
        print("single_search_check_session : DB 트랜잭션 에러...")
        return (False, -1)

    if g.all_blocked:  # 전부 막혔으면
        print('All accounts are blocked by instagram.. please try "check_avail" manually later..')
        return (False, -1)

    if len(g.acc_inuse) == 0:
        print('No sessions available..')
        return (False, -1)

    print('세션 생성 완료')
    tmp = list()
    for i in g.acc_inuse:
        tmp.append(i['aid'])
    print('가용중인 세션 (aid) :', tmp)

    # g.mapping['aid'] = 현재 total_acc_info에서의 index번호
    map = g.mapping
    for s in copy.deepcopy(g.acc_inuse):  # 가용가능한 세션을 돌면서
        print('Currently trying with ...',
              g.total_acc_info[map[s['aid']]]['id'], g.total_acc_info[map[s['aid']]]['pw'])
        print('Start Crawling... keyword :', keyword)
        status, recent_list, timestamp = hot_key_instagram_recent(
            keyword, s['session'])
        # total_acc_info에서 last_used정보 변경
        g.total_acc_info[map[s['aid']]]['last_used'] = int(
            datetime.now().timestamp())

        # status 상태 따라서 분기
        if status == 0:
            # 정상적으로 크롤링에 성공한 경우
            # db에 적재하고 tid반환
            corpus = ''
            for page in recent_list:
                for post in page:
                    corpus = corpus + delimiter + post

            conn, cur = access_db()
            if len(res) >= 1 and enforce:  # Db에 있는데도 enforce인경우
                cur.execute(
                    'SELECT tid FROM is_tag WHERE tname = (%s)', (keyword))
                tid = cur.fetchone()['tid']
                cur.execute(
                    'select ttable FROM tag_info WHERE tid= (%s)', (tid))
                ttable = cur.fetchone()['ttable']
                # tag_info 업데이트
                cur.execute('update tag_info set up_date=(%s), time_stamp=(%s) where tid=(%s)',
                            (time.strftime('%Y-%m-%d'), timestamp, tid))
                # 1 = s_corpus, 2 = t_corpus, 3 = n_corpus
                # corpus 업데이트
                if ttable == 1:  # s_corpus
                    cur.execute(
                        'update s_corpus set corpus=(%s) where tid=(%s)', (corpus[12:], tid))
                    pass
                elif ttable == 2:  # t_corpus
                    cur.execute(
                        'update t_corpus set corpus=(%s) where tid=(%s)', (corpus[12:], tid))
                    pass
                else:  # n_corpus
                    cur.execute(
                        'update n_corpus set corpus=(%s) where tid=(%s)', (corpus[12:], tid))
                    pass
                close_db(conn)
                return (True, tid)

            else:  # DB에 없으면 enforce여부에 관계없이
                cur.execute('insert into is_tag (tname) values (%s);', keyword)
                cur.execute(
                    'SELECT tid FROM is_tag WHERE tname = (%s);', keyword)
                tid = cur.fetchone()['tid']
                # tag_info에 저장
                cur.execute('insert into tag_info (tid, ttable, up_date, time_stamp) values (%s, %s, %s, %s);',
                            (tid, 3, time.strftime('%Y-%m-%d'), timestamp))
                # n_corpus에 저장
                cur.execute(
                    'insert into n_corpus (tid, corpus) values (%s, %s);', (tid, corpus[12:]))
                close_db(conn)
                return (True, tid)

        elif 1 <= status <= 2:
            # CSRF Error(IP혹은 계정 block 혹은 크롤링 block) or 계정 임시block(checkpoint필요)
            # account block됨. => block로직 (total_acc_info에서 block으로 바꾸기)
            g.total_acc_info[map[s['aid']]]['blocked'] = True
            g.total_acc_info[map[s['aid']]]['in_use'] = False
            # 디비에 차단 정보 바로 업데이트
            conn, cur = access_db()
            cur.execute('update accounts set blocked=(%s), up_date=(%s), last_used=(%s), in_use=(%s) where id=(%s);',
                        (1, str(time.strftime('%Y-%m-%d %H:%M:%S')), g.total_acc_info[map[s['aid']]]['last_used'], 0, g.total_acc_info[map[s['aid']]]['id']))
            close_db(conn)
            # acc_inuse에서 삭제
            for i, a in enumerate(g.acc_inuse):
                if a['aid'] == s['aid']:
                    g.acc_inuse.pop(i)
                    break

        elif status == 3:
            # 검열 키워드 혹은 페이지 x (404error)
            print(
                'to client : 해당 태그는 인스타그램에서 검색이 제한되어있거나, 결과를 제공하지 않습니다. 다른 키워드를 입력하세요...')
            return (False, -1)

        elif status == 5:
            # 인스타그램에서 최근 게시물을 제공하지 않는 태그 ( len(recent_list[0]) == 0 )
            print('to client : 인스타그램에서 최근 게시물을 제공하지 않습니다. 다른 키워드를 입력하세요..')
            return (False, -1)

        else:  # status가 4인경우
            # 그 외 알수없는 에러
            print('원인을 알 수 없는 에러 입니다..')

        # 세션 교체 (while문 복귀)
        time.sleep(random.uniform(5, 10))

    # 가용가능한 세션을 다 썼지만 결과 도출이 되지 않은 경우
    print('to client : 현재 서비스가 원활하지 않습니다. 나중에 다시 시도하세요..')
    return (False, -1)


# 구글 트렌드에서 실시간 검색어 가져오기
def trend_crawler_client():  # 7개 리턴.
    tmplist = list()
    session = Session()
    url = 'https://trends.google.co.kr/trends/api/dailytrends?hl=ko&tz=-540&geo=KR&ns=15'
    resp = session.get(url)

    for page in json.loads(resp.text[6:])['default']['trendingSearchesDays']:
        for i in page['trendingSearches']:
            tmplist.append(i['title']['query'])
    # 중복제거해서 7개 리턴
    tmp = list()
    for i in tmplist:
        if i not in tmp:
            tmp.append(i)
    trendlist = list()
    for i in tmplist:
        print(i.split())
        if len(i.split()) == 1:
            trendlist.append(i)
    idx = len(trendlist) - 1
    while len(trendlist) <= 5:
        if len(trendlist[idx]) > 7:
            trendlist.pop(idx)
    return trendlist[:5]


def get_guest_token(session):
    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
    }
    resp = session.post(
        'https://api.twitter.com/1.1/guest/activate.json', headers=headers)
    return session, resp.json()['guest_token']


def set_params(keyword, session):  # header와 parameter값을 설정해준다.
    params = {'include_profile_interstitial_type': '1',
              'include_blocking': '1',
              'include_blocked_by': '1',
              'include_followed_by': '1',
              'include_want_retweets': '1',
              'include_mute_edge': '1',
              'include_can_dm': '1',
              'include_can_media_tag': '1',
              'include_ext_has_nft_avatar': '1',
              'skip_status': '1',
              'cards_platform': 'Web-12',
              'include_cards': '1',
              'include_ext_alt_text': 'true',
              'include_ext_limited_action_results': 'false',
              'include_quote_count': 'true',
              'include_reply_count': '1',
              'tweet_mode': 'extended',
              'include_ext_collab_control': 'true',
              'include_entities': 'true',
              'include_user_entities': 'true',
              'include_ext_media_color': 'true',
              'include_ext_media_availability': 'true',
              'include_ext_sensitive_media_warning': 'true',
              'include_ext_trusted_friends_metadata': 'true',
              'send_error_codes': 'true',
              'simple_quoted_tweet': 'true',
              'q': '',
              'tweet_search_mode': 'live',
              'count': '20',
              'query_source': 'recent_search_click',
              'pc': '1',
              'spelling_corrections': '1',
              'include_ext_edit_control': 'true',
              'ext': 'mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl%2Ccollab_control%2Cvibe'}

    headers = {'authority': 'twitter.com',
               'method': 'GET',
               # 'path': '/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=false&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_collab_control=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=%23%EB%83%89%EB%8F%99%EB%A7%8C%EB%91%90&tweet_search_mode=live&count=20&query_source=recent_search_click&pc=1&spelling_corrections=1&include_ext_edit_control=true&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl%2Ccollab_control%2Cvibe',
               'scheme': 'https',
               'accept': '*/*',
               'accept-encoding': '',
               'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
               'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
               # 'cookie': 'guest_id_marketing=v1%3A166667526885979112; guest_id_ads=v1%3A166667526885979112; _ga=GA1.2.90083710.1666675272; _gid=GA1.2.208720928.1666675272; kdt=haoAurXsKba1QzgQArmyjksDpPIxI2NgYdsKXgdi; dnt=1; _sl=1; personalization_id="v1_s+fyK3WK3jNZxdSZKpb+4g=="; guest_id=v1%3A166676189695496518; ct0=c957e33ed33737a2fbe46ccce2767ad1; gt=1585140401979412480; g_state={"i_l":1,"i_p":1666769101996}',
               # 해쉬태그로 검색할경우
               'referer': 'https://twitter.com/search?q={}&src=recent_search_click&f=live'.format(parse.quote('#'+keyword)),
               'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': '"Windows"',
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-origin',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
               # csrf가 없어도되는지?
               # 'x-csrf-token': 'c957e33ed33737a2fbe46ccce2767ad1',
               'x-guest-token': '',
               'x-twitter-active-user': 'yes',
               'x-twitter-client-language': 'ko'}

    params['q'] = parse.quote('#'+keyword)
    # headers의 accept-encoding을 json으로 교체
    headers['accept-encoding'] = 'json'

    # headers의 x-guest-token 채우기
    # guest-token받아오기
    session, headers['x-guest-token'] = get_guest_token(session)

    # headers, parameters 설정 끝
    return (params, headers, session)


def t_crawler(keyword, nposts=450):  # keyword는 검색할 변수, nposts는 크롤링하고자하는 게시물 수
    print('Start Crawling... keyword : ', keyword)

    totalbf = datetime.now()
    nopostcnt = 0
    # 반환할 textlist
    textlist = list()
    ncrawled = 0
    # session 생성
    session = Session()
    # parameter 초기값 받아오기
    params, headers, session = set_params(keyword, session)

    # session 인스턴스 생성

    request_url = 'https://twitter.com/i/api/2/search/adaptive.json'

    # get 요청을 보낼 url 완성
    keys = list(params.keys())
    values = list(params.values())
    get_request_url = request_url+'?'
    for cursor in range(len(keys)):
        get_request_url += '%s=%s&' % (keys[cursor], values[cursor])
    get_request_url = get_request_url[:-1]

    # headers의 'path' 변수 변경
    headers['path'] = get_request_url[19:]

    # 1페이지 검색
    # get 요청 보내기 (1페이지)
    try:
        resp = session.get(get_request_url, headers=headers)
        respjson = resp.json()
        ncontents = len(respjson['globalObjects']['tweets'].keys())

        if ncontents == 0:
            nopostcnt += 1

        tmpcrawled = ncrawled
        textlist.append(list())
        for i in respjson['globalObjects']['tweets'].keys():
            textlist[0].append(respjson['globalObjects']
                               ['tweets'][i]['full_text'])
            ncrawled += 1
            if ncrawled >= nposts:
                print('수집 완료! 수집한 총 게시물 수 :', ncrawled)
                return textlist
        # 다음 페이지 가르키는 커서 변수에 값 넣어주기
        next_pg = respjson['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']
    except:
        print('\n\n\n!!!!!!!!!!!!!!!******알 수 없는 에러입니다******!!!!!!!!!!!!!!!\n\n\n')
        print('수집한 총 게시물 수 :', ncrawled)
        return textlist

    # 2페이지부터 추가 검색
    cur_page = 2
    while True:
        try:
            tmpcrawled = ncrawled
            params['cursor'] = next_pg
            get_request_url = request_url+'?'
            keys = list(params.keys())
            values = list(params.values())
            for cursor in range(len(keys)):
                get_request_url += '%s=%s&' % (keys[cursor], values[cursor])
            get_request_url = get_request_url[:-1]
            resp = session.get(get_request_url, headers=headers)
            respjson = resp.json()
            ncontents = len(respjson['globalObjects']['tweets'].keys())
            if ncontents == 0:  # 5페이지 연속으로 빈페이지가 나오는경우
                if nopostcnt > 5:
                    print('더 이상 수집할 게시물이 없습니다.')
                    print('수집한 총 게시물 수 :', ncrawled)
                    return textlist
                nopostcnt += 1
            else:
                nopostcnt = 0

            next_pg = respjson['timeline']['instructions'][-1]['replaceEntry']['entry']['content']['operation']['cursor']['value']

            textlist.append(list())
            for i in respjson['globalObjects']['tweets'].keys():
                textlist[-1].append(respjson['globalObjects']
                                    ['tweets'][i]['full_text'])
                ncrawled += 1
                if ncrawled >= nposts:
                    print('수집 완료! 수집한 총 게시물 수 :', ncrawled)
                    return textlist
            cur_page += 1
        except:
            print('\n\n\n!!!!!!!!!!!!!!!******알 수 없는 에러입니다******!!!!!!!!!!!!!!!\n\n\n')
            print('수집한 총 게시물 수 :', ncrawled)
            return textlist


def t_search(keyword):
    try:
        # db연결
        conn, cur = access_db()
        cur.execute(
            'SELECT tid FROM is_tag WHERE tname = (%s);', (keyword))
        res = cur.fetchall()
        # DB에 존재할 경우
        if len(res) >= 1:
            print('DB에서 해당 키워드를 찾았습니다.. keyword :', keyword)
            tid = res[0]['tid']
            conn.close()
            return (True, tid)
        close_db(conn)
        ######################## DB에 존재하지 않을경우, 크롤링->DB적재->값 반환 #####################
        delimiter = 'HOTKEY123!@#'
        textlist = t_crawler(keyword)
        corpus = ''
        delimiter = 'HOTKEY123!@#'
        for page in textlist:
            for post in page:
                corpus += delimiter + post
        conn, cur = access_db()
        cur.execute('insert into is_tag (tname) values (%s);', keyword)
        cur.execute('SELECT tid FROM is_tag WHERE tname = (%s);', keyword)
        tid = cur.fetchone()['tid']
        # tag_info에 저장
        cur.execute('insert into tag_info (tid, ttable, up_date, time_stamp) values (%s, %s, %s, %s);',
                    (tid, 3, time.strftime('%Y-%m-%d'), datetime.now().timestamp()))
        # n_corpus에 저장
        cur.execute(
            'insert into n_corpus (tid, corpus) values (%s, %s);', (tid, corpus[12:]))
        close_db(conn)
        return (True, tid)
    except:
        return (False, -1)

# 인스타그램 인기게시물 사진 가져오기


def top_image(query):
    session = Session()
    header = gen_header()
    images = list()
    resp = session.get(
        'https://www.instagram.com/api/v1/tags/logged_out_web_info/?tag_name={}'.format(parse.quote(query)), headers=header)
    try:
        resource = resp.json()
        for i in resource['data']['hashtag']['edge_hashtag_to_top_posts']['edges']:
            images.append(i['node']['thumbnail_resources'][-1]['src'])
        return (True, images[:9])
    except:
        print(resp.status_code)
        return (False, images)
