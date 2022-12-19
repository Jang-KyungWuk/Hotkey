import preprocess as pp
import networkx as nx
import pyvis as pyv
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt


def network(plaintext,ldaResult, sep='HOTKEY123!@#',
            maxEdge=150, saveDir='./templates/',saveFilename='network',
            returnEnglishMorph=True,
            targetMorphs=['Noun'],
            morphWeight={'Noun':1},skipList=['\n'],
            minlength=2,
            titleKwdCount=5,
            topicColors=['#EFC168','#EFED8C','#AEE155','#B280E9','#35DDD1'],
            heightPX = "1000px",
            bgColor="#000000",
            fontColor="#FFFFFF",
            morphemeAnalyzer = "Okt",topicWeight=5,lineSplit=True):

    try:

        sdata = pp.plain_structurize(plaintext=plaintext, sep=sep)
        
        ma = pp.setMorphemeAnalyzer(morphemeAnalyzer)
        enma = pp.nltkMA()
        

        if lineSplit == True:
            data = pp.data_tokenize(data=sdata,
                                    morphemeAnalyzer=ma,
                                    returnEnglishMorph=returnEnglishMorph,
                                    morphemeAnalyzerEN=enma,
                                    returnMorph=True,
                                    targetMorphs=targetMorphs,
                                    lineSplitADV=lineSplit)
        else:
            data = pp.data_tokenize(data=sdata,
                                morphemeAnalyzer=ma,
                                returnEnglishMorph=returnEnglishMorph,
                                morphemeAnalyzerEN=enma,
                                returnMorph=True,
                                targetMorphs=targetMorphs,
                                lineSplit=lineSplit)


        topicTitles , kwd2topic = kwd_topic_pairing(ldaResult, titleKwdCount=titleKwdCount)

        kwdData, kwd2Morph = kwd_morph_pairing(data, lineSplit=lineSplit)


        kwdPair = kwd_paring(kwdData,kwd2topic,kwd2Morph,
                             skipList=skipList,
                             morphWeight=morphWeight,
                             minlength=minlength,topicWeight=topicWeight,
                             lineSplit=lineSplit)

        topPair = get_top_pair(kwdPair, maxEdge=maxEdge)
        
        nxG = darw_networkx_network(topPair, kwd2Morph, kwd2topic, topicTitles, topicColors= topicColors)
        
        pyvis_network_html(nxG,
                           saveDir=saveDir, saveName=saveFilename,
                           heightPX = heightPX,
                           bgColor=bgColor,
                           fontColor=fontColor)
        

        return True
    except:
        return False


def kwd_topic_pairing(topics, titleKwdCount=5):
    '''
    토픽 순위를 기반으로 키워드가 어느 토픽에 가까운지 반환하는 dict을 만듦
    '''
    topicCount = len(topics)
    topicTitles = dict()
    
    maxlen = 0
    for topicNum, topic in enumerate(topics):
        topicLen = len(topic)
        if topicLen>maxlen:
            maxlen = topicLen
        topicTitles[topicNum+1] = "_".join([topic[idx] for idx in range(titleKwdCount)])
    
    kwd2topic = dict()
    for rank in range(maxlen):
        for topicIdx in range(topicCount):
            try:
                kwd = topics[topicIdx][rank]
            except:
                continue

            if kwd not in kwd2topic:
                kwd2topic[kwd] = topicIdx+1

                
    return topicTitles , kwd2topic


def kwd_morph_pairing(data, lineSplit=False):
    '''
    키워드를 입력하면 해당 키워드의 품사를 반환할 수 있도록 dict을 만듦
    '''
    kwdMorphDist = dict()
    returnData = list()
    
    if lineSplit==True:
        for post in data:
            partialResultPost = list()
            for line in post:
                partialResult = list()
                for tok in line:
                    kwd = tok[0]
                    morph = tok[1]
                    try:
                        kwdMorphDist[kwd][morph]+=1
                    except:
                        try:
                            kwdMorphDist[kwd][morph]=1
                        except:
                            kwdMorphDist[kwd] = dict()
                            kwdMorphDist[kwd][morph]=1
                    partialResult.append(kwd)
                partialResultPost.append(partialResult)
            returnData.append(partialResultPost)
                    
    else:
        for post in data:
            partialResult = list()
            for tok in post:
                kwd = tok[0]
                morph = tok[1]
                try:
                    kwdMorphDist[kwd][morph]+=1
                except:
                    try:
                        kwdMorphDist[kwd][morph]=1
                    except:
                        kwdMorphDist[kwd] = dict()
                        kwdMorphDist[kwd][morph]=1
                partialResult.append(kwd)
            returnData.append(partialResult)

    kwd2Morph = dict()
    for kwd in kwdMorphDist:
        morphs = list(kwdMorphDist[kwd].keys())
        counts = list(kwdMorphDist[kwd].values())

        kwd2Morph[kwd] = morphs[counts.index(max(counts))]
        
    return returnData, kwd2Morph



def kwd_paring(data, kwd2topic, kwd2Morph, skipList=['\n'], morphWeight={'NNG':1,'NNP':10,'emj':0}, minlength=2,topicWeight=5,lineSplit=False):
    
    kwdPair = dict()
    
    if lineSplit==True:
        for post in data:
            for line in post:
                if len(line) < minlength:
                    continue
                
                uniqueKwds = list(set(line))
                uklen = len(uniqueKwds)
                
                for idx1 in range(0,uklen-1):
                    for idx2 in range(1, uklen):
                        kwd1 = uniqueKwds[idx1]
                        kwd2 = uniqueKwds[idx2]
                        if kwd1 == kwd2:
                            continue

                        weight = morphWeight[kwd2Morph[kwd1]]*morphWeight[kwd2Morph[kwd2]]
                        try:
                            if kwd2topic[kwd1] == kwd2topic[kwd2]:
                                weight+=topicWeight
                        except:
                            pass

                        pair = "%s<*>%s"%(kwd1,kwd2)
                        possible = "%s<*>%s"%(kwd2,kwd1)

                        if possible in kwdPair:
                            kwdPair[possible]+=weight
                        else:
                            try:
                                kwdPair[pair]+=weight
                            except:
                                kwdPair[pair]=weight
        
    else:
        for post in data:
            if len(post) < minlength:
                continue

            uniqueKwds = list(set(post))
            uklen = len(uniqueKwds)

            for idx1 in range(0,uklen-1):
                for idx2 in range(1, uklen):
                    kwd1 = uniqueKwds[idx1]
                    kwd2 = uniqueKwds[idx2]
                    if kwd1 == kwd2:
                        continue

                    weight = morphWeight[kwd2Morph[kwd1]]*morphWeight[kwd2Morph[kwd2]]
                    try:
                        if kwd2topic[kwd1] == kwd2topic[kwd2]:
                            weight+=topicWeight
                    except:
                        pass

                    pair = "%s<*>%s"%(kwd1,kwd2)
                    possible = "%s<*>%s"%(kwd2,kwd1)

                    if possible in kwdPair:
                        kwdPair[possible]+=weight
                    else:
                        try:
                            kwdPair[pair]+=weight
                        except:
                            kwdPair[pair]=weight

    return kwdPair



def get_top_pair(kwdPair, maxEdge=50):
    '''
    키워드 : 가중치 쌍의 딕셔너리를 받아 입력한 개수만큼의 상위 가중치 쌍을 딕셔너리에 담아 반환
    '''
    topPair = dict()

    ks = list(kwdPair.keys())
    vs = list(kwdPair.values())
    for _ in range(maxEdge):    
        w = max(list(vs))
        idx = vs.index(w)

        nodes = ks[idx].split('<*>')
        node1, node2 = nodes[0], nodes[1]

        try:
            topPair[node1][node2] = w
        except:
            topPair[node1] = dict()
            topPair[node1][node2] = w

        ks.pop(idx)
        vs.pop(idx)
    
    return topPair



def darw_networkx_network(topPair, kwd2Morph, kwd2topic, topicTitles, topicColors=['#EFC168','#EFED8C','#AEE155','#B280E9','#35DDD1']):
    
    '''
    networkx를 이용해 그래프를 작성한다.
    '''
    
    # topicColors = ['#DB4927','#EB02D4','#F7BA00','#830BF1','#97240A']
    # topicColors = ['#30EDE9','#34EC3C','#820BF0','#F5B901','#EC1C24']
    # topicColors=['#EFC168','#EFED8C','#AEE155','#B280E9','#35DDD1']
    
    countmax=-1
    countmin=100000
    for kwdFrom in topPair.keys():
        for kwdTo in topPair[kwdFrom].keys():
            weight = topPair[kwdFrom][kwdTo]
            if weight > countmax:
                countmax=weight
            if weight < countmin:
                countmin=weight

    G = nx.Graph(topPair)

    localConnectivity = dict()
    for pair in list(G.edges.keys()):
        try:
            localConnectivity[pair[0]]+=1
        except:
            localConnectivity[pair[0]]=1
        try:
            localConnectivity[pair[1]]+=1
        except:
            localConnectivity[pair[1]]=1

    for edge in G.edges.data():
        try:
            G.edges[edge[0],edge[1]]['weight'] = ((topPair[edge[0]][edge[1]] - countmin)/(countmax-countmin))*3+2        
        except:
            G.edges[edge[0],edge[1]]['weight'] = ((topPair[edge[1]][edge[0]] - countmin)/(countmax-countmin))*3+2
        
        G.edges[edge[0],edge[1]]['color'] = '#aaaaaa'

    for node in G.nodes.data():

        lc = localConnectivity[node[0]]
        if lc<5:
            G.nodes[node[0]]['size'] = 10
        elif lc<10:
            G.nodes[node[0]]['size'] = 20
        else:
            G.nodes[node[0]]['size'] = 30
        
        
        try:
            topic = kwd2topic[node[0]]
            G.nodes[node[0]]['title'] = str("토픽 %s : %s"%(topic,topicTitles[topic]))
            G.nodes[node[0]]['color'] = topicColors[topic-1]
        except:
            G.nodes[node[0]]['title'] = str("토픽 외")
            G.nodes[node[0]]['color'] = "#aaaaaa"

         
    return G


def pyvis_network_html(G, saveDir='./templates/',saveName='network',
                       heightPX = "1000px",
                       bgColor="#EDF0F5",
                       fontColor="#000000"):
    
    '''
    networkx로 작성된 그래프를 받아 pyvis를 이용해 html로 시각화 한다.
    '''
    
    nt = pyv.network.Network(height=heightPX, width="100%",bgcolor=bgColor,font_color=fontColor)
    # nt.barnes_hut(gravity=-550)
    nt.from_nx(G)
    nt.save_graph(saveDir+saveName+'.html')

