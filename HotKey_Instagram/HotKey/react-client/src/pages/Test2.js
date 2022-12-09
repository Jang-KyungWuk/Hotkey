import React from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import styled from "styled-components";

const Test2 = () => {
  //레이아웃 테스트용
  return (
    <div>
      <Header loading={false} />
      <Wrapper>
        <Resultdiv>
          <img src={"/tmp_imgs/tmp.jpg"}></img>
        </Resultdiv>
      </Wrapper>
      <Footer />
    </div>
  );
};

//실제 결과가 들어갈 div
const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 9.5vh; //헤더크기(+0.5vh)만큼 margin주기
`;
// fetch된 경우 결과 보여줄 Result Div => min-height 속성
const Resultdiv = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 800px; //고정 픽셀값 (결과값은 크기가 작아지면 안될듯)
  width: 100vw; //유동 픽셀값 (추후 테스트 거쳐서 레이아웃 수정)
  align-items: center;
  background-color: ivory;
`;

export default Test2;
