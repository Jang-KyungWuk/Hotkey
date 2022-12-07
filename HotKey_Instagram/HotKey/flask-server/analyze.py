from db import *

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
