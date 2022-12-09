
from db import *
from urllib import request
from crawling import *


# tid를 전달받으면 db에서 corpus랑 image꺼내오는 함수
def get_corpus(tid):
    conn, cur = access_db()
    # 여기서 구현
    corpus = ''  # 임시
    close_db(conn)
    return corpus


"""
single search를 수행하면 서버에는 tid만 전달된다.
프론트에 이미지가 전달되려면,
tid를 받아서 tname을 찾고
디렉토리에 top_image를 실행해서 이미지들을 저장한 뒤
경로들을 리스트로 만들기. 리스트로 리턴해주기
"""
# tid를 받아서 이미지를 저장하고, 폴더에 저장된 이미지 이름 리스트를 반환하는 함수
# //default image 생성해두기
# DB에서 image테이블없애기,,
# blob 인사이트 생각 => DB에 blob형태로 저장하면 서버에 저장할 필요가 없음. (이건 일단 서버에 저장하는 걸로 구현하되, 발표할때는 blob으로 DB활용하는 아이디어 생각.)


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
        return (False, [])
    image_name = []
    for idx, url in enumerate(images):
        filename = tname+str(idx)
        save_path = '../react-client/src/top_imgs/'+filename+'.jpg'
        request.urlretrieve(url, save_path)
        image_name.append(filename+'.jpg')
    return (True, image_name)
