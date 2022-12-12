from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from kiwipiepy import Kiwi
from wordcloud import WordCloud
from PIL import Image
from preprocess import *

# input수정 (filedir, keyword) 추가


def sklda(plaintext, filedir='../react-client/src/visualization/lda_results/', keyword='tmp', n_top_words=300, n_iter=30):
    """
    ------------------------------------------------------------------------------

    텍스트를 받아 lda로 토픽을 나눕니다.
    토픽 수 별로 perplexity를 계산 한 후, perplexity값이 가장 낮은 토픽 수로 분석한 결과를 리스트로 리턴합니다.
    각 토픽 별 워드클라우드 이미지를 생성합니다.

    ------------------------------------------------------------------------------

    파라미터 설명

    plaintext : txt, 인스타그램 포스트들이 수집된 원문 텍스트. 'HOTKEY123!@#'로 포스트들을 구분한다.
    n_top_words : int, 각 토픽 별로 상위 몇 개의 단어를 리턴할 지
    n_iter : int, lda 분석 반복 수

    ------------------------------------------------------------------------------
    """
    try:
        # 형태소분석기 키위 인스턴스 생성
        kiwi = Kiwi()
        kiwi.prepare()

    # 전처리함수를 통해 스팸포스트 제거
        print("\nFiltering spam post...")
        t0 = time()
        t1 = time()
        doc = preprocess(plaintext, sep='HOTKEY123!@#',
                         returnPlain=True).replace('#', '').split('HOTKEY123!@')
        # doc = plaintext
        print("done in %0.3fs." % (time() - t0))

        print("\nExtracting kiwi features for LDA...")
        t0 = time()

    # sklearn CountVectorizer의 tokenizer 변수에 넣을 함수 정의
        def tokenize_ko(doc):
            tokens = kiwi.tokenize(doc)
    #         추가로 사용해 볼 만한 태그들
            tagset = {'VA-I',  'MAG', 'XR', 'NNP', 'NNG'}
    #         tagset = {'NNP', 'NNG'}
            results = []
            for token in tokens:
                if token.tag in tagset:
                    results.append(token.form)
            return results

    # sklearn CountVectorizer를 통한 전처리
        kiwi_vectorizer = CountVectorizer(
            min_df=2, max_features=1000, tokenizer=tokenize_ko)
        kiwivoca = kiwi_vectorizer.fit_transform(doc)
        print("done in %0.3fs." % (time() - t0))

    # sklearn lda 분석을 통해 2~5개의 토픽 수 중 perplexity가 가장 낮은 값 찾기
        print("\nFinding the optimal number of topics...")
        t0 = time()
        perplexity = []
        for i in range(2, 6):
            lda = LatentDirichletAllocation(
                n_components=i,
                max_iter=n_iter,
                learning_method="online",
                learning_offset=50.0,
                random_state=0,
            )
            lda.fit(kiwivoca)
            perplexity.append(lda.perplexity(kiwivoca))

    # 가장 낮은 perplexity 값을 가지는 최적의 토픽 수로 저장
        n_topics = perplexity.index(min(perplexity))+2
        print(perplexity)
        print("done in %0.3fs." % (time() - t0),
              f"the optimal number of topics is {n_topics}")

    # 최적의 토픽 수로 lda분석
        print("\nFitting LDA models with KIWI features, number of topics=%d, max_iter=%d" % (
            n_topics, n_iter))
        t0 = time()
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            max_iter=n_iter,
            learning_method="online",
            learning_offset=50.0,
            random_state=0,
        )
        lda.fit(kiwivoca)

    # 토픽 넘버 : 해당 토픽의 토큰들 의 형태로 출력, 같은 토픽의 토큰들로 구성된 리스트 생성
        kiwi_feature_names = kiwi_vectorizer.get_feature_names_out()
        topic_list = []
        for topic_idx, topic in enumerate(lda.components_):
            top_features_ind = topic.argsort()[: -n_top_words - 1: -1]
            top_features = [kiwi_feature_names[i] for i in top_features_ind]
            topic_list.append(top_features)
            #print('Topic {}: {}'.format(topic_idx+1, ' '.join(top_features)))

        print("done in %0.3fs." % (time() - t0))

        print("\nGenerating word cloud for each topics")
        t0 = time()

    # 워드클라우드 생성 수 찾기

        if perplexity[0] > perplexity[2]:
            lda = LatentDirichletAllocation(
                n_components=4,
                max_iter=n_iter,
                learning_method="online",
                learning_offset=50.0,
                random_state=0,
            )
        else:
            lda = LatentDirichletAllocation(
                n_components=2,
                max_iter=n_iter,
                learning_method="online",
                learning_offset=50.0,
                random_state=0,
            )
        lda.fit(kiwivoca)

    # 워드클라우드 마스크 이미지 생성

        im1 = Image.open('./templates/masks/mask3.png')
        im2 = Image.open('./templates/masks/mask4.png')
        im3 = Image.open('./templates/masks/mask5.png')
        im4 = Image.open('./templates/masks/mask7.png')

    # 이미지 파일 전처리
        mask1 = Image.new("RGB", im1.size, (255, 255, 255))
        mask1.paste(im1)
    #     mask1 = mask1.resize((500, 400))
        mask1 = np.array(mask1)

        mask2 = Image.new("RGB", im2.size, (255, 255, 255))
        mask2.paste(im2)
    #     mask2 = mask2.resize((500, 400))
        mask2 = np.array(mask2)

        mask3 = Image.new("RGB", im3.size, (255, 255, 255))
        mask3.paste(im3)
    #     mask3 = mask3.resize((500, 400))
        mask3 = np.array(mask3)

        mask4 = Image.new("RGB", im4.size, (255, 255, 255))
        mask4.paste(im4)
    #     mask4 = mask4.resize((500, 400))
        mask4 = np.array(mask4)

        mask = []
        mask.append(mask1)
        mask.append(mask2)
        mask.append(mask3)
        mask.append(mask4)

    # 워드클라우드 생성
        terms = kiwi_vectorizer.get_feature_names()
        terms_count = 200

        for idx, topic in enumerate(lda.components_):
            print('Topic# ', idx+1)
            abs_topic = abs(topic)
            topic_terms = [[terms[i], topic[i]]
                           for i in abs_topic.argsort()[:-terms_count-1:-1]]
            topic_terms_sorted = [[terms[i], topic[i]]
                                  for i in abs_topic.argsort()[:-terms_count - 1:-1]]
            topic_words = []
            for i in range(terms_count):
                topic_words.append(topic_terms_sorted[i][0])
            # print(','.join(word for word in topic_words))
            dict_word_frequency = {}

            for i in range(terms_count):
                dict_word_frequency[topic_terms_sorted[i]
                                    [0]] = topic_terms_sorted[i][1]
            wc = WordCloud(background_color="white", colormap='autumn', mask=mask[idx], max_words=100,
                           max_font_size=60, min_font_size=10, prefer_horizontal=0.9, font_path='./templates/fonts/NanumGothic.ttf')
            wc.generate_from_frequencies(dict_word_frequency)
            # wc.to_file(filename=f'./templates/lda_results/Topic#{idx+1}.png')
            # 1212수정_세윤
            wc.to_file(filename=filedir+keyword+str(idx+1)+'.png')

        print("done in %0.3fs." % (time() - t0))
        print("in total, %0.3fs." % (time() - t1))

        return True, topic_list
    except:
        return False, []
