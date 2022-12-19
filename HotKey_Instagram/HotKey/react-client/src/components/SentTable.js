import React from "react";
import styled from "styled-components";

const SentTable = ({ sent_result }) => {
  let res = [
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"],
  ];
  for (let k = 0; k < sent_result.length; k++) {
    if (k > 6 && sent_result[k][1] < 4) break;
    res[k] = [k + 1, sent_result[k][0], sent_result[k][2]];
  }
  console.log(res);
  //스크롤 기능 추가하기.!
  return (
    <Table>
      <THead>
        <Th1>순위</Th1>
        <Th2>단어</Th2>
        <Th3>분류</Th3>
      </THead>
      <Tbody>
        {res.slice(0, -1).map((data) => (
          <>
            <Tr key={data[0]}>
              <Td1>{data[0]}</Td1>
              <Td2>{data[1]}</Td2>
              {data[2] === "긍정" ? (
                <Tdp>긍정</Tdp>
              ) : (
                <>
                  {data[2] === "부정" ? (
                    <Tdn>부정</Tdn>
                  ) : (
                    <>{data[2] === "중립" ? <Tdnn>중립</Tdnn> : <Td2>-</Td2>}</>
                  )}
                </>
              )}
            </Tr>
            <div style={{ height: "0px", borderBottom: "1px outset" }}></div>
          </>
        ))}
        <Tr>
          <Td1>{res[res.length - 1][0]}</Td1>
          <Td2>{res[res.length - 1][1]}</Td2>
          {res[res.length - 1][2] === "긍정" ? (
            <Tdp>긍정</Tdp>
          ) : (
            <>
              {res[res.length - 1][2] === "부정" ? (
                <Tdn>부정</Tdn>
              ) : (
                <>
                  {res[res.length - 1][2] === "중립" ? (
                    <Tdnn>중립</Tdnn>
                  ) : (
                    <Td2>-</Td2>
                  )}
                </>
              )}
            </>
          )}
        </Tr>
      </Tbody>
    </Table>
  );
};

const Table = styled.div`
  margin-top: 3%;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 96%;
  border-spacing: 0px;
  border: 1px outset;
  border-radius: 20px;
  overflow: hidden;
`;
const THead = styled.div`
  display: flex;
  width: 100%;
  height: 15%;
  background-color: black;
`;
const Th = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: calc(0.7vw + 0.7vh);
  font-family: chosun;
  letter-spacing: 0.15vw;
`;
const Th1 = styled(Th)`
  width: 20%;
  color: white;
`;
const Th2 = styled(Th)`
  width: 40%;
  color: white;
`;
const Th3 = styled(Th)`
  width: 40%;
  color: white;
`;
const Tr = styled.div`
  display: flex;
  width: 100%;
  height: 16.4%;
`;
const Tbody = styled.div`
  height: 85%;
  width: 100%;
  overflow-y: overlay;
  &::-webkit-scrollbar {
    width: 5px;
  }
  &::-webkit-scrollbar-track {
    background: white;
  }
  &::-webkit-scrollbar-thumb {
    background: gray;
    border-radius: 10px;
  }
`;

const Td1 = styled(Th)`
  width: 20%;
  height: 100%;
`;
const Td2 = styled(Th)`
  width: 40%;
  height: 100%;
`;
const Tdp = styled(Th)`
  color: #7db3f2;
  font-weight: bold;
  width: 40%;
  height: 100%;
`;
const Tdn = styled(Th)`
  color: #e17781;
  font-weight: bold;
  width: 40%;
  height: 100%;
`;
const Tdnn = styled(Th)`
  color: #d6dfe1;
  font-weight: bold;
  width: 40%;
  height: 100%;
`;

export default SentTable;
