import React from "react";
import styled from "styled-components";
import PacmanLoader from "react-spinners/PacmanLoader";
import visualizing from "../images/visualizing.jpg";

const Loading3 = () => {
  return (
    <>
      <Load1>
        <Load11>
          <Load111>
            <PacmanLoader size={"2vw"} color={"#D94925"} />
          </Load111>
          <Load112>
            <Img src={visualizing} />
          </Load112>
        </Load11>
      </Load1>
    </>
  );
}; //loading div1 => 로딩중 action 구현
const Load1 = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 40%;
`;
//loading div1-1 => 각 loading section (총 3개)
const Load11 = styled.div`
  display: flex;
  height: 100%;
  width: 60%;
  align-items: center;
  justify-content: center;
`;
//loading div1-1-1 => Load11내부에서 Pacman이 들어갈 div
const Load111 = styled.div`
  display: flex;
  height: 100%;
  align-items: center;
  justify-content: center;
`;
//loading div1-1-2 => Load12내부에서 Text Img가 들어갈 div
const Load112 = styled.div`
  display: flex;
  margin-left: 10%;
  width: 65%;
  height: 100%;
  align-items: center;
  justify-content: center;
`;
//로딩 중 텍스트 이미지
const Img = styled.img`
  height: 15%;
  border: 0px solid;
`;
export default Loading3;
