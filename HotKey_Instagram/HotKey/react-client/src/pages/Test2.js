import React, { useState, useEffect } from "react";
import styled from "styled-components";
import NewLogo from "../images/NewLogo.png";
import { motion } from "framer-motion";
import { TransitionGroup, CSSTransition } from "react-transition-group";

const images = [
  require("../home_imgs/home0.png"),
  require("../home_imgs/home1.png"),
  // require("../home_imgs/home2.png"),
  // require("../home_imgs/home3.png"),
  // require("../home_imgs/home4.png"),
];
console.log("현재화면크기 : ", window.innerWidth, "x", window.innerHeight);
const Test2 = () => {
  //레이아웃 테스트용
  const [candidates, setCandidates] = useState(0);

  useEffect(() => {
    setTimeout(() => {
      if (candidates === images.length - 1) setCandidates(0);
      else setCandidates(candidates + 1);
    }, 5000);
  }, [candidates]);
  return (
    <Wrapper
      index={candidates}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
    >
      {candidates}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
        }}
      >
        <motion.img
          src={NewLogo}
          style={{ height: "33vh", width: "90vw" }}
          initial={{ opacity: 0, y: "-30vh" }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.5, delay: 0.5 }}
        ></motion.img>
      </div>

      <BtDiv
        initial={{ opacity: 0.5, x: "30vw" }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 1.5 }}
      >
        <Div2>
          <Inputdiv>
            <Input
              autoFocus
              placeholder="키워드를 입력하세요"
              maxLength="20"
            ></Input>
          </Inputdiv>
          <Button>SEARCH</Button>
        </Div2>
        <Div3>
          <Trenddiv>
            <Trendbtn>손흥민</Trendbtn>
            <Trendbtn>네이마르</Trendbtn>
            <Trendbtn>브라질</Trendbtn>
            <Trendbtn>월드컵</Trendbtn>
            <Trendbtn>16강</Trendbtn>
          </Trenddiv>
          <Trenddiv2></Trenddiv2>
        </Div3>
      </BtDiv>
    </Wrapper>
  );
};

const Wrapper = styled(motion.div)`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-image: url(${(props) => images[props.index]});
  transition: 2s;
  background-size: cover;
  font-size: 0px;
`;
//background에만 opacity를 적용하는것은 리액트에서는 어렵고, 배경이미지 후보는 매일 트렌드에 맞춰 관리자가 수동으로 정한다 => filter를 매뉴얼하게 해서 사진 등록.
//로고 아래를 채울 Div
const BtDiv = styled(motion.div)`
  width: 100vw;
  height: 77vh;
  display: flex;
  flex-direction: column;
  align-items: center;
`;
//검색input + button 들어갈 Div
const Div2 = styled.div`
  display: flex;
  margin-top: 0.5%;
  width: 60%;
  height: 10%;
  justify-content: space-around;
  align-items: center;
  //background-color: white;
  border-radius: 17px;
  box-shadow: 2px 5px 5px 1px black;
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
  border-left: 3px solid;
  border-right: 3px solid;
  background-color: white;
  box-shadow: 2px 3px 5px 1px black;
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
  // font-weight: bold;
  // color: #ce3909;
  color: white;
  letter-spacing: 0.2vw;
  box-shadow: 1px 3px 5px 1px gray;
`;
//trend 보여줄 Div
const Div3 = styled.div`
  display: flex;
  width: 60%;
  height: 20%;
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
const Trenddiv2 = styled.div`
  display: flex;
  width: 100%;
  height: 50%;
  justify-content: space-around;
  align-items: center;
`;
const Trendbtn = styled.button`
  cursor: pointer;
  width: 15%;
  height: 60%;
  border-radius: 30px;
  // font-size: ${(props) => (props.len < 8 ? "1vw" : "0.7vw")};
  font-size: 1vw;
  // background-color: #e8e8e8;
  background-color: black;
  color: white;
  font-family: Roboto;
  letter-spacing: 0.1vw;
  font-weight: bold;
  border: 0px solid;
  box-shadow: 2px 3px 5px 1px gray;
`;

export default Test2;
