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
    return (True, keyword, corpus)

# tid를 받아서 이미지를 저장하고, 폴더에 저장된 이미지 이름 리스트를 반환하는 함수


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
        save_path = './images/top_imgs/'+filename+'.jpg'
        request.urlretrieve(url, save_path)
        imagenum += 1
    return (True, tname, imagenum)
