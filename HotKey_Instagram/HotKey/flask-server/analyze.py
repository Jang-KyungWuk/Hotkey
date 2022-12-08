from db import *
from urllib import request

# 1. tid를 전달받으면 db에서 corpus랑 image꺼내오는 함수 만들기


def get_corpus(tid):
    conn, cur = access_db()
    # 여기서 구현
    corpus = ''  # 임시
    close_db(conn)
    return corpus


def get_image(tid):
    conn, cur = access_db()
    # 여기서 구현
    image = ''  # 임시
    close_db(conn)
    return image
# 2. post의 index 9개를 전달받으면 image에서 그 index에 해당하는 이미지 9개 가져와서 어딘가에 저장하는 함수 만들기
# 로직 :
# single_search실행 중, 1) db에 없는 새로운 키워드인경우 => 수집하면서 그대로 이미지 url들도 전달
# 2) db에 있는 키워드 인경우 => 세션 가능한거 아무거나 하나 로그인해서 첫페이지만 받아오기.
# //default image 생성해두기
# DB에서 image테이블없애기,,?
# blob 인사이트 생각 => DB에 blob형태로 저장하면 서버에 저장할 필요가 없음. (이건 일단 서버에 저장하는 걸로 구현하되, 발표할때는 blob으로 DB활용하는 아이디어 생각.)


# 받은 이미지 url을 가지고 특정 경로에 저장하는 함수
def save_image(imgurl, filename):
    # react-client\public\tmp_imgs에 저장
    # filename규칙 => <tag_name><0~8>.jpg
    save_path = '../react-client/public/top_imgs/'+filename+'.jpg'
    download_file = request.urlretrieve(imgurl, save_path)
    return
