import React from "react";
import styled from "styled-components";

const SentTable = ({ sent_result }) => {
  const res = sent_result;
  return (
    <Table>
      <THead>
        <tr>
          <td>단어</td>
          <td>빈도 수</td>
          <td>분류</td>
        </tr>
      </THead>
      <tbody>
        <tr>
          <td>{res[0][0]}</td>
          <td>{res[0][1]}</td>
          <td>{res[0][2]}</td>
        </tr>
        <tr>
          <td>{res[1][0]}</td>
          <td>{res[1][1]}</td>
          <td>{res[1][2]}</td>
        </tr>
        <tr>
          <td>{res[2][0]}</td>
          <td>{res[2][1]}</td>
          <td>{res[2][2]}</td>
        </tr>
        <tr>
          <td>{res[3][0]}</td>
          <td>{res[3][1]}</td>
          <td>{res[3][2]}</td>
        </tr>
        <tr>
          <td>{res[4][0]}</td>
          <td>{res[4][1]}</td>
          <td>{res[4][2]}</td>
        </tr>
        <tr>
          <td>{res[5][0]}</td>
          <td>{res[5][1]}</td>
          <td>{res[5][2]}</td>
        </tr>
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
  border-radius: 20px;
`;
const THead = styled.thead`
  font-size: calc(0.7vw + 0.7vh);
  font-weight: bold;
  height: 15%;
`;
const Td1 = styled.td`
  background-color: blue;
`;

export default SentTable;
