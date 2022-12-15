import React from "react";
import styled from "styled-components";
import Footer_image from "../images/Footer_image.jpg";

const Footer = () => {
  return (
    <Foot>
      <Img
        src={Footer_image}
        onClick={() => {
          window.open("https://inisw.ictest.kr/");
        }}
      ></Img>
    </Foot>
  );
};

const Foot = styled.div`
  display: flex;
  height: 7vh;
  width: 100vw;
  border-top: 1px solid;
  // position: absolute;
  left: 2px;
  background-color: white;
`;
//이미지
const Img = styled.img`
  margin-top: 0.5%;
  margin-left: 1.5%;
  height: 90%;
  border: 0px solid;
  cursor: pointer;
`;

export default Footer;
