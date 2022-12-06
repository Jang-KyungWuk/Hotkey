import React, { useEffect, useState } from "react";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import search_insert from "../images/search_insert.jpg";
import Footer from "../components/Footer";
import { useNavigate, Link } from "react-router-dom";
import styled from "styled-components";

const SearchInput = () => {
  const [query, setQuery] = useState("");
  const [trendlist, setTrendList] = useState([]);
  const navigate = useNavigate();
  useEffect(() => {
    fetch("/trend_client")
      .then((res) => res.json())
      .then((data) => {
        setTrendList(data);
      });
  }, []);

  useEffect(() => {
    //trendlist잘 받아오는지 테스트용 코드..
    console.log("받아온 trendlist :", trendlist);
    console.log(trendlist[0]);
  }, [trendlist]);

  const onClick = (word) => {
    console.log("검색결과 페이지로 이동");
    navigate("/search_result", {
      state: { keyword: word },
    });
  };

  return (
    <div>
      <Wrapper>
        <Div1>
          <Link to="/search" style={{ height: "100%" }}>
            <Logo src={HotKey_Logo}></Logo>
          </Link>
        </Div1>
        {query.length === 0 ? (
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
                    alert("검색어를 한 글자 이상 입력하세요");
                  }
                }}
              ></Input>
            </Inputdiv>
            <Button
              onClick={() => {
                alert("검색어를 한 글자 이상 입력하세요");
              }}
            >
              SEARCH
            </Button>
          </Div2>
        ) : (
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
                    onClick(query);
                  }
                }}
              ></Input>
            </Inputdiv>
            <Button
              onClick={() => {
                onClick(query);
              }}
            >
              SEARCH
            </Button>
          </Div2>
        )}
        <Div3>
          <Trenddiv>
            <Trendbtn
              onClick={() => {
                onClick(trendlist[0]);
              }}
            >
              {trendlist[0]}
            </Trendbtn>
            <Trendbtn
              onClick={() => {
                onClick(trendlist[1]);
              }}
            >
              {trendlist[1]}
            </Trendbtn>
            <Trendbtn
              onClick={() => {
                onClick(trendlist[2]);
              }}
            >
              {trendlist[2]}
            </Trendbtn>
            <Trendbtn
              onClick={() => {
                onClick(trendlist[3]);
              }}
            >
              {trendlist[3]}
            </Trendbtn>
          </Trenddiv>
          <Trenddiv>
            <Trendbtn
              onClick={() => {
                onClick(trendlist[4]);
              }}
            >
              {trendlist[4]}
            </Trendbtn>
            <Trendbtn
              onClick={() => {
                onClick(trendlist[5]);
              }}
            >
              {trendlist[5]}
            </Trendbtn>
            <Trendbtn
              onClick={() => {
                onClick(trendlist[6]);
              }}
            >
              {trendlist[6]}
            </Trendbtn>
          </Trenddiv>
        </Div3>
        <div
          style={{
            display: "flex",
            height: "53%",
            flexDirection: "column",
            justifyContent: "center",
          }}
        >
          <Img src={search_insert} alt="search_insert.jpg"></Img>
        </div>
      </Wrapper>
      <Footer></Footer>
    </div>
  );
};
const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  height: 95vh;
  width: 100vw;
  align-items: center;
`;
//로고 들어갈거
const Div1 = styled.div`
  margin-top: 5%;
  display: flex;
  margin-bottom: 3%;
  align-items: center;
  justify-content: center;
  height: 10%;
  width: 100%;
`;
const Logo = styled.img`
  display: block;
  height: 100%;
`;
//검색input + button 들어갈 Div
const Div2 = styled.div`
  display: flex;
  width: 50%;
  height: 8%;
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
//trend 보여줄 Div
const Div3 = styled.div`
  margin-top: 0.5%;
  display: flex;
  width: 50%;
  height: 12%;
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
//trend button
const Trendbtn = styled.button`
  cursor: pointer;
  background-color: black;
  width: 20%;
  height: 70%;
  border-radius: 30px;
  font-size: 1vw;
  color: white;
  font-family: Roboto;
`;
//이미지를 background로 하는 div
const Img = styled.img`
  width: 70vw;
  border: 0px solid;
`;
export default SearchInput;
