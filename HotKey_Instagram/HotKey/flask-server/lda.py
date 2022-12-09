from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from kiwipiepy import Kiwi
from preprocess import preprocess

# LDA => 결과값만 리턴


def sklda(plaintext, n_top_words=30, n_iter=30):
    """
    ------------------------------------------------------------------------------

    텍스트를 받아 lda로 토픽을 나눕니다.
    토픽 수 별로 perplexity를 계산 한 후, perplexity값이 가장 낮은 토픽 수로 분석한 결과를 리스트로 리턴합니다.

    ------------------------------------------------------------------------------

    파라미터 설명

    plaintext : txt, 인스타그램 포스트들이 수집된 원문 텍스트. 'HOTKEY123!@#'로 포스트들을 구분한다.
    n_top_words : int, 각 토픽 별로 상위 몇 개의 단어를 리턴할 지
    n_iter : int, lda 분석 반복 수

    ------------------------------------------------------------------------------
    """
# 형태소분석기 키위 인스턴스 생성
    kiwi = Kiwi()
    kiwi.prepare()

# 전처리함수를 통해 스팸포스트 제거
    print("\nFiltering spam post...")
    t0 = time()
    t1 = time()
    doc = preprocess(plaintext, sep='HOTKEY123!@#',
                     returnPlain=True).replace('#', '').split('HOTKEY123!@')
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
        print('Topic {}: {}'.format(topic_idx+1, ' '.join(top_features)))

    print("done in %0.3fs." % (time() - t0))
    print("in total, %0.3fs." % (time() - t1))
    return topic_list
