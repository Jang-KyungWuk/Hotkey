import React from "react";
import styled from "styled-components";
import Footer_image from "../images/Footer_image.jpg";

const Footer = () => {
  return (
    <Foot>
      <Img src={Footer_image}></Img>
    </Foot>
  );
};

const Foot = styled.div`
  display: flex;
  height: 60px;
  width: 100vw;
  border-top: 2px solid;
  // position: absolute;
  left: 2px;
`;
//이미지
const Img = styled.img`
  margin-top: 0.5%;
  margin-left: 1.5%;
  height: 90%;
  border: 0px solid;
`;

export default Footer;
