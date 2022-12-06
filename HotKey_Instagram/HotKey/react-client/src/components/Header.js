import React, { useState } from "react";
import styled from "styled-components";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import { useNavigate } from "react-router-dom";
const Header = () => {
  //*****검색중 (서버가 돌아가는 중)에 뒤로가기를 누르게 되면 백엔드에서 크롤링 중인 세션 모두 로그아웃 시키는 등.. 조치가 필요하다!!!! */
  const [query, setQuery] = useState("");
  const navigate = useNavigate();
  return (
    <Headerdiv>
      <Logodiv>
        <Logo
          src={HotKey_Logo}
          onClick={() => {
            var confirmed = window.confirm("검색창으로 돌아가시겠습니까?");
            if (confirmed) navigate("/search");
          }}
        ></Logo>
      </Logodiv>
      <Searchdiv>
        <Div2>
          <Inputdiv>
            <Input
              placeholder="키워드를 입력하세요"
              maxLength="20"
              onChange={(e) => {
                setQuery(e.target.value);
                //=> query 만 설정하고, on enter 기능은 없애기!
              }}
            ></Input>
          </Inputdiv>
          <Button
            onClick={() => {
              if (query.length === 0) alert("검색어를 한 글자 이상 입력하세요");
              else {
                console.log("검색결과 페이지로 이동");
                navigate("/search_result", {
                  state: { keyword: query },
                });
              }
            }}
          >
            SEARCH
          </Button>
        </Div2>
      </Searchdiv>
    </Headerdiv>
  );
};

const Headerdiv = styled.div`
  display: flex;
  height: 9vh;
  width: 100vw;
  position: sticky;
  top: 8px;
  background-color: white;
`;
const Logodiv = styled.div`
  display: flex;
  height: 100%;
  width: 30%;
  align-items: center;
`;
const Logo = styled.img`
  margin-top: 2%;
  margin-left: 20%;
  display: block;
  height: 80%;
  cursor: pointer;
`;
const Searchdiv = styled.div`
  display: flex;
  justify-content: flex-end;
  align-items: center;
  height: 100%;
  width: 70%;
`;
const Div2 = styled.div`
  margin-right: 10%;
  display: flex;
  width: 80%;
  height: 80%;
  justify-content: space-around;
  align-items: center;
  background-color: #d94925;
  border-radius: 20px;
`;
//input이 들어갈 Div
const Inputdiv = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 70%;
  height: 65%;
  border-radius: 30px;
  border: 0px solid;
  background-color: white;
`;
//input박스
const Input = styled.input`
  width: 90%;
  height: 80%;
  border-radius: 30px;
  border: 0px solid;
  font-family: Roboto;
  font-size: 1.3vw;
  &:focus {
    outline: none;
  }
`;
//검색button 박스
const Button = styled.button`
  cursor: pointer;
  background-color: black;
  width: 17%;
  height: 65%;
  border-width: 1px;
  border-radius: 30px;
  font-family: Roboto;
  font-size: 1.3vw;
  color: white;
  letter-spacing: 3px;
`;

export default Header;
