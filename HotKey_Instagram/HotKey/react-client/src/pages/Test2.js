import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import Left from "../images/Left.png";
import Right from "../images/Right.png";
import Header from "../components/Header.js";

console.log("현재화면크기 : ", window.innerWidth, "x", window.innerHeight);
const bg = [
  require("../images/ResultBackground0.png"), //1페이지백그라운드
  require("../images/ResultBackground1.png"), //2페이지백그라운드
];

const Test2 = () => {
  //레이아웃 테스트용
  const [sliderIdx, setSliderIdx] = useState(0);
  return (
    <>
      <Header />
      <Wrapper url={bg[sliderIdx]}>
        <ResultWrapper>
          <Slider style={{ transform: `translateX(-${sliderIdx * 95.5}vw)` }}>
            <SliderContent1>
              <Direction
                src={Right}
                onClick={() => {
                  setSliderIdx(1);
                }}
              ></Direction>
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
  font-size: 0px;
  background-image: url(${(prop) => prop.url});
  transition: 1s;
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
  transition: all 0.7s ease-out;
`;
const SliderContent1 = styled.div`
  height: 100%;
  width: 95.5vw;
`;
const SliderContent2 = styled.div`
  height: 100%;
  width: 95.5vw;
`;
const Direction = styled.img`
  display: block;
  cursor: pointer;
`;
export default Test2;
