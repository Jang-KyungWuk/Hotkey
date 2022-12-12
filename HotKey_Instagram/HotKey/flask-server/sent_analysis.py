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
                  saveDir='../react-client/src/visualization/sent_results/', fileName='tmp',
                  sentDictFile='sent_dict.pkl',
                  legends=['Positive', 'Neutral', 'Negative'],
                  colors=['#5555ff', '#55ff55', '#ff5555']):
    try:
        with open(sentDictFile, 'rb') as file:
            sentDict = pkl.load(file)

        tokenized = pp.data_tokenize(data=pp.plain_structurize(plaintext),
                                     morphemeAnalyzer=pp.setMorphemeAnalyzer(
            "키위"),
            targetMorphs=sentMorph)
        positiveCount = 0
        neutralCount = 0
        negativeCount = 0

        for post in tokenized:
            for kwd in post:
                if kwd in sentDict:
                    if sentDict[kwd] > 0:
                        positiveCount += 1
                    elif sentDict[kwd] == 0:
                        neutralCount += 1
                    else:
                        negativeCount += 1

        ratios = np.array([positiveCount, neutralCount,
                           negativeCount], dtype='float16')
        counts = np.sum(ratios)
        ratios = ratios/counts*100

        sent_visualization(ratios,
                           saveDir=saveDir, fileName=fileName,
                           legends=legends, colors=colors)
        return True
    except:
        return False


def sent_visualization(ratios,
                       saveDir='./templates/sent_results/', fileName='sent_pie',
                       legends=['Positive', 'Neutral', 'Negative'],
                       colors=['#5555ff', '#55ff55', '#ff5555']):

    label = ["%s%%" % (ratio) for ratio in ratios]
    plt.pie(ratios, labels=label, labeldistance=0.6, colors=colors)
    plt.legend(legends)
    plt.savefig(saveDir+fileName+'.jpg')
