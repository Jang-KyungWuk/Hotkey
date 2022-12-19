# !/usr/bin/env python
# coding: utf-8


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
    def __init__(self,
                 morph_header='NLTK_',
                 word_tokenize_language='english',
                 word_tokenize_preserve_line=False,
                 pos_tag_tagset=None,
                 pos_tag_lang='eng'):
        """
        create instance and set parameters
        """
    
        # nltk로 형태소 분석에 사용되는 패러미터들을 할당
        self.morph_header = morph_header
        self.word_tokenize_language = word_tokenize_language
        self.word_tokenize_preserve_line = word_tokenize_preserve_line
        self.pos_tag_tagset = pos_tag_tagset
        self.pos_tag_lang = pos_tag_lang
        
    def __call__(self,text):
        """
        nltk.pos_tag(nltk.word_tokenize(text input))
        """
        result = list()
        for token in nltk.pos_tag(nltk.word_tokenize(text,
                                                     language=self.word_tokenize_language,
                                                     preserve_line=self.word_tokenize_preserve_line),
                                  tagset=self.pos_tag_tagset,
                                  lang=self.pos_tag_lang):
            result.append([token[0],self.morph_header+token[1]])
        return result


class setMorphemeAnalyzer:
    def __init__(self, maText,maParamDict=None):
        
        '''
        maText 를 토대로 형태소 분석기의 종류를 구분
        maParamDict에 해당 형태소 분석기의 패러미터로 넣을 수 있는 값이 있으면 해당 값을, 없으면 기본값을 설정
        형태소 분석기의 tokenize (키위) / pos (KoNLPy 계열) 함수에 __call__을 통해 입력받을 수 있는 형태의 인스턴스를 반환
        '''
        if maText in ['kiwi','Kiwi','KIWI','키위']:
            if maParamDict==None:
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

                self.ma = Kiwi(num_workers=num_workers,model_path=model_path,
                               options=options,integrate_allomorph=integrate_allomorph,
                               load_default_dict=load_default_dict,load_typo_dict=load_typo_dict,
                               model_type=model_type, typos=typos, typo_cost_threshold=typo_cost_threshold).tokenize

        elif maText in ['Hannanum', 'hannanum', 'HANNANUM','한나눔']:
            if maParamDict==None:
                self.ma = konlpy.tag.Hannanum().pos
            else:
                if 'jvmpath' in maParamDict:
                    jvmpath = maParamDict['jvmpath']
                else:
                    jvmpath=None

                if 'max_heap_size' in maParamDict:
                    max_heap_size = maParamDict['max_heap_size']
                else:
                    max_heap_size=1024

                self.ma = konlpy.tag.Hannanum(jvmpath=jvmpath, max_heap_size=max_heap_size).pos

        elif maText in ['Komoran','KOMORAN','komoran','코모란']:
            if maParamDict == None:
                self.ma = konlpy.tag.Komoran().pos
            else:
                if 'jvmpath' in maParamDict:
                    jvmpath = maParamDict['jvmpath']
                else:
                    jvmpath=None

                if 'userdic' in maParamDict:
                    userdic = maParamDict['userdic']
                else:
                    userdic=None

                if 'modelpath' in maParamDict:
                    modelpath = maParamDict['modelpath']
                else:
                    modelpath=None

                if 'max_heap_size' in maParamDict:
                    max_heap_size = maParamDict['max_heap_size']
                else:
                    max_heap_size=1024

                self.ma = konlpy.tag.Komoran(jvmpath=jvmpath, userdic=userdic,
                                             modelpath=modelpath, max_heap_size=max_heap_size).pos

        elif maText in ['Kkma','KKMA','kkma','꼬꼬마']:
            if maParamDict == None:
                self.ma = konlpy.tag.Kkma().pos
            else:
                if 'jvmpath' in maParamDict:
                    jvmpath = maParamDict['jvmpath']
                else:
                    jvmpath=None

                if 'max_heap_size' in maParamDict:
                    max_heap_size = maParamDict['max_heap_size']
                else:
                    max_heap_size=1024

                self.ma = konlpy.tag.Kkma(jvmpath=jvmpath, max_heap_size=max_heap_size).pos


        elif maText in ['Okt','OKT','okt','오픈코리안텍스트','트위터']:
            if maParamDict == None:
                self.ma = konlpy.tag.Okt().pos
            else:
                if 'jvmpath' in maParamDict:
                    jvmpath = maParamDict['jvmpath']
                else:
                    jvmpath=None

                if 'max_heap_size' in maParamDict:
                    max_heap_size = maParamDict['max_heap_size']
                else:
                    max_heap_size=1024

                self.ma = konlpy.tag.Okt(jvmpath=jvmpath, max_heap_size=max_heap_size).pos

        elif maText in ['Mecab','mecab','MECAB','미캐브']:
            if maParamDict == None:
                self.ma = konlpy.tag.Mecab().pos
            else:
                if 'dicpath' in maParamDict:
                    dicpath = maParamDict['dicpath']
                else:
                    dicpath='/usr/local/lib/mecab/dic/mecab-ko-dic'

                self.ma = konlpy.tag.Mecab(dicpath=dicpath).pos

        else:
            raise Exception('No such morpheme analyzer\nSupported morpheme analyzers are Kiwi, KoNLPy(Hannanum, Komoran, Kkma, Okt, Mecab)')

    def __call__(self,text):
        
        '''
        기존의 (토큰,품사) 튜플들을 담은 리스트를 반환하는 구조 대신 [토큰, 품사] 리스트를 담은 리스트를 반환
        '''
        result = list()
        for token in self.ma(text):
            result.append([token[0],token[1]])
        return result


def preprocess(plaintext, sep='HOTKEY123!@#',
               returnIndex=False, returnTopIndex=None, 
               returnPlain=False, returnMorph=False,
               multiReturn = False,
               removeHashTag=True,
               morphemeAnalyzer='kiwi',morphemeAnalyzerParams=None, targetMorphs=['NNP','NNG'],
               returnEnglishMorph=True, EETagRule={'NLTK_NNP':'NNP','NLTK_NN':'NNG','R_W_HASHTAG':'W_HASHTAG'},
               filterMorphemeAnalyzer='kiwi', filterMorphemeAnalyzerParams=None, filterTargetMorphs=['NNP','NNG','W_HASHTAG'],
               filterEnglishMorph=True, filterEETagRule={'NLTK_NNP':'NNP','NLTK_NN':'NNG','R_W_HASHTAG':'W_HASHTAG'},
               k_1Filter=1.5 ,bFilter=0.75,filterThreshold = 2.5):
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
    fma = setMorphemeAnalyzer(filterMorphemeAnalyzer, filterMorphemeAnalyzerParams)
    
    # 구분자가 마지막에도 붙어있어 data 마지막에 비어있는 포스트가 있을 경우 이를 제거
    data = plain_structurize(plaintext,sep)
    
    # 해쉬태그를 구성하는 '#'을 제거하고 싶을 경우 이를 제거
    # 구분자에도 '#'이 포함되어 있을 경우 이 또한 제외하여 처리
    if removeHashTag == True:
        newSep = sep.replace('#','')
        tdata = plain_structurize(plaintext.replace('#',' '),newSep)

            
    # 해쉬태그 처리가 없으면 기존의 위의 data 변수를 복제하여 사용
    else:
        tdata = data*1
    
    # BM25에서 사용하기 위한 원문서들의 길이를 저장
    postLens = list()
    for post in data:
        postLens.append(len(post))
        
    
    # BM25 필터링에 사용 될 토큰화 된 결과값을 저장
    ftok = data_tokenize(data,fma,filterTargetMorphs,
                         returnMorph=False,returnEnglishMorph=True,eeTagRule=filterEETagRule)
    
    flag=False
    # 만약 모든 결과 분석의 조건들이 필터 분석의 조건들과 일치하면 이전의 토큰화 결과를 그대로 사용할 것
    if (removeHashTag==False and\
        morphemeAnalyzer==filterMorphemeAnalyzer and\
        morphemeAnalyzerParams==filterMorphemeAnalyzerParams and\
        targetMorphs==filterTargetMorphs and\
        returnMorph==False and\
        returnEnglishMorph==filterEnglishMorph and\
        EETagRule==filterEETagRule):
        flag=True
    
    
    # BM25를 통해 각 토큰들의 점수를 계산하고 문서별로 평균을 낸 결과를 저장
    filterScores = BM25(ftok, postLens, k_1=k_1Filter, b=bFilter)
    # 문서의 개수를 저장
    dataLen = len(postLens)
    
    # 단일 결과 반환
    if multiReturn == False:
        if returnIndex == True: # 인덱스들을 반환
            if returnTopIndex == None or returnTopIndex >= dataLen: # 최신 인덱스들을 전체 (혹은 지정 개수가 전체보다 커서 전체를) 반환
                idxs = list(range(dataLen))
                spamCount = 0
                for idx, score in enumerate(filterScores):
                    if score < filterThreshold:
                        idxs.remove(idx)
                        spamCount+=1
                print("%s 개의 데이터가 삭제되었습니다."%spamCount)
                return idxs
                
            else: # 최신 인덱스들을 지정 개수만큼 반환
                idxs = list()
                idxsCount = 0
                idx = 0
                while idxsCount < returnTopIndex:
                    if filterScores[idx] >= filterThreshold:
                        idxs.append(idx)
                        idxsCount+=1
                    idx+=1
                return idxs
        
        # 반환 데이터 선택
        elif returnPlain==True: # 원문을 반환하는 경우
            returnData = data
                    
        elif flag==True: # 결과 데이터가 필터 데이터와 동일해서 바로 처리가 가능한 경우
            returnData = ftok
        
        else: # 새로 작업을 해야 하는 경우
            returnData = tdata
        
        idx=0
        spamCount = 0
        while idx<dataLen:
            if filterScores[idx] < filterThreshold:
                spamCount+=1
                returnData.pop(idx) # 반환 데이터에서 점수 기준에 부합하지 않은 값 제거
                filterScores.pop(idx) # 점수 기준에 부합하지 않은 값 제거
                idx-=1
                dataLen-=1
            idx+=1
        
        if returnPlain==True: # 원문 반환
            print("%s 개의 데이터가 삭제되었습니다."%spamCount)
            return sep.join(returnData)
        
        elif flag==True: # 필터에서와 동일 데이터 반환
            print("%s 개의 데이터가 삭제되었습니다."%spamCount)
            return returnData
        
        else: # 모두 아닐 경우 함수 시작 시 정의한 값들로 형태소 분석 시작 후 결과 반환
            returnData = data_tokenize(returnData, tma, targetMorphs,
                                       returnMorph= returnMorph,
                                       returnEnglishMorph=returnEnglishMorph,
                                       eeTagRule=EETagRule)
            print("%s 개의 데이터가 삭제되었습니다."%spamCount)
            return returnData


        
    else: # 복수 결과 반환
        returnDatas = dict() # 데이터를 반환할 딕셔너리
        
        idxs = list(range(dataLen))
        popIdxs = list()
        spamCount = 0
        for idx, score in enumerate(filterScores):
            if score < filterThreshold:
                idxs.remove(idx)
                popIdxs.append(idx-spamCount)
                spamCount+=1
        
        if returnIndex == True: # 필터링 이후 인덱스를 반환할 때
            returnDatas['index'] = idxs
            if returnTopIndex!=None: # 최근 인덱스를 정해진 개수만큼 반환하도록 요청받았을 때
                if returnTopIndex >= dataLen: # 단 전체 데이터 길이보다 많이 요청되면 전체 길이를 반환
                    returnTopIndex=dataLen 
                returnDatas['topIndex'] = idxs[:returnTopIndex]
                
        if returnPlain==True: # 원문 반환 요청 시
            for idx in popIdxs: # 원문이 담긴 data를 기준으로 스팸 인덱스에서 
                data.pop(idx)
            returnDatas['plain']=sep.join(data) # 원래 입력 형태인 구분자로 글들이 구분된 하나의 문자열로 반환
            
        for idx in popIdxs: # 데이터에서 스팸 인덱스의 데이터를 삭제 
            tdata.pop(idx)
            
        # 형태소 분석 수행    
        returnDatas['tokenized'] = data_tokenize(tdata, tma, targetMorphs,
                                                 returnMorph = returnMorph,
                                                 returnEnglishMorph = returnEnglishMorph,
                                                 eeTagRule = EETagRule) 
        print("%s 개의 데이터가 삭제되었습니다."%spamCount)
        return returnDatas


def plain_structurize(plaintext, sep='HOTKEY123!@#'):
    structuredData = plaintext.split(sep)
    if structuredData[-1] == '':
        structuredData=structuredData[:-1]
    return structuredData



def data_tokenize(data,morphemeAnalyzer,
                  targetMorphs=['NNP','NNG'],
                  returnMorph=False,
                  returnEnglishMorph=False,
                  eeTagRule={'NLTK_NNP':'NNP',
                             'NLTK_NN':'NNG',
                             'R_W_HASHTAG':'W_HASHTAG'}):
    '''
    데이터를 주어진 형태소 분석기 인스턴스로 분석하고 정해진 품사를 반환
    '''
    returnData = list()
    
    if returnEnglishMorph == True:
        for post in data:
            partialReturn = list()
            tokenizedData=HEMEK_tokenize(remove_stopwords(post),morphemeAnalyzer,nltkMA())
            
            for tok in tokenizedData:
                if tok[1] in eeTagRule:
                    tok[1] = eeTagRule[tok[1]]
                if tok[1] in targetMorphs:
                    if returnMorph == True:
                        partialReturn.append(tok)
                    else:
                        partialReturn.append(tok[0])
            returnData.append(partialReturn)
     
    else:
        for post in data:
            partialReturn=list()
            tokenizedData = morphemeAnalyzer(remove_stopwords(post))
            for tok in tokenizedData:
                if tok[1] in targetMorphs:
                    if returnMorph == True:
                        partialReturn.append(tok)
                    else:
                        partialReturn.append(tok[0])
            returnData.append(partialReturn)
    
    return returnData



def remove_stopwords(text, stopwordRule={'\n':' ','\u200b':' ','\\n':' '}):
    
    '''
    입력받은 텍스트를 stopwordRule 에 정의된 불용어:대체 텍스트 쌍대로 불용어를 대체 텍스트로 교체
    '''
    for stopword in stopwordRule:
        text = text.replace(stopword,stopwordRule[stopword])
    return text


def get_demojized_set():
    
    '''
    emoji 라이브러리로 demojize 결과로 나올 수 있는 모든 :이모티콘 이름: 형식 set 에 담아 반환
    '''
    return set(re.findall("'en': '(:[^:]+:)'",str(emoji.EMOJI_DATA.values())))



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
    if type(regexps) == str:
        regexps = [regexps]
    if type(matchLabels) == str:
        matchLabels = [matchLabels]
    expCount = len(regexps)
    
    if filters == None:
        filters = [None]*expCount

    if expCount != len(matchLabels) and expCount != len(filters):
        raise Exception('Regular Expression and Label (and filter) counts are not matched')
    
    
    returnData = list()
    
    foundDict=dict()
    for idx in range(expCount):
        for found in re.finditer(regexps[idx],text):
            if filters[idx] == None:
                pass
            elif found.group() not in filters[idx]:
                continue
            
            foundDict[found.start()] = (found.end(),matchLabels[idx])
    
    starts = list(foundDict.keys())
    starts.sort()
    prevEnd = 0
    for start in starts:
        end = foundDict[start][0]
        label = foundDict[start][1]     
        if prevEnd!=start:
            returnData.append([text[prevEnd:start],nomatchLabel])
        returnData.append([text[start:end],label])
        prevEnd = end
        
    if prevEnd != len(text):
        returnData.append([text[prevEnd:],nomatchLabel])
    
    return returnData


def HEMEK_tokenize(text,KRmorphemeAnalyzer,NKRmorphemeAnalyzer):
    
    '''
    이모티콘, 해쉬태그, 맨션, 영어, 한글로 나눠서 영어와 한글을 각기 다른 형태소 분석기로 처리하고 그 결과를 반환
    결과는 [[토큰1, 품사1], [토큰2, 품사2], ...] 형식으로 반환
    '''
    
    chunks = regexp_spliter(text,[':[^: ]+:'],['R_W_EMJ'],'CHUNK',[get_demojized_set()])
    
    # Hashtag Emoji Mention chunk
    HEMc = list()
    for chunk in chunks:
        if chunk[1] == 'CHUNK':
            HEMc+=regexp_spliter(chunk[0],['[#][^#@ ]+|#$','[@][^#@ㄱ-ㅎ가-힣 ]+|@$'],['R_W_HASHTAG','R_W_MENTION'],'CHUNK')
        else:
            HEMc.append(chunk)
            
    '''
    해쉬태그, 맨션 안에는 이모티콘이 들어갈 수 있기 때문에 해쉬태그, 맨션 직후 이모티콘이 나오면 이를 해쉬태그, 맨션에 붙은 것으로 처리
    '''
    cursor = 0
    flag = False
    lenHEMc = len(HEMc)
    while cursor < lenHEMc: # 인덱스가 아직 전체 길이 안에 있는 동안 while 안을 반복
        if HEMc[cursor][1] in ('R_W_HASHTAG','R_W_MENTION'): # 지금 인덱스에 있는 데이텅의 라벨이 해쉬태그 혹은 맨션일 시
            if flag==True: # 이미 이전에 해쉬태그나 맨션이 있어서 이어지는 이모티콘들을 갖고 있으면 이를 하나로 처리
                for merge in range(mergeCount):
                    HEMc[mergePos][0] += HEMc.pop(mergePos+1)[0]
                cursor-=mergeCount
                lenHEMc-=mergeCount

            mergePos = cursor*1
            mergeCount = 0
            flag=True # flag 변수를 True로 지정

        elif HEMc[cursor][1] == 'R_W_EMJ': # 만약 이모티콘이 나왔다면
            if flag==True: # flag 변수가 True 라면 == 앞에서 해쉬태그, 맨션이 나왔고 이전에 이모티콘들만 나온 경우
                mergeCount+=1 # 이것도 이모티콘이니 합칠 대상으로 판정
        else:
            if flag==True: # 이모티콘, 맨션, 해쉬태그가 아니면 == 하나로 합치면 안 되는 데이터일 경우
                # 앞에서 찾은 이모티콘의 개수만큼 전체 인덱스, 현재 인덱스를 빼고 해쉬태그/맨션에 이모티콘 병합
                for merge in range(mergeCount):
                    HEMc[mergePos][0] += HEMc.pop(mergePos+1)[0]
                cursor-=mergeCount
                lenHEMc-=mergeCount
                flag=False
        cursor+=1

    if flag==True: # 만약 모든 데이터를 확인했는데 flag가 여전히 True면 == 해쉬태그/맨션이 나오고 계속 이모티콘이 나오다 끝난 경우
        for merge in range(mergeCount): # 동일한 과정으로 처리한다.
            tok, morph = HEMc.pop(mergePos+1)
            HEMc[mergePos][0] += tok
        

    # Hashtag Emoji Mention English Korean
    HEMEK = list()
    for chunk in HEMc:
        if chunk[1] == 'CHUNK':
            HEMEK+=regexp_spliter(chunk[0],
                                  ['[ㄱ-ㅎ가-힣0-9\,\.\/\\\;\'\[\]\`\-\=\<\>\?\:\"\{\}\|\~\!\@\#\$\%\^\&\*\(\)\_\+\"\' ]+'],
                                  ['KR_CHUNK'],'NKR_CHUNK')
        else:
            HEMEK.append(chunk)
    
    result = []
    for chunk in HEMEK:
        text = chunk[0]
        if re.fullmatch('[ ]+||[\n]+',text):
            continue
        elif chunk[1] == 'KR_CHUNK':
            for token in KRmorphemeAnalyzer(text):
                result.append([token[0],token[1]])
            
        elif chunk[1] == 'NKR_CHUNK':
            for token in NKRmorphemeAnalyzer(text):
                result.append([token[0],token[1]])
        else:
            result.append(chunk)
        
    return result


def BM25(data, postLens, k_1=1.5, b=0.75):
    avgPostLen = np.mean(postLens)
    
    '''
    BM25 알고리즘으로 문서 내의 각 토큰별로 점수를 계산하고 문서별로 문서내에 있는 모든 토큰의 점수의 평균을 리스트에 담아 반환
    '''
    
    N = len(data) # 전체 데이터의 길이 (문서의 개수)
    
    n = dict()
    
    # 전체 문서들을 방문하며 어느 문서에 특정 토큰이 등장했다면 해당 토큰에 1점을 부여
    for post in data:
        uniqueToks = set(post)
        for tok in uniqueToks:
            try:
                n[tok]+=1
            except:
                n[tok] = 1
    
    IDF = dict()
    for tok in n.keys():
        IDF[tok] = log1p((N-n[tok]+0.5)/(n[tok]+0.5))


    filterScores = list()

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

