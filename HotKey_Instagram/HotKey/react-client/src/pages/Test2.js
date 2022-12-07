import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import styled from "styled-components";
import loading from "../images/loading.jpg";
import Loading1 from "../components/Loading1";
import Loading2 from "../components/Loading2";
import Loading3 from "../components/Loading3";

const Test2 = () => {
  //레이아웃 테스트용
  const [lstate, setLstate] = useState(0);
  /*로딩 상태!! => 'loading'변수 : 전체 loading이 완료 되었는지
  서버에서 keyword 크롤링 요청 -> 서버에서 corpus 받아오면 setLstate(1) 
  -> corpus와 image를 다시 서버에 전달, 분석 요청 
  -> 서버에서 result받으면 setLstate(2)
  -> (눈속임) sleep(3)하고 setLstate(0)하고 loading = false로 바꾸기
  */
  useEffect(() => {
    console.log("useEffect시작");

    setTimeout(() => {
      console.log("아오1");
      setLstate(1);
      setTimeout(() => {
        console.log("아오2");
        setLstate(2);
        setTimeout(() => {
          console.log("아오3");
          setLstate(0);
        }, 1000);
      }, 2000);
    }, 3000);
  }, []);
  if (lstate === 0)
    return (
      <div>
        <Header />
        <Wrapper>
          <Loadingdiv>
            <Loading1 />
            <Load2>
              <Img src={loading}></Img>
            </Load2>
          </Loadingdiv>
        </Wrapper>
        <Footer />
      </div>
    );
  else if (lstate === 1)
    return (
      <div>
        <Header />
        <Wrapper>
          <Loadingdiv>
            <Loading2 />
            <Load2>
              <Img src={loading}></Img>
            </Load2>
          </Loadingdiv>
        </Wrapper>
        <Footer />
      </div>
    );
  else
    return (
      <div>
        <Header />
        <Wrapper>
          <Loadingdiv>
            <Loading3 />
            <Load2>
              <Img src={loading}></Img>
            </Load2>
          </Loadingdiv>
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
  background-color: black;
`;
// fetch되지 않은 경우, 로딩 Div => 반응형
const Loadingdiv = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 2vh;
  width: 100vw;
  height: 80vh;
`;
//loading div2 => 분석중 이미지가 들어갈 div
const Load2 = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 60%;
`;
//이미지
const Img = styled.img`
  height: 90%;
  border: 0px solid;
`;

export default Test2;
