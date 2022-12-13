import React, { useState, useEffect } from "react";
import styled from "styled-components";
import NewLogo from "../images/NewLogo.png";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
const images = [
  require("../home_imgs/home0.png"),
  require("../home_imgs/home1.png"),
  require("../home_imgs/home2.png"),
  require("../home_imgs/home3.png"),
  require("../home_imgs/home4.png"),
];
const Home = () => {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [trendlist, setTrendList] = useState(["", "", "", "", ""]);
  //레이아웃 테스트용
  const [candidates, setCandidates] = useState(0);
  useEffect(() => {
    fetch("/trend_client")
      .then((res) => res.json())
      .then((data) => {
        setTrendList(data);
        console.log(data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);
  useEffect(() => {
    setTimeout(() => {
      if (candidates === images.length - 1) setCandidates(0);
      else setCandidates(candidates + 1);
    }, 7000);
  }, [candidates]);
  const onClick = (word) => {
    console.log("분석요청 페이지로 이동");
    navigate("/fetch", {
      state: { keyword: word },
    });
  };
  return (
    <Wrapper
      index={candidates}
      initial={{ opacity: 0.5 }}
      animate={{ opacity: 1 }}
      transition={{ ease: "easeOut", duration: 1 }}
    >
      {candidates}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
        }}
      >
        <motion.img
          src={NewLogo}
          style={{ height: "33vh", width: "90vw" }}
          initial={{ opacity: 0, y: "-30vh" }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.5, delay: 0.5 }}
        ></motion.img>
      </div>

      <BtDiv
        initial={{ opacity: 0.2, x: "30vw" }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 1.5 }}
      >
        <Div2>
          <Inputdiv>
            <Input
              autoFocus
              placeholder="키워드를 입력하세요"
              maxLength="20"
              onChange={(e) => {
                setQuery(e.target.value);
              }}
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  if (query.length >= 1) onClick(query);
                  else alert("검색어를 한 글자 이상 입력하세요");
                }
              }}
            ></Input>
          </Inputdiv>
          <Button
            onClick={() => {
              if (query.length >= 1) onClick(query);
              else alert("검색어를 한 글자 이상 입력하세요");
            }}
          >
            SEARCH
          </Button>
        </Div2>
        <Div3>
          <Trenddiv>
            <Trendbtn
              onClick={() => {
                if (trendlist[0].length > 0) onClick(trendlist[0]);
              }}
            >
              {trendlist[0]}
            </Trendbtn>
            <Trendbtn
              onClick={() => {
                if (trendlist[1].length > 0) onClick(trendlist[1]);
              }}
            >
              {trendlist[1]}
            </Trendbtn>
            <Trendbtn
              onClick={() => {
                if (trendlist[2].length > 0) onClick(trendlist[2]);
              }}
            >
              {trendlist[2]}
            </Trendbtn>
            <Trendbtn
              onClick={() => {
                if (trendlist[3].length > 0) onClick(trendlist[3]);
              }}
            >
              {trendlist[3]}
            </Trendbtn>
            <Trendbtn
              onClick={() => {
                if (trendlist[4].length > 0) onClick(trendlist[4]);
              }}
            >
              {trendlist[4]}
            </Trendbtn>
          </Trenddiv>
          <Trenddiv2></Trenddiv2>
        </Div3>
      </BtDiv>
    </Wrapper>
  );
};
const Wrapper = styled(motion.div)`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-image: url(${(props) => images[props.index]});
  transition: 2s;
  background-size: cover;
  font-size: 0px;
  overflow: hidden;
`;
//background에만 opacity를 적용하는것은 리액트에서는 어렵고, 배경이미지 후보는 매일 트렌드에 맞춰 관리자가 수동으로 정한다 => filter를 매뉴얼하게 해서 사진 등록.
//로고 아래를 채울 Div
const BtDiv = styled(motion.div)`
  width: 100vw;
  height: 77vh;
  display: flex;
  flex-direction: column;
  align-items: center;
`;
//검색input + button 들어갈 Div
const Div2 = styled.div`
  display: flex;
  margin-top: 0.5%;
  width: 60%;
  height: 10%;
  justify-content: space-around;
  align-items: center;
  //background-color: white;
  border-radius: 17px;
  box-shadow: 2px 5px 5px 1px black;
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
  border-left: 3px solid;
  border-right: 3px solid;
  background-color: white;
  box-shadow: 2px 3px 5px 1px black;
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
  // font-weight: bold;
  // color: #ce3909;
  color: white;
  letter-spacing: 0.2vw;
  box-shadow: 1px 3px 5px 1px gray;
`;
//trend 보여줄 Div
const Div3 = styled.div`
  display: flex;
  width: 60%;
  height: 20%;
  justify-content: center;
  flex-direction: column;
`;
//trend 위아래 Div
const Trenddiv = styled.div`
  display: flex;
  width: 100%;
  height: 50%;
  justify-content: space-around;
  align-items: center;
`;
const Trenddiv2 = styled.div`
  display: flex;
  width: 100%;
  height: 50%;
  justify-content: space-around;
  align-items: center;
`;
const Trendbtn = styled.button`
  cursor: pointer;
  width: 15%;
  height: 60%;
  border-radius: 30px;
  font-size: 1vw;
  background-color: black;
  color: white;
  font-family: Roboto;
  letter-spacing: 0.1vw;
  font-weight: bold;
  border: 0px solid;
  box-shadow: 2px 3px 5px 1px gray;
`;

export default Home;
