#!/usr/bin/env python
# coding: utf-8
import preprocess as pp
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

"""spamfilter를 통과한 플레인텍스트를 받아서 감성분석 수행
기본 디렉토리 ./templates/ 에 sent_pie.jpg 저장
return True
"""


def sent_analysis(plaintext,
                  sentMorph=['IC', 'MAG', 'MM', 'NNB', 'NNG', 'NNP',
                             'NP', 'NR', 'SL', 'SP', 'SW', 'VA', 'XR'],
                  saveDir='./templates/', fileName='sent_pie',
                  sentDictFile='sent_dict.pkl',
                  colors=['#FFBF25', '#D6DFE1', '#272B3A'],
                  fontPath=None,
                  topSentReturn=12):
    '''
    multi tok sent
    NNG,EFN,VV,VA,XR,ECS,EMO,ETD,VXV,VXA,JC,MAG,ECD,XR,ECE,JKG,MDT,JKO,NNB,NNP,JKS,JKM,ETN,XSV,XSA,XSN,NP,IC,VCN,NNM,MDN,JX

    single tok sent
    'IC', 'MAG', 'MM', 'NNB', 'NNG', 'NNP', 'NP', 'NR', 'SL', 'SP', 'SW', 'VA', 'XR'
    '''
    try:

        # 감성 사전을 열고 데이터를 불러옴
        with open(sentDictFile, 'rb') as file:
            sentDict = pkl.load(file)

        # 감성 사전과 동일한 기준으로 토큰화 수행
        tokenized = pp.data_tokenize(data=pp.plain_structurize(plaintext),
                                     morphemeAnalyzer=pp.setMorphemeAnalyzer(
            "키위"),
            targetMorphs=sentMorph)

        # 긍정 / 중립 / 부정 키워드들을 관리하는 dict
        positiveDict = dict()
        neutralDict = dict()
        negativeDict = dict()

        # 포스트별, 토큰별로 돌면서 감성 사전에 등재된 단어인지 체크하고 등재된 단어일 시 점수에 따라 긍정/중립/부정 dict에 추가
        for post in tokenized:
            for kwd in post:
                if kwd in sentDict:
                    if sentDict[kwd] > 0:
                        try:
                            positiveDict[kwd] += 1
                        except:
                            positiveDict[kwd] = 1

                    elif sentDict[kwd] == 0:
                        try:
                            neutralDict[kwd] += 1
                        except:
                            neutralDict[kwd] = 1
                    else:
                        try:
                            negativeDict[kwd] += 1
                        except:
                            negativeDict[kwd] = 1

        # 비율 계산
        ratios = np.array([sum(list(positiveDict.values())),
                           sum(list(neutralDict.values())),
                           sum(list(negativeDict.values()))], dtype='float16')
        counts = np.sum(ratios)
        ratios = ratios/counts*100

        # 시각화
        sent_visualization(ratios, saveDir=saveDir, fileName=fileName)

        # 빈도수가 높은 순으로 키워드 - 빈도 - 긍부정 여부을 하나의 튜플로 묶은 데이터의 list를 반환
        sentKwds = list(positiveDict.keys()) + \
            list(neutralDict.keys())+list(negativeDict.keys())
        sentLabels = ['긍정' for cursor in range(len(positiveDict))]+['중립' for cursor in range(
            len(neutralDict))]+['부정' for cursor in range(len(negativeDict))]
        sentKwdCounts = list(positiveDict.values()) + \
            list(neutralDict.values())+list(negativeDict.values())

        results = list()
        for got in range(topSentReturn):
            idx = sentKwdCounts.index(max(sentKwdCounts))
            results.append(
                (sentKwds.pop(idx), sentKwdCounts.pop(idx), sentLabels.pop(idx)))

        return (True, results)
    except:
        return (False, [])


def sent_visualization(ratios,
                       saveDir='', fileName='sent_pie',
                       legends=['Positive', 'Neutral', 'Negative'],
                       colors=['#7DB3F2', '#D6DFE1', '#E17781']):
    '''
    ------------------------------------------------------------------------------

    긍정,중립,부정의 비율을 받아 파이 차트를 생성, 입력받은 경로에 저장합니다.

    ------------------------------------------------------------------------------

    파라미터 설명

    ratios : list of numbers, 긍정, 중립, 부정의 비율
    saveDir : str, 저장할 파이차트 이미지 파일 경로, 기본값 ''
    fileName : str, 저장할 파이차트 이미지 파일 이름, 기본값 'sent_pie'
    legends : list of strings, 범례, 기본값 ['Positive', 'Neutral', 'Negative']
    colors : list of strings, 파이차트의 각 범례 별 색, 기본값 ['#7DB3F2','#D6DFE1','#E17781']

    ------------------------------------------------------------------------------
    '''

    df = pd.DataFrame(zip(legends, ratios), columns=['legends', 'ratios'])
    df.sort_values('ratios', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    fig = px.pie(df, values='ratios', names='legends', color='legends',
                 color_discrete_map={'Positive': '#7DB3F2', 'Neutral': '#D6DFE1', 'Negative': '#E17781'})

    fig.update_traces(textposition='outside', textinfo='percent+label',
                      hole=.4, hoverinfo="label+percent+name", pull=[0.1, 0, 0])
    fig.update_layout(width=600, height=600, margin=dict(
        t=0, l=0, r=0, b=0), showlegend=False)
    fig.write_image(saveDir+fileName+'.png')
