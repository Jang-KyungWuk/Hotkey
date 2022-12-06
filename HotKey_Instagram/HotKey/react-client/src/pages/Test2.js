import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import styled from "styled-components";
import loading from "../images/loading.jpg";

const Test2 = () => {
  //레이아웃 테스트용
  return (
    <div>
      <Header></Header>
      <Wrapper></Wrapper>
      <Footer></Footer>
    </div>
  );
};

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  height: 2000px; //수정하기
  width: 100vw;
  align-items: center;
  background-color: ivory;
`;
//로고 들어갈거
const Div1 = styled.div`
  margin-top: 5%;
  display: flex;
  margin-bottom: 3%;
  align-items: center;
  justify-content: center;
  height: 10%;
  width: 100%;
`;
const Logo = styled.img`
  display: block;
  height: 100%;
`;
//검색input + button 들어갈 Div
const Div2 = styled.div`
  display: flex;
  width: 50%;
  height: 8%;
  justify-content: space-around;
  align-items: center;
  background-color: #d94925;
  border-radius: 20px;
`;
//input이 들어갈 Div
const Inputdiv = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 70%;
  height: 65%;
  border-radius: 30px;
  border: 0px solid;
  background-color: white;
`;
//input박스
const Input = styled.input`
  width: 90%;
  height: 80%;
  border-radius: 30px;
  border: 0px solid;
  font-family: Roboto;
  font-size: 1.3vw;
  &:focus {
    outline: none;
  }
`;
//검색button 박스
const Button = styled.button`
  cursor: pointer;
  background-color: black;
  width: 17%;
  height: 65%;
  border-width: 1px;
  border-radius: 30px;
  font-family: Roboto;
  font-size: 1.3vw;
  color: white;
  letter-spacing: 3px;
`;
//trend 보여줄 Div
const Div3 = styled.div`
  margin-top: 0.5%;
  display: flex;
  width: 50%;
  height: 12%;
  justify-content: center;
  flex-direction: column;
`;
//trend 위아래 Div
const Trenddiv = styled.div`
  display: flex;
  width: 100%;
  height: 50%;
  justify-content: space-around;
  align-items: center;
`;
//trend button
const Trendbtn = styled.button`
  cursor: pointer;
  background-color: black;
  width: 20%;
  height: 70%;
  border-radius: 30px;
  letter-spacing: 2px;
  font-size: 0.8vw;
  color: white;
  font-family: Roboto;
`;
//이미지를 background로 하는 div
const Img = styled.img`
  width: 70vw;
  border: 0px solid;
`;
export default Test2;
