import React, { useState } from "react";
import styled from "styled-components";
import Header_Logo from "../images/Header_Logo.jpg";
import Logo2 from "../images/Logo2.png";
import { useNavigate } from "react-router-dom";
const Header = ({ loading }) => {
  //loading => 분석결과페이지가 로딩중... (loading == True)
  //*****검색중 (서버가 돌아가는 중)에 뒤로가기를 누르게 되면 백엔드에서 크롤링 중인 세션 모두 로그아웃 시키는 등.. 조치가 필요하다!!!! */
  const [query, setQuery] = useState("");
  const navigate = useNavigate();
  return (
    <Headerdiv>
      <Logodiv>
        <Logo
          src={Header_Logo}
          onClick={() => {
            if (loading) {
              var confirmed = window.confirm(
                "현재 검색결과가 로딩 중입니다.\n검색창으로 돌아가시겠습니까?"
              );
              if (confirmed) navigate("/search");
            } else navigate("/search");
          }}
        ></Logo>
      </Logodiv>
      <Blank />
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
              else if (loading) {
                var confirmed = window.confirm(
                  "현재 검색결과가 로딩 중입니다.\n입력하신 키워드의 결과창으로 이동하시겠습니까?" +
                    "\n\n키워드 :  " +
                    query
                );
                if (confirmed) {
                  console.log("검색결과 페이지로 이동, keyword:" + query);
                  navigate("/search_result", {
                    state: { keyword: query },
                  });
                }
              } else {
                //로딩중이지 않은경우, 바로 이동
                console.log("검색결과 페이지로 이동, keyword:" + query);
                navigate("/search_result", {
                  state: { keyword: query },
                });
              }
            }}
          >
            SEARCH
          </Button>
          <Logodiv2>
            <Logoimg2
              src={Logo2}
              onClick={() => {
                window.open("http://localhost:3000/info");
              }}
            ></Logoimg2>
          </Logodiv2>
        </Div2>
      </Searchdiv>
    </Headerdiv>
  );
};

const Headerdiv = styled.div`
  display: flex;
  height: 9vh;
  width: 100vw;
  position: fixed;
  top: 0px;
  left: 2px;
`;
const Logodiv = styled.div`
  display: flex;
  height: 100%;
  width: 17%;
  align-items: center;
`;
const Logo = styled.img`
  margin-top: 2%;
  margin-left: 15%;
  display: block;
  height: 3.7vw;
  cursor: pointer;
`;
const Blank = styled.div`
  display: block;
  height: 100%;
  width: 10%;
`;
const Searchdiv = styled.div`
  display: flex;
  justify-content: center;
  align-items: flex-end;
  height: 100%;
  width: 70%;
`;
const Logodiv2 = styled.div`
  margin-left: 3%;
  display: flex;
  height: 100%;
  width: 20%;
  align-items: center;
  justify-content: center;
`;
const Logoimg2 = styled.img`
  display: block;
  height: 3vw;
  cursor: pointer;
`;
//searchbox를 감싸는 div
const Div2 = styled.div`
  display: flex;
  width: 100%;
  height: 80%;
  align-items: center;
  background-color: #d94925;
  border-radius: 20px;
`;
//input이 들어갈 Div
const Inputdiv = styled.div`
  margin-left: 3%;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 55%;
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
  margin-left: 3%;
  cursor: pointer;
  background-color: black;
  width: 13%;
  height: 65%;
  border-width: 1px;
  border-radius: 30px;
  font-family: Roboto;
  font-size: 1.3vw;
  color: white;
  letter-spacing: 0.2vw;
`;

Header.defaultProps = {
  loading: true,
};
export default Header;
