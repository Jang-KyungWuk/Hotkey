import React from "react";
import styled from "styled-components";
import PacmanLoader from "react-spinners/PacmanLoader";
import { PulseLoader } from "react-spinners";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faHourglassHalf,
  faFileLines,
  faChartBar,
  faCircleCheck,
  faThumbsUp,
} from "@fortawesome/free-regular-svg-icons";

const Loading3 = () => {
  return (
    <Div>
      <Div1>
        <Icondiv>
          <FontAwesomeIcon icon={faHourglassHalf} size="3x" />
        </Icondiv>
        <Textdiv>데이터를 수집하고 있습니다</Textdiv>
        <Spindiv>
          <FontAwesomeIcon icon={faCircleCheck} size="3x" />
        </Spindiv>
      </Div1>
      <Div2>
        <Icondiv>
          <FontAwesomeIcon icon={faChartBar} size="3x" />
        </Icondiv>
        <Textdiv>수집된 데이터를 분석하고 있습니다</Textdiv>
        <Spindiv>
          <FontAwesomeIcon icon={faThumbsUp} size="3x" />
        </Spindiv>
      </Div2>
      <Div3>
        <Icondiv>
          <FontAwesomeIcon icon={faFileLines} size="3x" />
        </Icondiv>
        <Textdiv>분석된 데이터를 출력하고 있습니다</Textdiv>
        <Spindiv>
          <PulseLoader size={10} />
        </Spindiv>
      </Div3>
    </Div>
  );
}; //전체 감싸는 Div
const Div = styled.div`
  margin-top: 10%;
  margin-left: 5%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 40%;
  width: 80%;
  border-radius: 20px;
`;
//첫번째 칸
const Div1 = styled.div`
  display: flex;
  height: 30%;
`;
//아이콘 들어갈 칸
const Icondiv = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 15%;
`;
//텍스트 들어갈 칸
const Textdiv = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 70%;
  font-family: chosun;
  font-size: 30px;
`;
//spinner 들어갈 칸
const Spindiv = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 15%;
`;
//두번째 칸
const Div2 = styled.div`
  display: flex;
  height: 30%;
  border-radius: 20px;
`;
//세번째 칸
const Div3 = styled.div`
  display: flex;
  height: 30%;
  border-radius: 20px;
`;
export default Loading3;
