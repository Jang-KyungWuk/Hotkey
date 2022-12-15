import React from "react";
import styled from "styled-components";

const SentTable = ({ sent_result }) => {
  let res = [];
  for (let i = 6; i < sent_result.length; i++) {
    if (sent_result[i][1] < 7) {
      res = sent_result.slice(0, i);
      break;
    }
  }
  //스크롤 기능 추가하기.!
  console.log(res);
  return (
    <Table>
      <THead>
        <tr>
          <Td>단어</Td>
          <Td>빈도</Td>
          <Td>분류</Td>
        </tr>
      </THead>
      <tbody>
        <Tr>
          <Td>{res[0][0]}</Td>
          <Td>{res[0][1]}</Td>
          <Tdp>{res[0][2]}</Tdp>
        </Tr>
        <Tr>
          <Td>{res[0][0]}</Td>
          <Td>{res[0][1]}</Td>
          <Tdn>부정</Tdn>
        </Tr>
        <Tr>
          <Td>{res[0][0]}</Td>
          <Td>{res[0][1]}</Td>
          <Tdnn>중립</Tdnn>
        </Tr>
        <Tr>
          <Td>{res[0][0]}</Td>
          <Td>{res[0][1]}</Td>
          <Tdp>{res[0][2]}</Tdp>
        </Tr>
        <Tr>
          <Td>{res[0][0]}</Td>
          <Td>{res[0][1]}</Td>
          <Tdp>{res[0][2]}</Tdp>
        </Tr>
        <Tr>
          <td>{res[0][0]}</td>
          <td>{res[0][1]}</td>
          <Tdn>부정</Tdn>
        </Tr>
      </tbody>
    </Table>
  );
};

const Table = styled.table`
  font-family: chosun;
  letter-spacing: 0.15vw;
  text-align: center;
  width: 100%;
  height: 100%;
  // border-radius: 20px;
  // border: 1.5px outset;
  border-collapse: seperate;
  border-spacing: 0px;
  border: 1px outset;
  border-radius: 20px;
`;
const THead = styled.thead`
  font-size: calc(0.7vw + 0.7vh);
  font-weight: bold;
  height: 15%;
  background-color: black;
  color: white;
`;
const Tr = styled.tr`
  font-size: calc(0.7vw + 0.7vh);
`;
//긍 7DB3F2 / 부 E17781 / 중립 D6DFE1
const Td = styled.td`
  border-bottom: 1px outset;
`;
const Tdp = styled.td`
  border-bottom: 1px outset black;
  color: #7db3f2;
  font-weight: bold;
`;
const Tdn = styled.td`
  border-bottom: 1px outset black;
  color: #e17781;
  font-weight: bold;
`;
//중립
const Tdnn = styled.td`
  border-bottom: 1px outset black;
  color: #d6dfe1;
  font-weight: bold;
`;
const Td1 = styled.td`
  border-bottom: 1px solid;
  color: #d6dfe1;
`;

export default SentTable;
