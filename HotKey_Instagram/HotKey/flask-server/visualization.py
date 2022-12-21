from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
# import plotly.express as px
import seaborn as sns
import pandas as pd
import re
from preprocess import *


def frequency(pt):
    """
    ------------------------------------------------------------------------------

    preprocess 함수의 리턴값으로 각 단어의 빈도 수를 나타내는 딕셔너리를 리턴합니다.
    키 값으로 단어를, 밸류 값으로 빈도 수를 갖습니다.

    ------------------------------------------------------------------------------

    파라미터 설명

    pt : list, preprocess 함수의 리턴값

    ------------------------------------------------------------------------------
    """
# 토큰들의 빈도를 dict형태로 저장
    voca = dict()
    for post in pt:
        for term in post:
            if term in voca:
                voca[term] += 1
            else:
                voca[term] = 1

    return voca


def wordcloud(pt, wc_filename='./images/visualization/wordcloud/tmp.png', wc_backgroundcolor='white',
              wc_colormap='copper', font_path='./templates/fonts/Chosun.ttf'):
    """
    ------------------------------------------------------------------------------

    frequency 함수의 리턴값으로 wordcloud 이미지 파일을 생성합니다.

    ------------------------------------------------------------------------------

    파라미터 설명

    pt : list, preprocess 함수의 리턴값
    wc_filename : str, 저장할 wordcloud 이미지 파일의 이름
    wc_backgroundcolor : str, wordcloud 그림파일의 배경색, 기본값은 'white'
    wc_colormap : str, wordcloud 그림파일의 컬러맵(wordcloud 모듈에 저장된), 기본값은 'autumn'
    font_path : str, wordcloud에 쓰일 폰트, 기본값은 'Chosun.ttf'

    ------------------------------------------------------------------------------
    """
    try:
        # frequency함수를 통해 빈도 딕셔너리 가져오기
        voca = frequency(pt)

        # 이미지 파일 읽어오기
        im = Image.open('./templates/masks/mask_camera.png')

        # 이미지 파일 전처리
        mask = Image.new("RGB", im.size, (255, 255, 255))
        mask.paste(im)
        mask = np.array(mask)

        # wordcloud 이미지 생성
        wc = WordCloud(background_color=wc_backgroundcolor,
                       colormap=wc_colormap, font_path=font_path, mask=mask, min_font_size=11)
        wc = wc.generate_from_frequencies(voca)

        # 입력받은 경로에 저장
        wc.to_file(filename=f'{wc_filename}')

        return True
    except:
        return False


def barplot(pt, bp_filename='./images/visualization/barplot/tmp.png'):
    """
    ------------------------------------------------------------------------------

    preprocess 함수의 리턴값으로 barplot 이미지 파일을 생성합니다.

    ------------------------------------------------------------------------------

    파라미터 설명

    pt : list, preprocess 함수의 리턴값
    bp_filename : str, 저장할 barplot 이미지 파일의 이름

    ------------------------------------------------------------------------------

    """

    try:
        # 데이터 전처리
        ptlist = []
        for post in pt:
            ptlist.extend(post)
        text_c = ' '.join(ptlist)

    # Pandas DataFrame 만드는 함수
        def get_df(input_text):
            list_words = input_text.split(' ')
            set_words = list(set(list_words))

            count_words = [list_words.count(i) for i in set_words]

            df = pd.DataFrame(zip(set_words, count_words),
                              columns=['words', 'count'])
            df.sort_values('count', ascending=False, inplace=True)
            df.reset_index(drop=True, inplace=True)
            return df

    # seaborn palette 에서 색을 가져오는 함수
        def get_colordict(palette, number, start):
            pal = list(sns.color_palette(
                palette=palette, n_colors=number).as_hex())
            color_d = dict(enumerate(pal, start=start))
            return color_d

        df_words = get_df(text_c)

    # barplot
        index_list = [[i[0], i[-1]+1] for i in np.array_split(range(100), 5)]

        n = df_words['count'].max()
        color_dict = get_colordict('bone_r', n, 1)
        plt.rcParams['font.family'] = 'Malgun Gothic'

        fig, axs = plt.subplots(1, 1, figsize=(
            4, 8), facecolor='white', squeeze=False)
        for col, idx in zip(range(0, 1), index_list):
            df = df_words[idx[0]:idx[-1]]
            label = [w + ': ' + str(n)
                     for w, n in zip(df['words'], df['count'])]
            color_l = [color_dict.get(i) for i in df['count']]
            x = list(df['count'])
            y = list(range(0, 20))

            sns.barplot(x=x, y=y, data=df, alpha=0.9, orient='h',
                        ax=axs[0][col], palette=color_l)
            axs[0][col].set_xlim(0, n+1)
            axs[0][col].set_yticklabels(label, fontsize=12)
            axs[0][col].spines['bottom'].set_color('white')
            axs[0][col].spines['right'].set_color('white')
            axs[0][col].spines['top'].set_color('white')
            axs[0][col].spines['left'].set_color('white')

        plt.tight_layout()
        plt.savefig(f'{bp_filename}')

        return True
    except:
        return False
