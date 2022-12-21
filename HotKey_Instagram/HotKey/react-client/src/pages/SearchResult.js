import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useLocation, useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import Left from "../images/Left.png";
import Right from "../images/Right.png";
import Header from "../components/Header.js";
import Imagegrid from "../components/Imagegrid";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import SentTable from "../components/SentTable.js";

const bg = [
  require("../images/ResultBackground0.png"), //1페이지백그라운드
  require("../images/ResultBackground1.png"), //2페이지백그라운드
  require("../images/ResultBackground2.png"), //3페이지백그라운드
];
const SearchResult = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const key_word = location.state?.key_word;
  const image_num = location.state?.image_num;
  const topic_num = location.state?.topic_num;
  const sent_result = location.state?.sent_result;
  const status = location.state?.status;
  const [sliderIdx, setSliderIdx] = useState(0);
  useEffect(() => {
    console.log("status :", status);
    if (location.state && status === false) {
      alert("데이터 분석에 실패했습니다. 잠시 후에 다시 시도해주세요");
      navigate("/");
    }
  }, []);

  let image_list = [
    "dddefault0",
    "dddefault1",
    "dddefault2",
    "dddefault3",
    "dddefault4",
    "dddefault5",
    "dddefault6",
    "dddefault7",
    "dddefault8",
  ];
  for (let i = 0; i < image_num; i++) {
    image_list[i] = key_word.toLowerCase() + i;
  }
  let topic_list = ["dddefault0", "dddefault1", "dddefault2", "dddefault3"];
  for (let i = 0; i < topic_num; i++) {
    topic_list[i] = key_word.toLowerCase() + i;
  }

  console.log("image_list :", image_list);
  console.log("topic_list :", topic_list);
  console.log("topic_num :", topic_num);
  console.log("key_word :", key_word);
  console.log("sent_result : ", sent_result);

  const sent1 = "지금 이 시간 당신이 궁금한 '" + key_word + "'";
  return (
    <>
      {status === true ? (
        <>
          <Header />
          <Wrapper url={bg[sliderIdx]}>
            <ResultWrapper>
              <Slider
                style={{ transform: `translateX(-${sliderIdx * 95.5}vw)` }}
              >
                <SliderContent1>
                  <Tmp1>
                    <Page11>
                      <Page111>
                        <Page1111>{key_word}</Page1111>
                        <Page1112>
                          <P1>{sent1}</P1>
                          <P2>
                            MADE BY [핫키 에디터]
                            <br />
                            @고려대학교 지능정보 SW아카데미
                            <br />
                            #인스타그램으로보는 #실시간 #트렌드 #분석
                          </P2>
                        </Page1112>
                      </Page111>
                    </Page11>
                    <Page12>
                      <Page121>
                        <Page1211>
                          <P3>
                            지금 이 시간,
                            <br />
                            사람들이 주목하는 핫한 사진
                          </P3>
                        </Page1211>
                      </Page121>
                      <Page122>
                        <Page1221>
                          {image_list.map((file) => (
                            <Imagegrid key={file} image={file} />
                          ))}
                        </Page1221>
                        <Page1222>
                          <Page12221>
                            <Img
                              src={
                                "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/wordcloud/" +
                                key_word.toLowerCase() +
                                ".png"
                              }
                              onClick={() => {
                                window.open(
                                  "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/wordcloud/" +
                                    key_word.toLowerCase() +
                                    ".png"
                                );
                              }}
                            ></Img>
                          </Page12221>
                          <Page12222>
                            <P4>
                              지금 이 시간,
                              <br />
                              사람들이 주목하는 핫 키워드
                            </P4>
                          </Page12222>
                        </Page1222>
                      </Page122>
                    </Page12>
                  </Tmp1>
                  <ButtonDiv>
                    <Direction
                      src={Right}
                      onClick={() => {
                        setSliderIdx(1);
                      }}
                    ></Direction>
                  </ButtonDiv>
                </SliderContent1>
                <SliderContent2>
                  <Page21>
                    <Direction
                      src={Left}
                      onClick={() => {
                        setSliderIdx(0);
                      }}
                    ></Direction>
                  </Page21>
                  <Page22>
                    <Page221>
                      <Page2211 url={require("../images/TextCircle.jpg")}>
                        <H1>{key_word}</H1>
                      </Page2211>
                      <Page2212>
                        <BarImg
                          src={
                            "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/barplot/" +
                            key_word.toLowerCase() +
                            ".png"
                          }
                          onClick={() => {
                            window.open(
                              "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/barplot/" +
                                key_word.toLowerCase() +
                                ".png"
                            );
                          }}
                        />
                      </Page2212>
                    </Page221>
                    <Page222>
                      <Page2221>
                        <P5>
                          지금 이 시간
                          <br />
                          키워드에 대한 사람들의 느낌은
                        </P5>
                      </Page2221>
                      <Page2222>
                        <BarImg
                          src={
                            "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/sent_results/" +
                            key_word.toLowerCase() +
                            ".png"
                          }
                          onClick={() => {
                            window.open(
                              "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/sent_results/" +
                                key_word.toLowerCase() +
                                ".png"
                            );
                          }}
                        />
                      </Page2222>
                      <Page2223>
                        <SentTable sent_result={sent_result} />
                      </Page2223>
                    </Page222>
                    <Page223>
                      <Page2231>
                        <Page22311>
                          <Page223111>
                            <Page2231111>
                              <br />
                              지금 이 시간
                              <br />
                              키워드간의 연관관계가 보고 싶다면
                            </Page2231111>
                            <Page2231112>
                              <NetButton
                                onClick={() => {
                                  console.log("네트워크 팝업 구현");
                                  //json에서 proxy설정한 것은 리액트 자체에서 request할때만 작용하는 것으로보임, 아래처럼 서버에 직접 접근하려면 서버의 주소를 적어줘야한다.
                                  //팝업창 옵션 (창 크기 조절 등 조정)
                                  const l = 0.15 * window.innerWidth;
                                  const w = 0.7 * window.innerWidth;
                                  const t = 0.05 * window.innerHeight;
                                  const h = 0.95 * window.innerHeight;
                                  const popupOption =
                                    "left=" +
                                    l +
                                    ", top=" +
                                    t +
                                    ", width=" +
                                    w +
                                    ", height =" +
                                    h +
                                    ", status=no;";
                                  window.open(
                                    "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/network/" +
                                      key_word.toLowerCase() +
                                      ".html",
                                    "",
                                    popupOption
                                  );
                                }}
                              >
                                네트워크 보기
                              </NetButton>
                            </Page2231112>
                          </Page223111>
                          <Page223112>
                            <P>
                              <span
                                style={{
                                  fontWeight: "bold",
                                  fontSize: "calc(1vw + 1vh)",
                                }}
                              >
                                네트워크
                              </span>
                              란,
                              <br />
                              단어들 간의 연관 관계를
                              <br />
                              <span style={{ color: "#e17781" }}>정점</span>과
                              <span style={{ color: "#7db3f2" }}>간선</span>으로
                              표현합니다.
                              <br />
                              <span style={{ color: "#e17781" }}>
                                이어져 있으면
                              </span>{" "}
                              <span style={{ fontWeight: "bold" }}>연관어</span>
                              , <br />
                              <span style={{ color: "#7db3f2" }}>
                                색이 같으면
                              </span>{" "}
                              <span style={{ fontWeight: "bold" }}>
                                유사 주제의 단어
                              </span>
                              입니다.
                            </P>
                          </Page223112>
                        </Page22311>
                        <Page22312>
                          <P6>
                            지금 이 시간
                            <br />
                            핫키 에디터가 나눈 토픽 분류별 모음
                            <br />
                          </P6>
                          <>*키워드를 기반으로 숨겨진 주제를 찾아놓았습니다.</>
                        </Page22312>
                      </Page2231>
                      <Page2232>
                        {topic_num === 2 ? (
                          <>
                            <Gridx>
                              <GridImg
                                style={{ height: "65%", width: "55%" }}
                                src={process.env.PUBLIC_URL + "/searching.png"}
                              ></GridImg>
                            </Gridx>
                            <Gridx>"두 개의 토픽으로 최적화 됩니다"</Gridx>
                            <Grid>
                              <GridImg
                                src={
                                  "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                  topic_list[0] +
                                  ".png"
                                }
                                onClick={() => {
                                  window.open(
                                    "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                      topic_list[0] +
                                      ".png"
                                  );
                                }}
                              ></GridImg>
                            </Grid>
                            <Grid>
                              <GridImg
                                src={
                                  "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                  topic_list[1] +
                                  ".png"
                                }
                                onClick={() => {
                                  window.open(
                                    "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                      topic_list[1] +
                                      ".png"
                                  );
                                }}
                              ></GridImg>
                            </Grid>
                          </>
                        ) : (
                          <>
                            <Grid>
                              <GridImg
                                src={
                                  "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                  topic_list[0] +
                                  ".png"
                                }
                                onClick={() => {
                                  window.open(
                                    "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                      topic_list[0] +
                                      ".png"
                                  );
                                }}
                              ></GridImg>
                            </Grid>
                            <Grid>
                              <GridImg
                                src={
                                  "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                  topic_list[1] +
                                  ".png"
                                }
                                onClick={() => {
                                  window.open(
                                    "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                      topic_list[1] +
                                      ".png"
                                  );
                                }}
                              ></GridImg>
                            </Grid>
                            <Grid>
                              <GridImg
                                src={
                                  "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                  topic_list[2] +
                                  ".png"
                                }
                                onClick={() => {
                                  window.open(
                                    "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                      topic_list[2] +
                                      ".png"
                                  );
                                }}
                              ></GridImg>
                            </Grid>
                            <Grid>
                              <GridImg
                                src={
                                  "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                  topic_list[3] +
                                  ".png"
                                }
                                onClick={() => {
                                  window.open(
                                    "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/visualization/lda_results/" +
                                      topic_list[3] +
                                      ".png"
                                  );
                                }}
                              ></GridImg>
                            </Grid>
                          </>
                        )}
                      </Page2232>
                    </Page223>
                    <Ttmp></Ttmp>
                  </Page22>
                </SliderContent2>
              </Slider>
            </ResultWrapper>
          </Wrapper>
        </>
      ) : (
        <div>
          <Link to="/">
            <img
              src={HotKey_Logo}
              style={{ width: 300, height: 100 }}
              alt="hotkey_logo.."
            ></img>
          </Link>
          <h1>페이지가 존재하지 않습니다.</h1>
          <Link to="/">검색페이지로 돌아가기</Link>
        </div>
      )}
    </>
  );
};
const Wrapper = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 7vh; //헤더 크기 만큼
  height: 93vh; //헤더 크기만큼 빼기
  width: 100vw;
  background-size: cover;
  background-image: url(${(prop) => prop.url});
  transition: all 1s ease-out;
`;
const ResultWrapper = styled.div`
  display: flex;
  height: 96.5%;
  width: 95.5%;
  background-color: white;
  overflow: hidden;
`;
const Slider = styled.div`
  position: relative;
  display: flex;
  width: calc(3 * 95.5vw);
  height: 100%;
  transition: all 0.5s ease-in;
`;
const SliderContent1 = styled.div`
  display: flex;
  flex-direction: row;
  height: 100%;
  width: 95.5vw;
`;
//page1의 왼쪽 (버튼 없이 결과만 들어가는)
const Tmp1 = styled.div`
  height: 100%;
  width: 96%;
`;
//page1의 맨 오른쪽 (버튼 들어갈 공간)
const ButtonDiv = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 4%;
`;
//page1의위
const Page11 = styled.div`
  height: 27%;
`;
//Page11의 왼쪽 (Text자리)
const Page111 = styled.div`
  display: flex;
  align-items: center;
  height: 100%;
  width: 80%;
`;
//Page111의 왼쪽 (키워드자리)
//글자수가 6개이상이면  width 변경!!, calc(3.8vw + 3.8vh)로 조정
const Page1111 = styled.div`
  display: flex;
  width: 40%;
  height: 100%;
  justify-content: flex-end;
  align-items: center;
  font-family: chosun;
  font-size: calc(4.3vw + 4.3vh);
  letter-spacing: -1px;
`;
//Page111의 오른쪽 (description)
//키워드가 6글자 이상이면 width, margin 변경!!
const Page1112 = styled.div`
  display: flex;
  flex-direction: column;
  margin-left: 5%;
  width: 55%;
  height: 100%;
  align-items: flex-start;
`;
const P1 = styled.p`
  font-size: calc(1.2vw + 1.2vh);
  font-family: chosun;
  font-weight: bold;
`;
const P2 = styled.p`
  font-size: calc(0.8vw + 0.8vh);
  font-family: chosun;
  line-height: 130%;
`;
//page1의아래
const Page12 = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 73%;
`;
//page12의 위, 텍스트 들어갈 공간
const Page121 = styled.div`
  display: flex;
  height: 10%;
  width: 100%;
`;
//Page121의 왼쪽, 텍스트 들어갈 공간
const Page1211 = styled.div`
  display: flex;
  margin-left: 8%;
  height: 100%;
  width: 45%;
  align-items: flex-end;
`;
const P3 = styled.p`
  font-size: calc(0.8vw + 0.8vh);
  font-family: chosun;
  line-height: 110%;
  margin-bottom: 3px;
`;
//Page12의 아래, 레이아웃 들어갈 공간
const Page122 = styled.div`
  display: flex;
  height: 90%;
  width: 100%;
`;
//Page122의 왼족, 이미지 그리드 들어갈 공간
const Page1221 = styled.div`
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(3, 1fr);
  grid-gap: 10px;
  width: 46%;
  margin-left: 5%;
  margin-top: 1%;
  margin-right: 4%;
  height: 90%;
`;
//Page122 의 오른쪽, 워드클라우드 & 텍스트 들어갈 공간
const Page1222 = styled.div`
  width: 42%;
  height: 97%;
  display: flex;
  flex-direction: column;
`;
//Page 1222의 위쪽, 워드클라우드
const Page12221 = styled.div`
  width: 95%;
  height: 80%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  border: 1px outset;
  &:hover {
    border: 0px outset;
    border-radius: 20px;
  }
  // overflow: hidden;
`;
//워드클라우드 이미지
const Img = styled.img`
  display: block;
  height: 100%;
  cursor: pointer;
  &:hover {
    transform: scale(1.35);
    border: 1px outset;
    border-radius: 20px;
  }
  transition: all 0.2s ease-out;
`;
//barplot전용 이미지
const BarImg = styled.img`
  display: block;
  height: 100%;
  cursor: pointer;
  &:hover {
    transform: scale(1.1);
    border: 1px outset;
    border-radius: 20px;
  }
  transition: all 0.2s ease-out;
`;
//Page 1222의 아래쪽, 텍스트
const Page12222 = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  height: 20%;
`;
//Page 12222의 텍스트
const P4 = styled.div`
  display: flex;
  margin-left: 8%;
  height: 70%;
  font-size: calc(0.8vw + 0.8vh);
  font-family: chosun;
  line-height: 120%;
`;
const SliderContent2 = styled.div`
  height: 100%;
  display: flex;
  flex-direction: row;
  width: 95.5vw;
`;
const Direction = styled.img`
  display: block;
  cursor: pointer;
  width: 60%;
`;
//2페이지
//버튼 들어갈 공간
const Page21 = styled.div`
  display: flex;
  flex-diretion: column;
  justify-content: center;
  align-items: center;
  width: 4%;
  height: 100%;
`;
const Page22 = styled.div`
  margin-left: 3%;
  display: flex;
  justify-content: space-around;
  height: 96%;
  width: 96%;
`;

//////////////
//2페이지 오른쪽 맨 왼쪽
const Page221 = styled.div`
  width: 21%;
`;
//Page221의 위, 이미지+키워드 들어갈자리
const Page2211 = styled.div`
  margin: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 27%;
  width: 80%;
  background-image: url(${(prop) => prop.url});
  background-size: 100% 100%;
`;
//Page2211에 들어가는 텍스트, 텍스트 길이에 따라 폰트 조정해야함! (1.3씩 정도?)
const H1 = styled.p`
  font-size: calc(1.8vw + 1.8vh);
  font-family: chosun;
`;
//Page221의 아래, 빈도분석 result 들어갈자리
const Page2212 = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 73%;
  border: 1px outset;
  border-radius: 20px;
`;
//2페이지 오른쪽 중간
const Page222 = styled.div`
  width: 21%;
`;
//14%, 42%, 42%
//Page222의 맨 위 글자 들어갈 div
const Page2221 = styled.div`
  display: flex;
  flex-direciton: column;
  align-items: flex-end;
  height: 20%;
`;
const P5 = styled.div`
  font-size: calc(0.8vw + 0.8vh);
  font-family: chosun;
  line-height: 120%;
  margin-bottom: 3%;
`;
//Page222의 중간 감성분석 pie chart 들어갈 div
const Page2222 = styled.div`
  height: 40%;
  border: 1px outset;
  border-radius: 20px;
  font-family: chosun;
  font-size: calc(1vw + 1vh);
  display: flex;
  justify-content: center;
  align-items: center;
`;
//Page223의 아래 감성분석 결과 table div
const Page2223 = styled.div`
  height: 40%;
  border: 0px outset;
  border-radius: 20px;
`;
//2페이지 오른쪽 맨 오른쪽
const Page223 = styled.div`
  width: 50%;
`;
const Ttmp = styled.div`
  width: 5%;
`;
//Page223의 위 (네트워크 + 설명까지)
const Page2231 = styled.div`
  height: 45%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
`;
//Page2231의 위 (네트워크)
const Page22311 = styled.div`
  display: flex;
  height: 50%;
`;
//Page22311 왼쪽 (텍스트, 버튼)
const Page223111 = styled.div`
  width: 50%;
`;
//Page223111 위 ( 텍스트 )
const Page2231111 = styled.div`
  height: 50%;
  margin-left: 10%;
  width: 90%;
  font-size: calc(0.8vw + 0.8vh);
  font-family: chosun;
  line-height: 120%;
`;
//Page223111 아래 ( 버튼div )
const Page2231112 = styled.div`
  margin-top: 2%;
  height: 40%;
  display: flex;
  justify-content: center;
  align-items: center;
`;
//네트워크버튼
const NetButton = styled.button`
  height: 100%;
  width: 85%;
  background-color: black;
  color: white;
  font-size: calc(1vw + 1vh);
  font-family: chosun;
  letter-spacing: 0.2vw;
  cursor: pointer;
  border-radius: calc(0.5vw + 0.5vh);
  border: 0px solid;
  transition: all 0.4s ease-out;
  &:hover {
    background-color: gray;
    color: black;
  }
`;
//Page22311오른쪽 (네트워크 보는법 설명)
const Page223112 = styled.div`
  font-size: calc(0.6vw + 0.6vh);
  width: 40%;
  // border: 1px outset;
  // border-radius: 20px;
  font-family: chosun;
  font-size: calc(0.7vw + 0.7vh);
  // display: flex;
  // justify-content: center;
  // align-items: center;
  text-align: center;
`;
const P = styled.p`
  margin-left: 5%;
  line-height: 3.3vh;
  text-align: left;
`;
//Page2231의 아래 (설명)
const Page22312 = styled.div`
  height: 40%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-family: chosun;
  line-height: 200%;
  font-size: calc(0.6vw + 0.6vh);
`;
const P6 = styled.div`
  font-size: calc(1vw + 1vh);
  font-family: chosun;
  line-height: 150%;
  text-align: center;
`;
//Page223의 아래 (토픽모델링 워드클라우드)
const Page2232 = styled.div`
  margin: auto;
  height: 53%;
  width: 80%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  grid-row-gap: 2%;
  grid-column-gap: 2%;
  padding: 1%;
`;
//그리드 자식 컴포넌트
const Grid = styled.div`
  height: 100%;
  width: 100%;
  border: 1px outset;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: chosun;
  font-size: 1.2vw;
  text-align: center;
  &:hover {
    transform: scale(1.2);
  }
  transition: all 0.2s ease-out;
`;
const Gridx = styled.div`
  height: 100%;
  width: 100%;
  border: 1px outset;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: chosun;
  font-size: 1.2vw;
  text-align: center;
`;
const GridImg = styled.img`
  width: 86%;
  cursor: pointer;
`;

export default SearchResult;
