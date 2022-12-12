import React from "react";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import styled from "styled-components";
import Footer from "../components/Footer";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

const Start = () => {
  const navigate = useNavigate();
  return (
    <>
      <div style={{ height: "90vh" }}>
        <motion.div>
          <Wrapper>
            <Div1>
              <Logo src={HotKey_Logo}></Logo>
            </Div1>
            <Div2>
              <Title>Is your Keyword Hot?</Title>
            </Div2>
            <Div3>
              <Button
                onClick={() => {
                  navigate("/search");
                }}
              >
                SEARCH YOUR KEYWORD
              </Button>
            </Div3>
          </Wrapper>
        </motion.div>
      </div>
      <Footer></Footer>
    </>
  );
};
const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  height: 90vh;
  width: 100vw;
`;
const Div1 = styled.div`
  margin-top: 5%;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 13%;
  width: 100%;
`;
//텍스트들어갈거
const Div2 = styled.div`
  display: flex;
  width: 100%;
  height: 40%;
  justify-content: center;
`;
const Title = styled.h1`
  font-family: Roboto;
  font-size: 7vw; //폰트는 반응형으로
  font-weight: bold;
  text-align: center;
`;
//버튼 들어갈거
const Div3 = styled.div`
  display: flex;
  width: 100%;
  height: 30%;
  justify-content: center;
  align-items: center;
`;
const Button = styled.button`
  cursor: pointer;
  background-color: #ce3909;
  width: 40%;
  height: 40%;
  border-width: 0px;
  border-radius: 15px;
  font-family: Roboto;
  font-size: 3vw;
  color: white;
  letter-spacing: 3;
`;
const Logo = styled.img`
  display: block;
  height: 90%;
`;

export default Start;
