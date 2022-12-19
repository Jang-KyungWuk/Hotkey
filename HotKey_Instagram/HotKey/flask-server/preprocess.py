# Morpheme Analyze
from kiwipiepy import Kiwi
import konlpy
import nltk

# Preprocess
import re
import emoji

# BM25
from math import log1p
import numpy as np


class nltkMA:
    def __init__(self, maParamDict=None):
        """
        create instance and set parameters
        """
        # nltk로 형태소 분석에 사용되는 패러미터들을 할당
        self.morph_header = 'NLTK_'
        self.word_tokenize_language = 'english'
        self.word_tokenize_preserve_line = False
        self.pos_tag_tagset = None
        self.pos_tag_lang = 'eng'

        if maParamDict == None:
            pass

        else:
            if 'morph_header' in maParamDict:
                self.morph_header = maParamDict['morph_header']
            elif 'header' in maParamDict:
                self.morph_header = maParamDict['header']

            if 'word_tokenize_language' in maParamDict:
                self.word_tokenize_language = maParamDict['word_tokenize_language']
            elif 'language' in maParamDict:
                self.word_tokenize_language = maParamDict['language']

            if 'word_tokenize_preserve_line' in maParamDict:
                self.word_tokenize_preserve_line = maParamDict['word_tokenize_preserve_line']
            elif 'preserve_line' in maParamDict:
                self.word_tokenize_preserve_line = maParamDict['preserve_line']

            if 'pos_tag_tagset' in maParamDict:
                self.pos_tag_tagset = maParamDict['pos_tag_tagset']
            elif 'tagset' in maParamDict:
                self.pos_tag_tagset = maParamDict['tagset']

            if 'pos_tag_lang' in maParamDict:
                self.pos_tag_lang = maParamDict['pos_tag_lang']
            elif 'lang' in maParamDict:
                self.pos_tag_lang = maParamDict['lang']

    def __call__(self, text):
        """
        nltk.pos_tag(nltk.word_tokenize(text input))
        """
        result = list()
        for token in nltk.pos_tag(nltk.word_tokenize(text,
                                                     language=self.word_tokenize_language,
                                                     preserve_line=self.word_tokenize_preserve_line),
                                  tagset=self.pos_tag_tagset,
                                  lang=self.pos_tag_lang):
            result.append([token[0], self.morph_header+token[1]])
        return result


class setMorphemeAnalyzer:
    def __init__(self, maText, maParamDict=None):
        '''
        maText 를 토대로 형태소 분석기의 종류를 구분
        maParamDict에 해당 형태소 분석기의 패러미터로 넣을 수 있는 값이 있으면 해당 값을, 없으면 기본값을 설정
        형태소 분석기의 tokenize (키위) / pos (KoNLPy 계열) 함수에 __call__을 통해 입력받을 수 있는 형태의 인스턴스를 반환
        '''
        if maText in ['kiwi', 'Kiwi', 'KIWI', '키위']:
            if maParamDict == None:
                self.ma = Kiwi().tokenize
            else:
                if 'num_workers' in maParamDict:
                    num_workers = maParamDict['num_workers']
                else:
                    num_workers = None

                if 'model_path' in maParamDict:
                    model_path = maParamDict['model_path']
                else:
                    model_path = None

                if 'options' in maParamDict:
                    options = maParamDict['options']
                else:
                    options = None

                if 'integrate_allomorph' in maParamDict:
                    integrate_allomorph = maParamDict['integrate_allomorph']
                else:
                    integrate_allomorph = None

                if 'load_default_dict' in maParamDict:
                    load_default_dict = maParamDict['load_default_dict']
                else:
                    load_default_dict = None

                if 'load_typo_dict' in maParamDict:
                    load_typo_dict = maParamDict['load_typo_dict']
                else:
                    load_typo_dict = None,

                if 'model_type' in maParamDict:
                    model_type = maParamDict['model_type']
                else:
                    model_type = 'knlm',

                if 'typos' in maParamDict:
                    typos = maParamDict['typos']
                else:
                    typos = None,

                if 'typo_cost_threshold' in maParamDict:
                    typo_cost_threshold = maParamDict['typo_cost_threshold']
                else:
                    typo_cost_threshold = 2.5

                self.ma = Kiwi(num_workers=num_workers, model_path=model_path,
                               options=options, integrate_allomorph=integrate_allomorph,
                               load_default_dict=load_default_dict, load_typo_dict=load_typo_dict,
                               model_type=model_type, typos=typos, typo_cost_threshold=typo_cost_threshold).tokenize

        elif maText in ['Hannanum', 'hannanum', 'HANNANUM', '한나눔']:
            if maParamDict == None:
                self.ma = konlpy.tag.Hannanum().pos
            else:
                if 'jvmpath' in maParamDict:
                    jvmpath = maParamDict['jvmpath']
                else:
                    jvmpath = None

                if 'max_heap_size' in maParamDict:
                    max_heap_size = maParamDict['max_heap_size']
                else:
                    max_heap_size = 1024

                self.ma = konlpy.tag.Hannanum(
                    jvmpath=jvmpath, max_heap_size=max_heap_size).pos

        elif maText in ['Komoran', 'KOMORAN', 'komoran', '코모란']:
            if maParamDict == None:
                self.ma = konlpy.tag.Komoran().pos
            else:
                if 'jvmpath' in maParamDict:
                    jvmpath = maParamDict['jvmpath']
                else:
                    jvmpath = None

                if 'userdic' in maParamDict:
                    userdic = maParamDict['userdic']
                else:
                    userdic = None

                if 'modelpath' in maParamDict:
                    modelpath = maParamDict['modelpath']
                else:
                    modelpath = None

                if 'max_heap_size' in maParamDict:
                    max_heap_size = maParamDict['max_heap_size']
                else:
                    max_heap_size = 1024

                self.ma = konlpy.tag.Komoran(jvmpath=jvmpath, userdic=userdic,
                                             modelpath=modelpath, max_heap_size=max_heap_size).pos

        elif maText in ['Kkma', 'KKMA', 'kkma', '꼬꼬마']:
            if maParamDict == None:
                self.ma = konlpy.tag.Kkma().pos
            else:
                if 'jvmpath' in maParamDict:
                    jvmpath = maParamDict['jvmpath']
                else:
                    jvmpath = None

                if 'max_heap_size' in maParamDict:
                    max_heap_size = maParamDict['max_heap_size']
                else:
                    max_heap_size = 1024

                self.ma = konlpy.tag.Kkma(
                    jvmpath=jvmpath, max_heap_size=max_heap_size).pos

        elif maText in ['Okt', 'OKT', 'okt', '오픈코리안텍스트', '트위터']:
            if maParamDict == None:
                self.ma = konlpy.tag.Okt().pos
            else:
                if 'jvmpath' in maParamDict:
                    jvmpath = maParamDict['jvmpath']
                else:
                    jvmpath = None

                if 'max_heap_size' in maParamDict:
                    max_heap_size = maParamDict['max_heap_size']
                else:
                    max_heap_size = 1024

                self.ma = konlpy.tag.Okt(
                    jvmpath=jvmpath, max_heap_size=max_heap_size).pos

        elif maText in ['Mecab', 'mecab', 'MECAB', '미캐브']:
            if maParamDict == None:
                self.ma = konlpy.tag.Mecab().pos
            else:
                if 'dicpath' in maParamDict:
                    dicpath = maParamDict['dicpath']
                else:
                    dicpath = '/usr/local/lib/mecab/dic/mecab-ko-dic'

                self.ma = konlpy.tag.Mecab(dicpath=dicpath).pos

        else:
            raise Exception(
                'No such morpheme analyzer\nSupported morpheme analyzers are Kiwi, KoNLPy(Hannanum, Komoran, Kkma, Okt, Mecab)')

    def __call__(self, text):
        '''
        기존의 (토큰,품사) 튜플들을 담은 리스트를 반환하는 구조 대신 [토큰, 품사] 리스트를 담은 리스트를 반환
        '''
        result = list()
        for token in self.ma(text):
            result.append([token[0], token[1]])
        return result


def preprocess(plaintext, sep='HOTKEY123!@#',
               returnIndex=False, returnTopIndex=None,
               returnPlain=False, returnMorph=False,
               multiReturn=False,
               removeHashTag=True,
               kwdMinLen=2,
               morphemeAnalyzer='okt', morphemeAnalyzerParams=None, targetMorphs=['Noun'],
               returnEnglishMorph=True, EETagRule={'NLTK_NNP': 'Noun', 'NLTK_NN': 'Noun', 'R_W_HASHTAG': 'W_HASHTAG', 'R_W_EMJ': 'EMJ'},
               enMorphemeAnalyzerParams=None,
               filterMorphemeAnalyzer='okt', filterMorphemeAnalyzerParams=None, filterTargetMorphs=['Noun', 'W_HASHTAG'],
               filterEnglishMorph=True, filterEETagRule={'NLTK_NNP': 'Noun', 'NLTK_NN': 'Noun', 'R_W_HASHTAG': 'W_HASHTAG'},
               filterEnMorphemeAnalyzerParams=None,
               k_1Filter=1.5, bFilter=0.75, filterThreshold=2.5):
    '''
    plaintext (str) : 구분자로 구분 된 글의 문자열 데이터 ex: "글1(구분자)글2(구분자)글3(구분자)글4"

    sep (str) : 구분자 ex = "HOTKEY123!@#"

    returnIndex = False (bool): True 시 결과 데이터로 스팸이 아닌 것으로 판별 된 글들의 인덱스 반환

    returnTopIndex = None (None / int) : 결과 데이터로 스팸이 아닌 것으로 판별 된 글들의 인덱스 중 반환 할 최신 인덱스의 개수

    returnPlain = False (bool) : True 시 결과 데이터로 스팸 필터링 이후 입력받은 plaintext와 동일한 형식으로 데이터 반환

    returnMorph = False (bool) : False 시 전체 리스트 안의 포스트의 리스트들에 토큰들이 있는 형태로 반환
                                 ex : [[글1토큰1, 글1토큰2, 글1토큰3, ... ], 
                                       [글2토큰1, 글2토큰2, ... ], ...]
                                 True 시 토큰의 품사를 같이 반환
                                 ex: [[[글1토큰1, 토큰1품사], [글1토큰2, 토큰2품사], ... ],
                                      [[글2토큰1, 토큰1품사], [글2토큰2, 토큰2품사], ... ], ... ]

    multiReturn = False (bool) : True 시 다수의 결과를 반환
    morphemeAnalyzer = 'kiwi' (str) : 문자열로 형태소 분석기의 이름 입력 시 해당 형태소 분석기의 인스턴스를 내부에서 생성

                                    지원 형태소 분석기 및 호출에 사용 가능한 문자열
                                    kiwipiepy.Kiwi      : 'kiwi','Kiwi','KIWI','키위'
                                    konlpy.tag.Hannanum : 'Hannanum', 'hannanum', 'HANNANUM','한나눔'
                                    konlpy.tag.Komoran  : 'Komoran','KOMORAN','komoran','코모란'
                                    konlpy.tag.Kkma     : 'Kkma','KKMA','kkma','꼬꼬마'
                                    konlpy.tag.Okt      : 'Okt','OKT','okt','오픈코리안텍스트','트위터'
                                    konlpy.tag.Mecab    : 'Mecab','mecab','MECAB','미캐브'

    morphemeAnalyzerParams = None (None / dict) : None

    targetMorphs = ['NNP','NNG'] (list / iterable) : 반환 하는 토큰들의 품사들의 종류를 제한, 기본값 NNP, NNG의 경우 형태소 분석기 기본값인 '고유명사', '일반명사' 형을 반환

    returnEnglishMorph = True (bool) : True 시 해쉬태그, 멘션, 이모티콘, 영어 품사들을 모두 분석해서 반환

    EETagRule = {'NLTK_NNP':'NNP','NLTK_NN':'NNG','R_W_HASHTAG':'W_HASHTAG'} (dict) : "영어 품사로 나올 수 있는 품사" : "해당 품사를 변환할 품사" 쌍의 dict 

    filterMorphemeAnalyzer
    filterMorphemeAnalyzerParams
    filterTargetMorphs
    filterEnglishMorph
    filterEETagRule

    BM25에 사용할 토큰을 구하는 토큰화에 사용되는 동일한 패러미터

    k_1Filter = 1.5 (float) : BM25의 변수, 1.2 이상, 2.0 이하
    bFilter = 0.75 (float) : BM25의 변수 (Christopher D. Manning, Prabhakar Raghavan, Hinrich Schütze. An Introduction to Information Retrieval, Cambridge University Press, 2009, p. 233.)

    filterThreshold = 2.5 (float) : BM25로 산출된 각 문서의 키워드들을 문서별로 평균을 구해서 해당 점수 이하의 문서들을 스팸문서로 간주, 제거

    다른 분석을 수행할 수 있도록 전처리를 수행


    형태소 분석기 인스턴스 생성
    필요시 # (해쉬태그) 삭제
    리스트 안에 문서의 문자열이 담긴 구조를 생성 
    개별 문서들을 돌면서 문서의 길이를 저장 (BM25 사용)
    필터용 토큰 데이터 생성
    BM25 알고리즘으로 필터용 토큰 데이터를 넣어서 문서별로 문서내 키워드별 BM25로 나온 점수의 평균으로 문서 점수 리스트 생성

    단일 데이터 반환
        인덱스 필요시 인덱스 반환
        상위 인덱스 필요시 반환
        원문 반환 필요 시 원문 반환

        토큰화 데이터 필요 시
            반환 데이터에 필요한 데이터가 필터와 동일한 형태소 분석기, 목표 품사 등 동일 조건을 가지면 해당 데이터로 반환
            BM25로 스팸으로 판정 된 데이터 제거 후 토큰화 실시
            데이터 반환

    복수 데이터 반환
    단일 데이터와 동일한 흐름으로 진행되지만 return 대신 딕셔너리에 추가하고 마지막에 딕셔너리를 반환  

    t- 로 시작하는 변수들은 target, 실제로 반환되는 데이터 혹은 그에 사용되는 인스턴스
    f- 로 시작하는 변수들은 filter, 내부적으로 BM25를 통해 필터링을 할 때 사용되는 데이터 혹은 그에 사용되는 인스턴스
    '''

    # 형태소 분석기 인스턴스 생성
    tma = setMorphemeAnalyzer(morphemeAnalyzer, morphemeAnalyzerParams)
    if (morphemeAnalyzer == filterMorphemeAnalyzer and morphemeAnalyzerParams == filterMorphemeAnalyzerParams):
        fma = tma
    else:
        fma = setMorphemeAnalyzer(
            filterMorphemeAnalyzer, filterMorphemeAnalyzerParams)

    tenma = nltkMA(enMorphemeAnalyzerParams)
    if (enMorphemeAnalyzerParams == filterEnMorphemeAnalyzerParams):
        fenma = tenma
    else:
        fenma = nltkMA(filterEnMorphemeAnalyzerParams)

    # 구분자가 마지막에도 붙어있어 data 마지막에 비어있는 포스트가 있을 경우 이를 제거
    data = plain_structurize(plaintext, sep)

    # 해쉬태그를 구성하는 '#'을 제거하고 싶을 경우 이를 제거
    # 구분자에도 '#'이 포함되어 있을 경우 이 또한 제외하여 처리
    if removeHashTag == True:
        newSep = sep.replace('#', '')
        tdata = plain_structurize(plaintext.replace('#', ' '), newSep)

    # 해쉬태그 처리가 없으면 기존의 위의 data 변수를 복제하여 사용
    else:
        tdata = data*1

    # BM25에서 사용하기 위한 원문서들의 길이를 저장
    postLens = list()
    for post in data:
        postLens.append(len(post))

    # BM25 필터링에 사용 될 토큰화 된 결과값을 저장
    ftok = data_tokenize(data, fma, filterTargetMorphs,
                         returnMorph=False, returnEnglishMorph=True, morphemeAnalyzerEN=fenma,
                         eeTagRule=filterEETagRule, kwdMinLen=kwdMinLen)

    flag = False
    # 만약 모든 결과 분석의 조건들이 필터 분석의 조건들과 일치하면 이전의 토큰화 결과를 그대로 사용할 것
    if (removeHashTag == False and
        morphemeAnalyzer == filterMorphemeAnalyzer and
        morphemeAnalyzerParams == filterMorphemeAnalyzerParams and
        targetMorphs == filterTargetMorphs and
        returnMorph == False and
        returnEnglishMorph == filterEnglishMorph and
            EETagRule == filterEETagRule):
        flag = True

    # BM25를 통해 각 토큰들의 점수를 계산하고 문서별로 평균을 낸 결과를 저장
    filterScores = BM25(ftok, postLens, k_1=k_1Filter, b=bFilter)
    # 문서의 개수를 저장
    dataLen = len(postLens)

    # 단일 결과 반환
    if multiReturn == False:
        if returnIndex == True:  # 인덱스들을 반환
            # 최신 인덱스들을 전체 (혹은 지정 개수가 전체보다 커서 전체를) 반환
            if returnTopIndex == None or returnTopIndex >= dataLen:
                idxs = list(range(dataLen))
                spamCount = 0
                for idx, score in enumerate(filterScores):
                    if score < filterThreshold:
                        idxs.remove(idx)
                        spamCount += 1
                print("%s 개의 데이터가 삭제되었습니다." % spamCount)
                return idxs

            else:  # 최신 인덱스들을 지정 개수만큼 반환
                idxs = list()
                idxsCount = 0
                idx = 0
                while idxsCount < returnTopIndex:
                    if filterScores[idx] >= filterThreshold:
                        idxs.append(idx)
                        idxsCount += 1
                    idx += 1
                return idxs

        # 반환 데이터 선택
        elif returnPlain == True:  # 원문을 반환하는 경우
            returnData = data

        elif flag == True:  # 결과 데이터가 필터 데이터와 동일해서 바로 처리가 가능한 경우
            returnData = ftok

        else:  # 새로 작업을 해야 하는 경우
            returnData = tdata

        idx = 0
        spamCount = 0
        while idx < dataLen:
            if filterScores[idx] < filterThreshold:
                spamCount += 1
                returnData.pop(idx)  # 반환 데이터에서 점수 기준에 부합하지 않은 값 제거
                filterScores.pop(idx)  # 점수 기준에 부합하지 않은 값 제거
                idx -= 1
                dataLen -= 1
            idx += 1

        if returnPlain == True:  # 원문 반환
            print("%s 개의 데이터가 삭제되었습니다." % spamCount)
            return sep.join(returnData)

        elif flag == True:  # 필터에서와 동일 데이터 반환
            print("%s 개의 데이터가 삭제되었습니다." % spamCount)
            return returnData

        else:  # 모두 아닐 경우 함수 시작 시 정의한 값들로 형태소 분석 시작 후 결과 반환
            returnData = data_tokenize(returnData, tma, targetMorphs,
                                       returnMorph=returnMorph,
                                       returnEnglishMorph=returnEnglishMorph,
                                       morphemeAnalyzerEN=tenma,
                                       eeTagRule=EETagRule,
                                       kwdMinLen=kwdMinLen)
            print("%s 개의 데이터가 삭제되었습니다." % spamCount)
            return returnData

    else:  # 복수 결과 반환
        returnDatas = dict()  # 데이터를 반환할 딕셔너리

        idxs = list(range(dataLen))
        popIdxs = list()
        spamCount = 0
        for idx, score in enumerate(filterScores):
            if score < filterThreshold:
                idxs.remove(idx)
                popIdxs.append(idx-spamCount)
                spamCount += 1

        if returnIndex == True:  # 필터링 이후 인덱스를 반환할 때
            returnDatas['index'] = idxs
            if returnTopIndex != None:  # 최근 인덱스를 정해진 개수만큼 반환하도록 요청받았을 때
                if returnTopIndex >= dataLen:  # 단 전체 데이터 길이보다 많이 요청되면 전체 길이를 반환
                    returnTopIndex = dataLen
                returnDatas['topIndex'] = idxs[:returnTopIndex]

        if returnPlain == True:  # 원문 반환 요청 시
            for idx in popIdxs:  # 원문이 담긴 data를 기준으로 스팸 인덱스에서
                data.pop(idx)
            # 원래 입력 형태인 구분자로 글들이 구분된 하나의 문자열로 반환
            returnDatas['plain'] = sep.join(data)

        for idx in popIdxs:  # 데이터에서 스팸 인덱스의 데이터를 삭제
            tdata.pop(idx)

        # 형태소 분석 수행
        returnDatas['tokenized'] = data_tokenize(tdata, tma, targetMorphs,
                                                 returnMorph=returnMorph,
                                                 returnEnglishMorph=returnEnglishMorph,
                                                 morphemeAnalyzerEN=tenma,
                                                 eeTagRule=EETagRule,
                                                 kwdMinLen=kwdMinLen)
        print("%s 개의 데이터가 삭제되었습니다." % spamCount)
        return returnDatas


def plain_structurize(plaintext, sep='HOTKEY123!@#', lineSplit=False):
    '''
    구분자로 구분된 문자열을 받아서 구분자를 기준으로 나눠서 리스트에 담아 반환
    만약 구분자로 나눈 리스트의 마지막 데이터가 비어있다면 (구분자로 문자열이 끝나면) 마지막 데이터를 삭제함
    '''
    if lineSplit == False:
        structuredData = plaintext.split(sep)
        if structuredData[-1] == '':
            structuredData = structuredData[:-1]

    else:
        structuredData = list()
        posts = plaintext.split(sep)
        for post in posts:
            structuredData.append(line_split(post))

    return structuredData


def data_tokenize(data, morphemeAnalyzer,
                  targetMorphs=['Noun'],
                  returnMorph=False,
                  returnEnglishMorph=False,
                  morphemeAnalyzerEN=nltkMA(),
                  eeTagRule={'NLTK_NNP': 'Noun', 'NLTK_NN': 'Noun',
                             'R_W_HASHTAG': 'W_HASHTAG', 'R_W_EMJ': 'EMJ'},
                  kwdMinLen=2,
                  lineSplit=False,
                  lineSplitADV=False):
    '''
    데이터를 주어진 형태소 분석기 인스턴스로 분석하고 정해진 품사를 반환
    '''
    returnData = list()

    if lineSplitADV == True:
        for post in data:
            tokenizedData = split_tokenize(
                post, morphemeAnalyzer, morphemeAnalyzerEN)

            postResult = []
            for line in tokenizedData:
                lineResult = []
                for tok in line:
                    text = tok[0]
                    morph = tok[1]
                    if len(text) < kwdMinLen:
                        continue
                    if morph in eeTagRule:
                        morph = eeTagRule[morph]
                    if morph in targetMorphs:
                        if returnMorph == True:
                            lineResult.append([text, morph])
                        else:
                            lineResult.append(text)
                postResult.append(lineResult)
            returnData.append(postResult)
        return returnData

    if lineSplit == True:
        for post in data:
            partialReturnPost = list()
            for line in post:
                partialReturn = list()
                if returnEnglishMorph == True:
                    filteredLine = remove_stopwords(line)
                    if re.fullmatch('[ㄱ-ㅎ가-힣0-9\,\.\/\\\;\'\[\]\`\-\=\<\>\?\:\"\{\}\|\~\!\$\%\^\&\*\(\)\_\+\"\' ]+', filteredLine):
                        tokenizedData = morphemeAnalyzer(filteredLine)
                    else:
                        tokenizedData = HEMEK_tokenize(
                            filteredLine, morphemeAnalyzer, morphemeAnalyzerEN)
                else:
                    tokenizedData = morphemeAnalyzer(filteredLine)

                for tok in tokenizedData:
                    if len(tok[0]) < kwdMinLen:
                        continue
                    # 변환 규칙에 있는 품사는 변환
                    if returnEnglishMorph == True and tok[1] in eeTagRule:
                        tok[1] = eeTagRule[tok[1]]

                    if tok[1] in targetMorphs:
                        # 품사까지 반환하도록 요청 받으면 [키워드, 품사] 쌍을 그대로 반환
                        if returnMorph == True:
                            partialReturn.append(tok)
                        else:  # 품사를 요청받지 않으면 키워드만 뽑아서 반환
                            partialReturn.append(tok[0])
                partialReturnPost.append(partialReturn)
            returnData.append(partialReturnPost)

    else:
        for post in data:
            partialReturn = list()
            if returnEnglishMorph == True:

                filteredPost = remove_stopwords(post)
                if re.fullmatch('[ㄱ-ㅎ가-힣0-9\,\.\/\\\;\'\[\]\`\-\=\<\>\?\:\"\{\}\|\~\!\$\%\^\&\*\(\)\_\+\"\' ]+', filteredPost):
                    tokenizedData = morphemeAnalyzer(filteredPost)
                else:
                    tokenizedData = HEMEK_tokenize(
                        filteredPost, morphemeAnalyzer, morphemeAnalyzerEN)

            else:
                tokenizedData = morphemeAnalyzer(remove_stopwords(post))

            for tok in tokenizedData:
                if len(tok[0]) < kwdMinLen:
                    continue
                # 변환 규칙에 있는 품사는 변환
                if returnEnglishMorph == True and tok[1] in eeTagRule:
                    tok[1] = eeTagRule[tok[1]]

                if tok[1] in targetMorphs:
                    # 품사까지 반환하도록 요청 받으면 [키워드, 품사] 쌍을 그대로 반환
                    if returnMorph == True:
                        partialReturn.append(tok)
                    else:  # 품사를 요청받지 않으면 키워드만 뽑아서 반환
                        partialReturn.append(tok[0])
            returnData.append(partialReturn)

    return returnData


def line_split(text, lineSplitSep='[\.\?\!] |[\\n]|[\n]|[\\\\]n', regexp=True):
    if regexp == True:
        returnData = list()
        chunks = regexp_spliter(text, lineSplitSep, 'split', 'target')
        for chunk in chunks:
            if chunk[1] == 'target':
                returnData.append(chunk[0])
        return returnData

    else:
        return text.split(lineSplitSep)


def remove_stopwords(text, stopwordRule={'\n': ' ', '\u200b': ' ', '\\n': ' '}):
    '''
    입력받은 텍스트를 stopwordRule 에 정의된 불용어:대체 텍스트 쌍대로 불용어를 대체 텍스트로 교체
    '''
    for stopword in stopwordRule:
        text = text.replace(stopword, stopwordRule[stopword])
    return text


def get_demojized_set():
    '''
    emoji 라이브러리로 demojize 결과로 나올 수 있는 모든 :이모티콘 이름: 형식 set 에 담아 반환
    '''
    return set(re.findall("'en': '(:[^:]+:)'", str(emoji.EMOJI_DATA.values())))


def regexp_spliter(text, regexps, matchLabels, nomatchLabel, filters=None):
    '''
    정규표현식들을 이용해 입력받은 텍스트들을 나누고 [나눠진 텍스트, 라벨] 리스트를 담은 리스트로 반환

    ex : ABCDEFG
    입력 받은 정규 표현식 : BC, EF
    입력 받은 라벨 : label1 label2
    입력 받은 불일치 라벨 : NO
    실행 결과 : [[A, NO], [BC, label1], [D, NO], [EF, label2], [G, NO]]

    정규표현식은 모두 re.finditer(정규표현식,입력텍스트) 으로 적용
    '''

    # 만약 입력값이 문자열인 경우 iterable 형식을 갖추기 위해 list에 넣음
    if type(regexps) == str:
        regexps = [regexps]
    if type(matchLabels) == str:
        matchLabels = [matchLabels]
    expCount = len(regexps)

    if filters == None:
        filters = [None]*expCount

    if expCount != len(matchLabels) and expCount != len(filters):
        raise Exception(
            'Regular Expression and Label (and filter) counts are not matched')

    returnData = list()

    foundDict = dict()
    for idx in range(expCount):
        # 텍스트에서 정규 표현식으로 일치하는 부분이 있는지 검색
        for found in re.finditer(regexps[idx], text):
            if filters[idx] == None:  # 필터가 없을 경우 별도의 처리 없이 이어감
                pass
            # 필터 대상에 있는 키워드가 아닐시 다음 키워드로 넘어감
            elif found.group() not in filters[idx]:
                continue
            # 정규 표현에 일치하는 부분의 시작 인덱스를 키로, 값에 종료 인덱스와 라벨을 튜플로 저장
            foundDict[found.start()] = (found.end(), matchLabels[idx])

    starts = list(foundDict.keys())
    starts.sort()
    prevEnd = 0
    for start in starts:
        end = foundDict[start][0]
        label = foundDict[start][1]
        if prevEnd != start:
            returnData.append([text[prevEnd:start], nomatchLabel])
        returnData.append([text[start:end], label])
        prevEnd = end

    if prevEnd != len(text):
        returnData.append([text[prevEnd:], nomatchLabel])

    return returnData


def HEMEK_tokenize(text, KRmorphemeAnalyzer, NKRmorphemeAnalyzer):
    '''
    이모티콘, 해쉬태그, 맨션, 영어, 한글로 나눠서 영어와 한글을 각기 다른 형태소 분석기로 처리하고 그 결과를 반환
    결과는 [[토큰1, 품사1], [토큰2, 품사2], ...] 형식으로 반환
    '''

    chunks = regexp_spliter(
        text, [':[^: ]+:'], ['R_W_EMJ'], 'CHUNK', [get_demojized_set()])

    # Hashtag Emoji Mention chunk
    HEMc = list()
    for chunk in chunks:
        if chunk[1] == 'CHUNK':
            HEMc += regexp_spliter(chunk[0], ['[#][^#@ ]+|#$', '[@][^#@ㄱ-ㅎ가-힣 ]+|@$'], [
                                   'R_W_HASHTAG', 'R_W_MENTION'], 'CHUNK')
        else:
            HEMc.append(chunk)

    '''
    해쉬태그, 맨션 안에는 이모티콘이 들어갈 수 있기 때문에 해쉬태그, 맨션 직후 이모티콘이 나오면 이를 해쉬태그, 맨션에 붙은 것으로 처리
    '''
    cursor = 0
    flag = False
    lenHEMc = len(HEMc)
    while cursor < lenHEMc:  # 인덱스가 아직 전체 길이 안에 있는 동안 while 안을 반복
        # 지금 인덱스에 있는 데이텅의 라벨이 해쉬태그 혹은 맨션일 시
        if HEMc[cursor][1] in ('R_W_HASHTAG', 'R_W_MENTION'):
            if flag == True:  # 이미 이전에 해쉬태그나 맨션이 있어서 이어지는 이모티콘들을 갖고 있으면 이를 하나로 처리
                for merge in range(mergeCount):
                    HEMc[mergePos][0] += HEMc.pop(mergePos+1)[0]
                cursor -= mergeCount
                lenHEMc -= mergeCount

            mergePos = cursor*1
            mergeCount = 0
            flag = True  # flag 변수를 True로 지정

        elif HEMc[cursor][1] == 'R_W_EMJ':  # 만약 이모티콘이 나왔다면
            if flag == True:  # flag 변수가 True 라면 == 앞에서 해쉬태그, 맨션이 나왔고 이전에 이모티콘들만 나온 경우
                mergeCount += 1  # 이것도 이모티콘이니 합칠 대상으로 판정
        else:
            if flag == True:  # 이모티콘, 맨션, 해쉬태그가 아니면 == 하나로 합치면 안 되는 데이터일 경우
                # 앞에서 찾은 이모티콘의 개수만큼 전체 인덱스, 현재 인덱스를 빼고 해쉬태그/맨션에 이모티콘 병합
                for merge in range(mergeCount):
                    HEMc[mergePos][0] += HEMc.pop(mergePos+1)[0]
                cursor -= mergeCount
                lenHEMc -= mergeCount
                flag = False
        cursor += 1

    if flag == True:  # 만약 모든 데이터를 확인했는데 flag가 여전히 True면 == 해쉬태그/맨션이 나오고 계속 이모티콘이 나오다 끝난 경우
        for merge in range(mergeCount):  # 동일한 과정으로 처리한다.
            tok, morph = HEMc.pop(mergePos+1)
            HEMc[mergePos][0] += tok

    # Hashtag Emoji Mention English Korean
    HEMEK = list()
    for chunk in HEMc:
        if chunk[1] == 'CHUNK':
            HEMEK += regexp_spliter(chunk[0],
                                    ['[ㄱ-ㅎ가-힣0-9\,\.\/\\\;\'\[\]\`\-\=\<\>\?\:\"\{\}\|\~\!\@\#\$\%\^\&\*\(\)\_\+\"\' ]+'],
                                    ['KR_CHUNK'], 'NKR_CHUNK')
        else:
            HEMEK.append(chunk)

    result = []
    for chunk in HEMEK:
        text = chunk[0]
        if re.fullmatch('[ ]+||[\n]+', text):  # 비어있는
            continue
        elif chunk[1] == 'KR_CHUNK':  # 한글 덩어리면 한글 형태소 분석기 적용
            for token in KRmorphemeAnalyzer(text):
                result.append([token[0], token[1]])

        elif chunk[1] == 'NKR_CHUNK':  # 한글이 아니면 (주로 영어 예상) 이면 영문 형태소 분석기 적용
            for token in NKRmorphemeAnalyzer(text):
                result.append([token[0], token[1]])
        else:
            result.append(chunk)

    return result


def BM25(data, postLens, k_1=1.5, b=0.75):
    '''
    BM25 알고리즘으로 문서 내의 각 토큰별로 점수를 계산하고 문서별로 문서내에 있는 모든 토큰의 점수의 평균을 리스트에 담아 반환
    '''

    avgPostLen = np.mean(postLens)  # 문서들의 평균 길이

    N = len(data)  # 전체 데이터의 길이 (문서의 개수)

    n = dict()  # 각 문서별로 키워드가 언급된 횟수

    # 전체 문서들을 방문하며 어느 문서에 특정 토큰이 등장했다면 해당 토큰에 1점을 부여
    for post in data:
        uniqueToks = set(post)
        for tok in uniqueToks:
            try:
                n[tok] += 1
            except:
                n[tok] = 1

    IDF = dict()
    for tok in n.keys():
        IDF[tok] = log1p((N-n[tok]+0.5)/(n[tok]+0.5))

    filterScores = list()  # 점수를 저장할 list

    for postidx, post in enumerate(data):
        postScore = 0
        for tok in post:
            tokCount = post.count(tok)
            postScore += (IDF[tok] * (
                (tokCount*(k_1+1))/(
                    tokCount+(k_1*(1-b+(b*(postLens[postidx]/avgPostLen)))))))
        try:
            filterScores.append((postScore/len(post)))
        except:
            filterScores.append(0)

    return filterScores


def spam_filter(plaintext):
    # 1211추가 - seyun
    # db로 부터 말뭉치를 받아서 스팸을 제거하고 다시 플레인텍스트 반환
    status = True
    pt = ''
    try:
        pt = preprocess(plaintext, returnPlain=True)
    except:
        status = False
    return (pt, status)


def HEMKEN_tokenize(text, KRmorphemeAnalyzer, NKRmorphemeAnalyzer):
    '''
    이모티콘, 해쉬태그, 맨션, 영어, 한글로 나눠서 영어와 한글을 각기 다른 형태소 분석기로 처리하고 그 결과를 반환
    결과는 [[토큰1, 품사1], [토큰2, 품사2], ...] 형식으로 반환
    '''

    chunks = regexp_spliter(
        text, '[\.\?\!] |[\\n]|[\n]|[\\\\]n', ['lsc'], 'CHUNK')

    lsChunks = list()
    for chunk in chunks:
        if chunk[1] == 'CHUNK':
            lsChunks += regexp_spliter(chunk[0], [':[^: ]+:'],
                                       ['R_W_EMJ'], 'CHUNK', [get_demojized_set()])
        else:
            lsChunks.append(chunk)

    # Hashtag Emoji Mention chunk
    HEMc = list()
    for chunk in lsChunks:
        if chunk[1] == 'CHUNK':
            HEMc += regexp_spliter(chunk[0], ['[#][^#@ ]+|#$', '[@][^#@ㄱ-ㅎ가-힣 ]+|@$'], [
                                   'R_W_HASHTAG', 'R_W_MENTION'], 'CHUNK')
        else:
            HEMc.append(chunk)

    '''
    해쉬태그, 맨션 안에는 이모티콘이 들어갈 수 있기 때문에 해쉬태그, 맨션 직후 이모티콘이 나오면 이를 해쉬태그, 맨션에 붙은 것으로 처리
    '''
    cursor = 0
    flag = False
    lenHEMc = len(HEMc)
    while cursor < lenHEMc:  # 인덱스가 아직 전체 길이 안에 있는 동안 while 안을 반복
        # 지금 인덱스에 있는 데이텅의 라벨이 해쉬태그 혹은 맨션일 시
        if HEMc[cursor][1] in ('R_W_HASHTAG', 'R_W_MENTION'):
            if flag == True:  # 이미 이전에 해쉬태그나 맨션이 있어서 이어지는 이모티콘들을 갖고 있으면 이를 하나로 처리
                for merge in range(mergeCount):
                    HEMc[mergePos][0] += HEMc.pop(mergePos+1)[0]
                cursor -= mergeCount
                lenHEMc -= mergeCount

            mergePos = cursor*1
            mergeCount = 0
            flag = True  # flag 변수를 True로 지정

        elif HEMc[cursor][1] == 'R_W_EMJ':  # 만약 이모티콘이 나왔다면
            if flag == True:  # flag 변수가 True 라면 == 앞에서 해쉬태그, 맨션이 나왔고 이전에 이모티콘들만 나온 경우
                mergeCount += 1  # 이것도 이모티콘이니 합칠 대상으로 판정
        else:
            if flag == True:  # 이모티콘, 맨션, 해쉬태그가 아니면 == 하나로 합치면 안 되는 데이터일 경우
                # 앞에서 찾은 이모티콘의 개수만큼 전체 인덱스, 현재 인덱스를 빼고 해쉬태그/맨션에 이모티콘 병합
                for merge in range(mergeCount):
                    HEMc[mergePos][0] += HEMc.pop(mergePos+1)[0]
                cursor -= mergeCount
                lenHEMc -= mergeCount
                flag = False
        cursor += 1

    if flag == True:  # 만약 모든 데이터를 확인했는데 flag가 여전히 True면 == 해쉬태그/맨션이 나오고 계속 이모티콘이 나오다 끝난 경우
        for merge in range(mergeCount):  # 동일한 과정으로 처리한다.
            tok, morph = HEMc.pop(mergePos+1)
            HEMc[mergePos][0] += tok

    # Hashtag Emoji Mention English Korean
    HEMEK = list()
    for chunk in HEMc:
        if chunk[1] == 'CHUNK':
            HEMEK += regexp_spliter(chunk[0],
                                    ['[ㄱ-ㅎ가-힣0-9\,\.\/\\\;\'\[\]\`\-\=\<\>\?\:\"\{\}\|\~\!\@\#\$\%\^\&\*\(\)\_\+\"\' ]+'],
                                    ['KR_CHUNK'], 'NKR_CHUNK')
        else:
            HEMEK.append(chunk)

    result = list()
    partialResult = list()
    partialFlag = False
    for chunk in HEMEK:
        text = chunk[0]
        ctype = chunk[1]

        if ctype == 'lsc':
            result.append(partialResult)
            partialResult = list()
            partialFlag = True

        elif re.fullmatch('[ ]+||[\n]+', text):  # 비어있는
            partialFlag = False
            continue
        elif ctype == 'KR_CHUNK':  # 한글 덩어리면 한글 형태소 분석기 적용
            for token in KRmorphemeAnalyzer(text):
                partialResult.append([token[0], token[1]])
            partialFlag = False
        elif ctype == 'NKR_CHUNK':  # 한글이 아니면 (주로 영어 예상) 이면 영문 형태소 분석기 적용
            for token in NKRmorphemeAnalyzer(text):
                partialResult.append([token[0], token[1]])
            partialFlag = False
        else:
            partialResult.append(chunk)
            partialFlag = False

    if partialFlag == False:
        result.append(partialResult)

    return result


def char_type(char):
    cord = ord(char)

    # 한글
    if cord in range(12593, 12643):
        return "KR"
    elif cord in range(44032, 55204):
        return "KR"

    # 숫자
    elif cord in range(48, 58):
        return "NUM"

    # 문장 구성
    elif cord == 32:
        return "blank"
    elif cord == 10:
        return "lineChange"
    elif cord == 92:
        return "backslash"

    # 해쉬태그, 맨션, 이모티콘
    elif cord == 58:
        return "colon"
    elif cord == 35:
        return "sharp"
    elif cord == 64:
        return "at"

    elif cord == 95:
        return "underBar"

    # 해쉬태그, 맨션 가능, 구두점
    elif cord == 46:
        return "punctuation"

    # 해쉬태그, 맨션 불가, 구두점
    elif cord == 63:
        return "question"
    elif cord == 33:
        return "exclamation"

    # 해쉬태그, 맨션 불가
    elif cord == 123:
        return "brace"
    elif cord == 125:
        return "brace"

    else:
        return "NKR"


def split_tokenize(text, ma=setMorphemeAnalyzer('okt'), enma=nltkMA()):
    result = []
    resultLine = []
    textLen = len(text)

    prevType = None
    cursor = 0
    anchor = 0

    special = None
    specialAnchor = None
    specialSubAnchor = None
    specialPrevType = None

    while cursor < textLen:
        char = text[cursor]
        ctype = char_type(char)

        if special == None:  # 이전에 태그,멘션,이모티콘 시작이 없었음
            if ctype in ("colon", "sharp", "at"):  # 태그, 맨션, 이모티콘 시작
                special = ctype  # 타입 저장
                specialAnchor = cursor  # 현재 위치 저장
                specialPrevType = prevType  # 직전 타입 등록
            elif ctype == 'lineChange':  # 줄바꿈 문자
                if prevType == 'KR':
                    resultLine.extend(ma(text[anchor:cursor]))
                else:
                    resultLine.extend(enma(text[anchor:cursor]))
                result.append(resultLine)
                resultLine = []
                cursor += 1
                anchor = cursor
                prevType = None
                continue
            elif ctype == 'backslash':  # 역슬래쉬가 나오면 뒤에 n이 이어서 나오면 줄을 바꿔줌
                try:  # 다음 값을 찾는 과정에서 Out of Index 에러 발생 가능성이 있음 그럴 시 단순 종료
                    if text[cursor+1] == 'n':
                        if prevType == 'KR':
                            resultLine.extend(ma(text[anchor:cursor]))
                        else:
                            resultLine.extend(enma(text[anchor:cursor]))
                        result.append(resultLine)
                        resultLine = []
                        cursor += 2  # 뒤의 줄바꿈 문자와 묶어서 두 칸 전진
                        anchor = cursor
                        prevType = None
                        continue
                except:
                    ctype = prevType
                    cursor += 1
                    pass
                ctype = prevType  # 아닐 시 단순 해프닝으로 처리하고 동일한 타입으로 가정

            elif ctype in ("punctuation", "question", "exclamation"):
                try:  # 다음 값을 찾는 과정에서 Out of Index 에러 발생 가능성이 있음 그럴 시 단순 종료
                    if text[cursor+1] == ' ':  # 구두점 후 다음이 비어있으면 줄바꿈으로 간주한다.
                        if prevType == 'KR':
                            resultLine.extend(ma(text[anchor:cursor]))
                        else:
                            resultLine.extend(enma(text[anchor:cursor]))
                        result.append(resultLine)
                        resultLine = []
                        cursor += 2
                        anchor = cursor
                        prevType = None
                        continue
                    else:
                        ctype = prevType
                        cursor += 1
                        continue
                except:
                    ctype = prevType
                    cursor += 1
                    continue

            else:
                if ctype in ("underBar", "NUM"):  # 언더바, 숫자는 이전과 같은 타입의 데이터 취급
                    ctype = prevType
                    pass

                elif ctype != prevType and ctype != None:  # 그 외에 다른 경우에서 현재 타입이 이전 타입과 다를경우 지금까지의 결과를 형태소 분석
                    if prevType == 'KR':
                        resultLine.extend(ma(text[anchor:cursor]))
                    else:
                        resultLine.extend(enma(text[anchor:cursor]))
                    anchor = cursor
                    prevType = ctype
                    pass

        else:  # 만약 특수 문자로 해쉬태그,맨션,이모티콘 등이 시작되었다면
            if special == "sharp":  # 해쉬태그일 시
                if ctype in ('blank', 'exclamation', 'question', 'brace', 'lineChange', 'backslash'):  # 그냥 종료
                    if prevType == 'KR':
                        if specialSubAnchor == None:
                            resultLine.extend(ma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:cursor], 'W_HASHTAG'])
                        else:
                            resultLine.extend(ma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:specialSubAnchor], 'W_HASHTAG'])
                            resultLine.extend(
                                enma(text[specialSubAnchor:cursor]))
                    elif prevType == 'NKR':
                        if specialSubAnchor == None:
                            resultLine.extend(enma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:cursor], 'W_HASHTAG'])
                        else:
                            resultLine.extend(enma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:specialSubAnchor], 'W_HASHTAG'])
                            resultLine.extend(
                                enma(text[specialSubAnchor:cursor]))
                    else:
                        pass

                    special = None
                    specialAnchor = None
                    specialPrevType = None
                    anchor = cursor
                    prevType = ctype
                    cursor += 1

                    if ctype == 'lineChange':
                        result.append(resultLine)
                        resultLine = []
                        continue

                    elif ctype == 'backslash':
                        try:
                            if text[cursor+1] == 'n':
                                cursor += 1
                                anchor += 1
                                result.append(resultLine)
                                resultLine = []
                                continue
                            else:
                                continue
                        except:
                            continue

                    elif ctype in ('question', 'exclamation'):
                        try:
                            if text[cursor] == ' ':
                                cursor += 1
                                anchor += 1
                                result.append(resultLine)
                                resultLine = []
                                continue
                            else:
                                continue
                        except:
                            continue

                    else:
                        continue

                elif ctype in "KR":  # 한글이 나올 시 specialSubAnchor 가 있다면 이모티콘이 성립하지 않으므로 이모티콘 전까지 처리
                    if specialSubAnchor != None:
                        if specialPrevType == 'KR':
                            resultLine.extend(ma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:specialSubAnchor], 'W_HASHTAG'])
                            resultLine.extend(enma(text[specialAnchor:cursor]))
                        else:
                            resultLine.extend(enma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:specialSubAnchor], 'W_HASHTAG'])
                            resultLine.extend(enma(text[specialAnchor:cursor]))
                        special = None
                        specialAnchor = None
                        specialSubAnchor = None
                        specialPrevType = None
                        anchor = cursor
                        prevType = ctype
                        cursor += 1
                        continue

                elif ctype == 'colon':
                    if specialSubAnchor != None:  # 콜론이 이미 전에 나왔고 문제없이 여기까지 왔다면 해당 콜론구는 이모티콘
                        specialSubAnchor = None
                    else:
                        specialSubAnchor = cursor

                elif ctype in ('at', 'sharp'):  # 이어서 새로운 맨션이 시작되는 경우
                    if specialPrevType == 'KR':
                        if specialSubAnchor == None:
                            resultLine.extend(ma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:cursor], 'W_HASHTAG'])
                        else:
                            resultLine.extend(ma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:specialSubAnchor], 'W_HASHTAG'])
                            resultLine.extend(
                                enma(text[specialSubAnchor:cursor]))
                    else:
                        if specialSubAnchor == None:
                            resultLine.extend(enma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:cursor], 'W_HASHTAG'])
                        else:
                            resultLine.extend(enma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:specialSubAnchor], 'W_HASHTAG'])
                            resultLine.extend(
                                enma(text[specialSubAnchor:cursor]))

                    special = ctype
                    specialAnchor = cursor
                    specialSubAnchor = None
                    specialPrevType = None
                    anchor = cursor
                    prevType = ctype
                    cursor += 1
                    continue

            elif special == "at":  # 맨션일 시 (한글 사용 불가능 / 이모티콘 추가 가능)
                if ctype in ('blank', 'KR', 'exclamation', 'question', 'brace', 'lineChange', 'backslash'):  # 그냥 종료
                    if specialPrevType == 'KR':
                        if specialSubAnchor == None:
                            resultLine.extend(ma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:cursor], 'W_MENTION'])
                        else:
                            resultLine.extend(ma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:specialSubAnchor], 'W_MENTION'])
                            resultLine.extend(
                                enma(text[specialSubAnchor:cursor]))
                    else:
                        if specialSubAnchor == None:
                            resultLine.extend(enma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:cursor], 'W_MENTION'])
                        else:
                            resultLine.extend(enma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:specialSubAnchor], 'W_MENTION'])
                            resultLine.extend(
                                enma(text[specialSubAnchor:cursor]))

                    special = None
                    specialAnchor = None
                    specialPrevType = None
                    anchor = cursor
                    prevType = ctype
                    cursor += 1

                    if ctype == 'lineChange':
                        result.append(resultLine)
                        resultLine = []
                        continue

                    elif ctype == 'backslash':
                        try:
                            if text[cursor] == 'n':
                                cursor += 1
                                anchor += 1
                                result.append(resultLine)
                                resultLine = []
                                continue
                            else:
                                continue
                        except:
                            continue

                    elif ctype in ('question', 'exclamation'):
                        try:
                            if text[cursor] == ' ':
                                cursor += 1
                                anchor += 1
                                result.append(resultLine)
                                resultLine = []
                                continue
                            else:
                                continue
                        except:
                            continue

                    else:
                        continue

                if ctype == 'colon':  # 해쉬태그에는 이모티콘이 들어갈 수 있음
                    if specialSubAnchor != None:
                        specialSubAnchor = None
                    else:
                        specialSubAnchor = cursor

                if ctype in ('sharp', 'at'):
                    if prevType == 'KR':
                        if specialSubAnchor == None:
                            resultLine.extend(ma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:cursor], 'W_MENTION'])
                        else:
                            resultLine.extend(ma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:specialSubAnchor], 'W_MENTION'])
                            resultLine.extend(
                                enma(text[specialSubAnchor:cursor]))
                    else:
                        if specialSubAnchor == None:
                            resultLine.extend(enma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:cursor], 'W_MENTION'])
                        else:
                            resultLine.extend(enma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:specialSubAnchor], 'W_MENTION'])
                            resultLine.extend(
                                enma(text[specialSubAnchor:cursor]))

                    cursor += 1
                    anchor = cursor
                    special = ctype
                    specialAnchor = cursor
                    specialPrevType = None
                    specialSubAnchor = None
                    prevType = ctype
                    continue

            elif special == 'colon':  # 이모티콘 관련해서 보고 있을 때
                if ctype == 'colon':
                    if prevType == 'colon':  # 이전도 콜론인데 지금도 콜론이면 앞의 콜론은 무시
                        special = ctype
                        specialAnchor = cursor
                        pass
                    else:  # 이전에 콜론이 나왔지만 직전값은 콜론이 아닌채로 통과한 경우
                        if specialPrevType == 'KR':
                            resultLine.extend(ma(text[anchor:specialAnchor]))
                            # 이모티콘은 자기자신을 포함
                            resultLine.append(
                                [text[specialAnchor:cursor+1], 'EMJ'])
                        else:
                            resultLine.extend(enma(text[anchor:specialAnchor]))
                            resultLine.append(
                                [text[specialAnchor:cursor+1], 'EMJ'])

                    cursor += 1  # 이모티콘은 자기자신 콜론까지 포함
                    anchor = cursor
                    special = None
                    specialPrevType = None
                    specialSubAnchor = None
                    prevType = ctype
                    continue

                elif ctype in ('sharp', 'at'):  # 이전에 콜론이 있었는데 지금 샵이나 엣이 나온다면 이전 콜론은 의미없는 콜론
                    special = ctype
                    if specialPrevType == 'KR':
                        resultLine.extend(ma(text[anchor:specialAnchor]))
                        resultLine.extend(enma(text[specialAnchor:cursor]))
                    else:
                        resultLine.extend(enma(text[anchor:cursor]))

                    anchor = cursor
                    specialAnchor = cursor
                    specialPrevType = None
                    specialSubAnchor = None
                    prevType = ctype
                    cursor += 1
                    continue

                elif ctype in ('blank', 'KR', 'exclamation', 'question', 'brace', 'lineChange', 'backslash'):
                    if specialPrevType == 'KR':
                        resultLine.extend(ma(text[anchor:specialAnchor]))
                        resultLine.extend(enma(text[specialAnchor:cursor]))
                    else:
                        resultLine.extend(enma(text[anchor:cursor]))

                    anchor = cursor
                    special = None
                    specialAnchor = cursor
                    specialPrevType = None
                    specialSubAnchor = None
                    prevType = ctype
                    cursor += 1
                    if ctype == 'backslash':
                        try:
                            if text[cursor] == 'n':
                                cursor += 1
                                anchor += 1
                                result.append(resultLine)
                                resultLine = []
                                continue
                            else:
                                continue
                        except:
                            continue

                    elif ctype in ('question', 'exclamation'):
                        try:
                            if text[cursor] == ' ':
                                cursor += 1
                                anchor += 1
                                result.append(resultLine)
                                resultLine = []
                                continue
                            else:
                                continue
                        except:
                            continue
                    continue

        cursor += 1
        prevType = ctype

    # 다 끝나고 마지막으로 추가
    if special != None:
        if specialSubAnchor != None:
            if specialPrevType == 'KR':
                if special in ('sharp', 'at'):
                    resultLine.extend(ma(text[anchor:specialAnchor]))
                    if special == 'sharp':
                        resultLine.append(
                            [text[specialAnchor:specialSubAnchor], 'W_HASHTAG'])
                        resultLine.extend(enma(text[specialSubAnchor:]))
                    else:
                        resultLine.append([text[specialAnchor:], 'W_MENTION'])
                        resultLine.extend(enma(text[specialSubAnchor:]))
                else:
                    resultLine.extend(enma(text[anchor:]))
            else:
                if special in ('sharp', 'at'):
                    resultLine.extend(enma(text[anchor:specialAnchor]))
                    if special == 'sharp':
                        resultLine.append([text[specialAnchor:], 'W_HASHTAG'])
                    else:
                        resultLine.append([text[specialAnchor:], 'W_MENTION'])
                else:
                    resultLine.extend(enma(text[anchor:]))

        else:
            if specialPrevType == 'KR':
                if special in ('sharp', 'at'):
                    resultLine.extend(ma(text[anchor:specialAnchor]))
                    if special == 'sharp':
                        resultLine.append([text[specialAnchor:], 'W_HASHTAG'])
                    else:
                        resultLine.append([text[specialAnchor:], 'W_MENTION'])
                else:
                    resultLine.extend(ma(text[anchor:specialAnchor]))
                    resultLine.extend(enma(text[specialAnchor:]))
            else:
                if special in ('sharp', 'at'):
                    resultLine.extend(enma(text[anchor:specialAnchor]))
                    if special == 'sharp':
                        resultLine.append([text[specialAnchor:], 'W_HASHTAG'])
                    else:
                        resultLine.append([text[specialAnchor:], 'W_MENTION'])
                else:
                    resultLine.extend(enma(text[anchor:]))

    elif anchor != textLen:
        if prevType == 'KR':
            resultLine.extend(ma(text[anchor:cursor]))
        else:
            resultLine.extend(enma(text[anchor:cursor]))
    if resultLine != []:
        result.append(resultLine)

    return result
