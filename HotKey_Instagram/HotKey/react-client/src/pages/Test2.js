import React, { useState } from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import Left from "../images/Left.png";
import Right from "../images/Right.png";
import Header from "../components/Header.js";
import Imagegrid from "../components/Imagegrid";

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
            <SliderContent1>
              <Page11>
                <Page111>
                  <Page1111>키워드</Page1111>
                  <Page1112>
                    <P1>지금 이 시간 당신이 궁금한 ' 키워드 '</P1>
                    <P2>
                      MADE BY [조 이름]
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
                      {/* <Img
                        src={require("../visualization/wordcloud/우래기.png")}
                      ></Img> */}
                      <h1>이미지</h1>
                    </Page12221>
                    <Page12222>
                      <P4>
                        지금 이 시간,
                        <br />
                        사람들이 주목하는 핫 키워드
                      </P4>
                    </Page12222>
                  </Page1222>
                  <Page1223>
                    <Direction
                      src={Right}
                      onClick={() => {
                        setSliderIdx(1);
                      }}
                    ></Direction>
                  </Page1223>
                </Page122>
              </Page12>
            </SliderContent1>
            <SliderContent2>
              <Direction
                src={Left}
                onClick={() => {
                  setSliderIdx(0);
                }}
              ></Direction>
            </SliderContent2>
          </Slider>
        </ResultWrapper>
      </Wrapper>
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
const SliderContent1 = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 95.5vw;
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
  justify-content: flex-end;
  height: 90%;
  width: 100%;
`;
//Page122의 왼족, 이미지 그리드 들어갈 공간
const Page1221 = styled.div`
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(3, 1fr);
  grid-gap: 10px;
  width: 42%;
  margin-top: 1%;
  margin-right: 4%;
  height: 85%;
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
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
`;
//워드클라우드 이미지
const Img = styled.img`
  display: block;
  width: 100%;
`;
//Page 1222의 아래쪽, 텍스트
const Page12222 = styled.div`
  width: 100%;
  height: 20%;
`;
//Page 12222의 텍스트
const P4 = styled.div`
  display: flex;
  margin-left: 8%;
  // justify-content: flex-end;
  font-size: calc(0.8vw + 0.8vh);
  font-family: chosun;
  line-height: 110%;
`;
//Page122의 맨 오른족, 버튼들어갈 공간
const Page1223 = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 6%;
`;
const SliderContent2 = styled.div`
  height: 100%;
  display: flex;
  flex-direction: column;
  width: 95.5vw;
`;
const Direction = styled.img`
  display: block;
  cursor: pointer;
  width: 90%;
  width: 50px;
`;

export default Test2;
