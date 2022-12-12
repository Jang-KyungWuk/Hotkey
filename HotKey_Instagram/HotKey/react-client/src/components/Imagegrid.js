import React from "react";
import styled from "styled-components";

const Imagegrid = ({ image }) => {
  console.log(window.innerHeight, window.innerWidth); //페이지가 막 렌더링 될때의 window 사이즈
  if (image.slice(0, -1) === "dddefault")
    return (
      <Imgdiv>
        <Img src={process.env.PUBLIC_URL + "/default.jpg"}></Img>
      </Imgdiv>
    );
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
  height: 80%;
  width: 80%;
  border-radius: 10px;
  opacity: 1;
`;
export default Imagegrid;
