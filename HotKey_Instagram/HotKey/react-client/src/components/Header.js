import React from "react";
import styled from "styled-components";
import Header_Logo from "../images/Header_Logo.jpg";
import Header_Logo2 from "../images/Header_Logo2.jpg";
import Logo2 from "../images/Logo2.jpg";
import { useNavigate } from "react-router-dom";
const Header = () => {
  //loading => 분석결과페이지가 로딩중... (loading == True)
  //*****검색중 (서버가 돌아가는 중)에 뒤로가기를 누르게 되면 백엔드에서 크롤링 중인 세션 모두 로그아웃 시키는 등.. 조치가 필요하다!!!! */

  const navigate = useNavigate();
  return (
    <Headerdiv>
      <Logodiv0>
        <Logoimg0
          src={Header_Logo}
          onClick={() => {
            if (window.confirm("검색창으로 돌아가시겠습니까?")) navigate("/");
          }}
        ></Logoimg0>
      </Logodiv0>
      <Logodiv1>
        <Logo
          src={Header_Logo2}
          onClick={() => {
            if (window.confirm("검색창으로 돌아가시겠습니까?")) navigate("/");
          }}
        ></Logo>
      </Logodiv1>
      <Logodiv2>
        <Logoimg2
          src={Logo2}
          onClick={() => {
            window.open("http://localhost:3000/info");
          }}
        ></Logoimg2>
      </Logodiv2>
    </Headerdiv>
  );
};

const Headerdiv = styled.div`
  display: flex;
  align-items: center;
  height: 7vh;
  width: 100vw;
  position: fixed;
  top: 0px;
  left: 2px;
  background-color: black;
`;
const Logodiv0 = styled.div`
  display: flex;
  height: 100%;
  width: 18%;
  margin-left: 2%;
  // justify-content: center;
  align-items: center;
`;
const Logodiv1 = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 60%;
`;
const Logo = styled.img`
  display: block;
  height: 65%;
  cursor: pointer;
`;
const Logodiv2 = styled.div`
  display: flex;
  height: 100%;
  width: 20%;
  align-items: center;
  justify-content: center;
`;
const Logoimg0 = styled.img`
  display: block;
  height: 70%;
  cursor: pointer;
`;
const Logoimg2 = styled.img`
  display: block;
  width: 70%;
  cursor: pointer;
`;
export default Header;
