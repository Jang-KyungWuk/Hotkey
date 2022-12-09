from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import plotly.express as px
import seaborn as sns
import pandas as pd
import seaborn as sns
import re


def ranking(plaintext, wcfilename='wordcloud.png', bpfilename='barplot.png',
            ppfilename='pieplot.png', wc_backgroundcolor='black', wc_colormap='autumn'):
    """
    ------------------------------------------------------------------------------

    텍스트를 받아 전처리함수를 통해 토큰화 한 후 빈도를 기반으로 그림파일을 생성합니다. 
    키값으로 토큰, 밸류값으로 빈도 수를 갖는 딕셔너리를 반환합니다.

    ------------------------------------------------------------------------------

    파라미터 설명

    plaintext : txt, 인스타그램 포스트들이 수집된 원문 텍스트. 'HOTKEY123!@#'로 포스트들을 구분한다.
    wcfilename : str, wordcloud 파일이름.
    bpfilename : str, barplot 파일이름.
    ppfilename : str, pieplot 파일이름.
    wc_backgroundcolor : str, wordcloud 그림파일의 배경색, 기본값은 'black'.
    wc_colormap : str, wordcloud 그림파일의 컬러맵(wordcloud 모듈에 저장된), 기본값은 'autumn'.

    ------------------------------------------------------------------------------
    """

# 입력받은 원문을 전처리함수를 통해 토큰화
    pt = preprocess(plaintext=plaintext, sep='HOTKEY123!@#',
                    targetMorphs=['NNP', 'NNG'])

# 토큰들의 빈도를 dict형태로 저장
    voca = dict()
    for post in pt:
        for term in post:
            if term in voca:
                voca[term] += 1
            else:
                voca[term] = 1

# 빈도 순(밸류값)으로 정렬
    voca_sorted = sorted(voca.items(), key=lambda x: x[1], reverse=True)

# 한글로 wordcloud 이미지를 생성하기 위해 글꼴 불러오기
    font_path = 'malgun.ttf'

# 이미지 파일 읽어오기
    im = Image.open('mask_camera.png')

# 이미지 파일 전처리
    mask = Image.new("RGB", im.size, (255, 255, 255))
    mask.paste(im)
    mask = np.array(mask)

# wordcloud 이미지 생성
    wc = WordCloud(background_color='black', colormap=wc_colormap,
                   font_path=font_path, mask=mask)
    wc = wc.generate_from_frequencies(voca)

# 입력받은 경로에 저장, 파일이름 중복될 경우 덮어쓰여짐
    wc.to_file(filename=f'{wcfilename}')

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
    color_dict = get_colordict('PuRd', n, 1)
    plt.rcParams['font.family'] = 'Malgun Gothic'

    fig, axs = plt.subplots(1, 1, figsize=(
        4, 8), facecolor='white', squeeze=False)
    for col, idx in zip(range(0, 1), index_list):
        df = df_words[idx[0]:idx[-1]]
        label = [w + ': ' + str(n) for w, n in zip(df['words'], df['count'])]
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
    plt.savefig(f'{bpfilename}')

# pieplot
    pal = list(sns.color_palette(palette='PuRd_r', n_colors=30).as_hex())

    fig = px.pie(df_words[0:20], values='count', names='words',
                 color_discrete_sequence=pal)

    fig.update_traces(textposition='outside', textinfo='percent+label',
                      hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(width=800, height=600,
                      margin=dict(t=0, l=0, r=0, b=0))

    fig.write_image(f'{ppfilename}')

    return voca_sorted
