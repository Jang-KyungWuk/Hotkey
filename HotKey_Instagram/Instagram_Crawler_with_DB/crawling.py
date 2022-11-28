from requests import get, post, Session
from urllib import parse
import json
from datetime import datetime, timedelta
import emoji
import time
import random
from db import * #access_db, close_db

# account 정보 (사실상 전부 차단 전력있음)
total_acc = [('kj10522002@korea.ac.kr','kj76081460!'), ('quickpass8@gmail.com','thskrl1!'),('hotkey2','gktzl2'),
                 ('seungirumd+1@gmail.com', 'pinstaw25'), ('lshyun0510.11@gmail.com', '*thvmxmdnpdj'),
                 ('seyun1052dev@gmail.com', 'kj76081460!'), ('lshyun0510.12@gmail.com', '*thvmxmdnpdj'),
                 ('quickpass88@gmail.com', 'thskrl1!'), ('hotkey22', 'gktzl22!'), ('tamikia0@hbviralbv.com', 'cvd0^ktm')]
#using_acc.sort(key=lambda x:x[2]) #최종 로그인 날짜에 따라 sorting하는 logic
delimiter = 'HOTKEY123!@#' #corpus생성을 위한 구분자
cur_idx = -1 #추후 삭제?

# 로그인 함수
def login(id, pw):
    # 새로운 헤더, 세션 생성 (새로운 세션 리턴)
    # 헤더, 세션, status를 리턴
    # status = 0 : success , 1 : checkpoint_needed 에러 (수동 인증 필요) 2 : incorrect pw 에러 (임시 차단)
    # 3. CSRF 에러 (IP문제) 4. 그 외

    header, session = dict(), Session()
    header['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'
    header['x-ig-app-id'] = '936619743392459'

    resp = session.get('https://www.instagram.com/data/manifest.json', headers=header)
    header['x-csrftoken'] = session.cookies.get('csrftoken')
    url = 'https://i.instagram.com/api/v1/web/accounts/login/ajax/'
    params = {'enc_password': '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(
        int(datetime.now().timestamp()), pw), 'username': id, 'optIntoOneTap': 'false'}

    resp = session.post(url, data=params, headers=header)  # 로그인 요청

    if resp.status_code == 400:
        print('Login Error : checkpoint_needed (수동 인증 필요) ...')
        print(resp.text)
        return header, session, 1
    elif resp.status_code == 403:
        print('Login Error : CSRF error (IP 문제) ,,, ')
        print(resp.text)
        return header, session, 3
    elif resp.status_code == 200:
        if not (resp.json()['authenticated']):
            print('Login Error : incorrect pw (계정 임시 차단 혹은 pw인증 에러)...')
            print(resp.json())
            return header,session,2
        else:
            print('Login Successful')
            return header, session, 0
    else:
        print('Login Error : unknown,,, response status code:', resp.status_code)
        print(resp.text)
        return header, session, 4

# 최근 게시물 생성 함수
def hot_key_instagram_recent(query, headers, session, max_page=40):
    # return (status, recent_list, timestamp, image_list)
    # status = 0 : success, 1 : 크롤링 중 문제 발생 (CSRF error), code는 200 , 2 : 400error - 계정에 checkpoint 필요
    # 3 : 검열 혹은 페이지 x,  4 : 그 외
    postcnt = 0  # 포스트 수 카운팅, 300개 되면 stop.
    timestamp = 0

    before = datetime.now()
    recent_list = list()
    image_list = list()

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
        # print(resp.content)
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

    print('누적 게시물 수 :', postcnt)
    print('최근 게시물 수집 완료!')
    print('총 소요시간 : ', datetime.now() - before, '\n')
    return (0, recent_list, timestamp, image_list)

#single_search 알고리즘
#주피터 노트북에 있는거 수정해서 올려야함. (session을 자동으로 해준다고 가정하고 ㅇㅇ)