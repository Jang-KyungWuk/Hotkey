import React, { useState } from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import Left from "../images/Left.png";
import Header from "../components/Header.js";
import Explain from "../images/Explain.png";

console.log("현재화면크기 : ", window.innerWidth, "x", window.innerHeight);
const bg = [
  require("../images/ResultBackground0.png"), //1페이지백그라운드
  require("../images/ResultBackground1.png"), //2페이지백그라운드
];

const Test2 = () => {
  //레이아웃 테스트용
  let image_list = [
    // "네이마르0",
    // "네이마르1",
    // "네이마르2",
    // "네이마르3",
    // "네이마르4",
    // "네이마르5",
    // "네이마르6",
    // "네이마르7",
    // "네이마르8",
  ];
  const [sliderIdx, setSliderIdx] = useState(0);
  return (
    <>
      <Header />
      <Wrapper url={bg[sliderIdx]}>
        <ResultWrapper>
          <Slider style={{ transform: `translateX(-${sliderIdx * 95.5}vw)` }}>
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
                    <H1>인스타그램</H1>
                  </Page2211>
                  <Page2212>[빈도분석 result]</Page2212>
                </Page221>
                <Page222>
                  <Page2221>
                    <P5>
                      지금 이 시간
                      <br />
                      키워드에 대한 사람들의 느낌은
                    </P5>
                  </Page2221>
                  <Page2222>[감성분석 piechart]</Page2222>
                  <Page2223>[감성분석 table]</Page2223>
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
                          <NetButton>네트워크 보기</NetButton>
                        </Page2231112>
                      </Page223111>
                      <Page223112>[네트워크 보는법 설명]</Page223112>
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
                    <Grid>
                      <GridImg
                        src={require("../visualization/lda_results/국정원0.png")}
                      ></GridImg>
                    </Grid>

                    <Grid>
                      <GridImg
                        src={require("../visualization/lda_results/국정원0.png")}
                      ></GridImg>
                    </Grid>
                    <Grid>
                      <GridImg
                        src={require("../visualization/lda_results/국정원0.png")}
                      ></GridImg>
                    </Grid>
                    <Grid>
                      <GridImg
                        src={require("../visualization/lda_results/국정원0.png")}
                      ></GridImg>
                    </Grid>
                  </Page2232>
                </Page223>
                <Ttmp></Ttmp>
              </Page22>
            </SliderContent2>
          </Slider>
        </ResultWrapper>
      </Wrapper>
    </>
  );
};

const SliderContent2 = styled.div`
  height: 100%;
  display: flex;
  align-items: center;
  flex-direction: row;
  width: 95.5vw;
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
const Direction = styled.img`
  display: block;
  cursor: pointer;
  width: 60%;
`;
//결과 들어갈 공간 2페이지 오른쪽
const Page22 = styled.div`
  display: flex;
  justify-content: space-around;
  width: 93%;
  height: 97%;
`;
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
  height: 73%;
  background-color: ivory;
  border: 1px solid;
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
  background-color: ivory;
  border: 1px solid;
  border-radius: 20px;
`;
//Page223의 아래 감성분석 결과 table div
const Page2223 = styled.div`
  height: 40%;
  background-color: ivory;
  border: 1px solid;
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
`;
//Page22311오른쪽 (네트워크 보는법 설명)
const Page223112 = styled.div`
  width: 40%;
  background-color: ivory;
  border: 1px solid;
  border-radius: 20px;
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
  border: 0.5px solid;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
`;
const GridImg = styled.img`
  width: 87%;
`;
//여기부터 1페이지
const Wrapper = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 7vh; //헤더 크기 만큼
  height: 93vh; //헤더 크기만큼 빼기
  width: 100vw;
  background-size: cover;
  background-image: url(${(prop) => prop.url});
  transition: all 0.5s ease-out;
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
  width: calc(2 * 95.5vw);
  height: 100%;
  transition: all 0.5s ease-in;
`;

export default Test2;
