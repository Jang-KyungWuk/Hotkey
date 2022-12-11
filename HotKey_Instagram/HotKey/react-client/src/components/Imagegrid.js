import React from "react";
import styled from "styled-components";

const Imagegrid = ({ image }) => {
  //   return <img src={require("../top_imgs/" + image)}></img>;
  return (
    <Imgdiv>
      <Img src={require("../top_imgs/" + image)} />
    </Imgdiv>
  );
};

const Imgdiv = styled.div`
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
`;
const Img = styled.img`
  height: 88%;
  width: 88%;
  border-radius: 10px;
`;
export default Imagegrid;
