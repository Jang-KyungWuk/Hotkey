import React from "react";
import styled from "styled-components";

const SentTable = ({ sent_result }) => {
  let res = [];
  for (let k = 0; k < sent_result.length; k++) {
    res[k] = [k + 1, sent_result[k][0], sent_result[k][2]];
  }
  //스크롤 기능 추가하기.!
  return (
    <Table>
      <THead>
        <Tr>
          <Td>순위</Td>
          <Td>단어</Td>
          <Td>분류</Td>
        </Tr>
      </THead>
      <Tbody>
        {res.map((data) => (
          <Tr key={data[0]}>
            <Td>{data[0]}</Td>
            <Td>{data[1]}</Td>
            {data[2] === "긍정" ? (
              <Tdp>긍정</Tdp>
            ) : (
              <>{data[2] === "부정" ? <Tdn>부정</Tdn> : <Tdnn>중립</Tdnn>}</>
            )}
          </Tr>
        ))}
      </Tbody>
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
  height: 13%;
  background-color: black;
  color: white;
`;
const Tbody = styled.tbody`
  height: 87%;
  width: 100%;
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
