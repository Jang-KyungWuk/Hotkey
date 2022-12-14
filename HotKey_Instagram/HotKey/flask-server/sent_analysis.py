#!/usr/bin/env python
# coding: utf-8
import preprocess as pp
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt

"""spamfilter를 통과한 플레인텍스트를 받아서 감성분석 수행
기본 디렉토리 ./templates/ 에 sent_pie.jpg 저장
return True
"""


def sent_analysis(plaintext,
                  sentMorph=['IC', 'MAG', 'MM', 'NNB', 'NNG', 'NNP',
                             'NP', 'NR', 'SL', 'SP', 'SW', 'VA', 'XR'],
                  saveDir='../react-client/src/visualization/sent_results/', fileName='sent_pie',
                  sentDictFile='sent_dict.pkl',
                  legends=['Positive', 'Neutral', 'Negative'],
                  colors=['#FFBF25', '#D6DFE1', '#272B3A'],
                  topSentReturn=12):
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

        sent_visualization(ratios,
                           saveDir=saveDir, fileName=fileName,
                           legends=legends, colors=colors)

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
                       saveDir='../react-client/src/visualization/sent_results/', fileName='sent_pie',
                       legends=['Positive', 'Neutral', 'Negative'],
                       colors=['#FFBF25', '#D6DFE1', '#272B3A'],
                       plotType='pie'):

    if plotType == 'pie':
        label = ["%s%%" % (ratio) for ratio in ratios]
        plt.pie(ratios, labels=label, labeldistance=0.6, colors=colors)
        plt.legend(legends)
        plt.savefig(saveDir+fileName+'.jpg')

    elif plotType == 'bar':
        cratios = list()
        for cursor in range(len(ratios)):
            cratios.append(np.sum(ratios[:cursor+1]))

        fig = plt.figure(figsize=(8, 1))

        for cursor in range(len(cratios)-1, -1, -1):
            plt.barh(['ratio'], [cratios[cursor]], color=colors[cursor])
            plt.barh(['ratio'], [cratios[cursor]], color=colors[cursor])
            plt.barh(['ratio'], [cratios[cursor]], color=colors[cursor])

        plt.xlim(-10, 110)
        plt.savefig(saveDir+fileName+'.jpg')
