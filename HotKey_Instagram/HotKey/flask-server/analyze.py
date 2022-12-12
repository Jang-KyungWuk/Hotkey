from db import *
from urllib import request
from crawling import *
from sent_analysis import *
from preprocess import *
from lda import *
from network import *
from visualization import *

# tid를 전달받으면 db에서 corpus를 꺼내오는 함수, (성공여부, corpus)를 반환


def get_corpus(tid):
    corpus = ''  # 임시
    conn, cur = access_db()
    try:
        cur.execute('select tname from is_tag where tid = (%s)', (tid))
        keyword = cur.fetchone()['tname']
        cur.execute(
            'select ttable FROM tag_info WHERE tid= (%s)', (tid))
        ttable = cur.fetchone()['ttable']
        if ttable == 1:  # s_corpus
            cur.execute('select corpus from s_corpus where tid=(%s)', (tid))
            corpus = cur.fetchone()['corpus']
        elif ttable == 2:  # t_corpus
            cur.execute('select corpus from t_corpus where tid=(%s)', (tid))
            corpus = cur.fetchone()['corpus']
        else:  # n_corpus
            cur.execute('select corpus from n_corpus where tid=(%s)', (tid))
            corpus = cur.fetchone()['corpus']
        if (len(corpus) == 0):
            close_db(conn)
            print("get_corpus error...")
            return (False, '', '')
    except:
        close_db(conn)
        print("get_corpus error...")
        return (False, '', '')
    close_db(conn)
    print('db에서 corpus가져오기 성공')
    return (True, keyword, corpus)

# tid를 받아서 이미지를 저장하고, 폴더에 저장된 이미지 이름 리스트를 반환하는 함수
# //default image 생성해두기
# DB에서 image테이블없애기,,


def get_image(tid):
    conn, cur = access_db()
    cur.execute('SELECT tname FROM is_tag WHERE tid = (%s);', tid)
    tname = cur.fetchone()['tname']  # tname 변수 저장
    close_db(conn)
    images = []
    for i in range(3):
        status, images = top_image(tname)
        if (status):
            break
    if not status:
        return (False, '', 0)
    imagenum = 0
    for idx, url in enumerate(images):
        filename = tname+str(idx)
        save_path = '../react-client/src/top_imgs/'+filename+'.jpg'
        request.urlretrieve(url, save_path)
        imagenum += 1
    return (True, tname, imagenum)

# 감성분석 테스트용 임시..


def sent_test(corpus):
    plaintext = corpus
    print("spam_filtering 시작...")
    pt, status = spam_filter(plaintext)
    if not status:
        print('Error during spam_filtering...')
        return False
    print("spam_filtering 완료...")
    print("sent_analysis 시작....")
    # 여기서 fileName지정하면, ./templates/sent_results/에 fileName.jpg로 저장
    status = sent_analysis(pt, fileName="tmp")
    if not status:
        print('Error during sent_analysis...')
        return False
    return True

# LDA 테스트용 임시..


def LDA_test(corpus):
    # LDA는 spam_filtering되지 않은 original corpus를 인풋으로 받음.
    plaintext = corpus
    print("LDA 분석 시작... (+토픽별 워드클라우드생성)")
    status, topic_list = sklda(plaintext)
    print("LDA 분석 완료")
    return (status, topic_list)


# 네트워크 테스트용 임시.. + LDA
# def network_test(corpus):
#     plaintext = corpus
#     pt, status = spam_filter(plaintext)
#     if not status:
#         print('Error during spam_filtering...')
#         return False
#     print("spam_filtering 완료...")
#     print("LDA 분석 + 토픽별 워드클라우드 생성 시작... path : ./templates/lda_results")
#     status, topic_list = sklda(plaintext)  # LDA는 스팸필터링 되지 않은 코퍼스를 인풋으로 받음
#     if not status:
#         print('Error during LDA Analysis...')
#         return False
#     print("network 생성 시작... path : ./templates/networks")
#     status = network(pt, topic_list)  # 스팸필터링된 plaintext와 LDA 결과값을 인풋으로 받음
#     if not status:
#         print('Error during network analysis...')
#         return False
#     return True

# 워드클라우드 & bar plot 테스트용 임시..


# def visualization_test(corpus):
#     plaintext = corpus
#     # wordcloud, barplot에 들어갈 input 형식 (리스트)
#     print("전처리함수 실행")
#     pt = preprocess(plaintext=plaintext, sep='HOTKEY123!@#')
#     print("전처리완료.. - 반환 : 리스트 형식")
#     print("wordcloud 생성 시작")
#     status = wordcloud(pt)
#     if not status:
#         print('wordcloud 생성 중 에러...')
#         return False
#     print("barplot 생성 시작")
#     status = barplot(pt)
#     if not status:
#         print('barplot 생성 중 에러..')
#         return False
#     return True
