import React from "react";
import styled from "styled-components";

const Imagegrid = ({ image }) => {
  //모든 파일은 jpg로 저장된다고 가정
  //이미지 number

  if (image.slice(-1) === "0")
    return (
      <>
        {image.slice(0, -1) === "dddefault" ? (
          <Imgdiv1>
            <Img src={process.env.PUBLIC_URL + "/default.jpg"}></Img>
          </Imgdiv1>
        ) : (
          <Imgdiv1>
            <Img
              src={
                "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/top_imgs/0/" +
                image +
                ".jpg"
              }
              onClick={() => {
                window.open(
                  "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/top_imgs/0/" +
                    image +
                    ".jpg"
                );
              }}
            />
          </Imgdiv1>
        )}
      </>
    );
  else if (image.slice(-1) === "5")
    return (
      <>
        {image.slice(0, -1) === "dddefault" ? (
          <Imgdiv5>
            <Img src={process.env.PUBLIC_URL + "/default.jpg"}></Img>
          </Imgdiv5>
        ) : (
          <Imgdiv5>
            <Img
              src={
                "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/top_imgs/0/" +
                image +
                ".jpg"
              }
              onClick={() => {
                window.open(
                  "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/top_imgs/0/" +
                    image +
                    ".jpg"
                );
              }}
            />
          </Imgdiv5>
        )}
      </>
    );

  if (image.slice(0, -1) === "dddefault")
    return (
      <Imgdiv>
        <Img src={process.env.PUBLIC_URL + "/default.jpg"}></Img>
      </Imgdiv>
    );
  return (
    <Imgdiv>
      <Img
        src={
          "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/top_imgs/0/" +
          image +
          ".jpg"
        }
        onClick={() => {
          window.open(
            "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/images/top_imgs/0/" +
              image +
              ".jpg"
          );
        }}
      />
    </Imgdiv>
  );
};

const Imgdiv = styled.div`
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  border-radius: 5px;
  border: 1px outset;
  &:hover {
    transform: scale(1.4);
  }
  transition: all 0.2s ease-out;
`;
const Imgdiv1 = styled(Imgdiv)`
  grid-row-start: 1;
  grid-row-end: 3;
  grid-column-start: 1;
  grid-column-end: 3;
  &:hover {
    transform: scale(1.3);
  }
  transition: all 0.2s ease-out;
`;
const Imgdiv5 = styled(Imgdiv)`
  grid-row-start: 2;
  grid-row-end: 4;
  grid-column-start: 3;
  grid-column-end: 5;
  &:hover {
    transform: scale(1.4);
  }
  transition: all 0.2s ease-out;
`;
const Img = styled.img`
  height: 100%;
  width: 100%;
  border-radius: 0px;
  opacity: 1;
  cursor: pointer;
`;
export default Imagegrid;
