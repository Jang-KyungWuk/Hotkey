import React, { useEffect, useState } from "react";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import search_insert from "../images/search_insert.jpg";
import recommend from "../images/recommend.jpg";
import Footer from "../components/Footer";
import { useNavigate, Link } from "react-router-dom";
import styled from "styled-components";
import { motion } from "framer-motion";

const SearchInput = () => {
  const [query, setQuery] = useState("");
  const [trendlist, setTrendList] = useState(undefined);
  const navigate = useNavigate();
  useEffect(() => {
    fetch("/trend_client")
      .then((res) => res.json())
      .then((data) => {
        setTrendList(data);
      })
      .catch((err) => {
        console.log(err);
        alert(err);
      });
  }, []);

  useEffect(() => {
    //trendlist잘 받아오는지 테스트용 코드..
    console.log("받아온 trendlist :", trendlist);
  }, [trendlist]);

  const onClick = (word) => {
    console.log("분석요청 페이지로 이동");
    navigate("/search_fetch", {
      state: { keyword: word },
    });
  };
  return (
    <>
      <div style={{ height: "90vh" }}>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <Wrapper>
            <Div1>
              <Link to="/" style={{ height: "100%" }}>
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
            <Recommend>{/* <RecomImg src={recommend}></RecomImg> */}</Recommend>
            {trendlist !== undefined ? (
              <Div3>
                <Trenddiv>
                  <Trendbtn
                    len={trendlist[0].length}
                    id={0}
                    onClick={() => {
                      onClick(trendlist[0]);
                    }}
                  >
                    {trendlist[0]}
                  </Trendbtn>
                  <Trendbtn
                    len={trendlist[1].length}
                    id={1}
                    onClick={() => {
                      onClick(trendlist[1]);
                    }}
                  >
                    {trendlist[1]}
                  </Trendbtn>
                  <Trendbtn
                    len={trendlist[2].length}
                    id={2}
                    onClick={() => {
                      onClick(trendlist[2]);
                    }}
                  >
                    {trendlist[2]}
                  </Trendbtn>
                  <Trendbtn
                    len={trendlist[3].length}
                    id={3}
                    onClick={() => {
                      onClick(trendlist[3]);
                    }}
                  >
                    {trendlist[3]}
                  </Trendbtn>
                </Trenddiv>
                <Trenddiv2>
                  <Trendbtn
                    len={trendlist[4].length}
                    id={4}
                    onClick={() => {
                      onClick(trendlist[4]);
                    }}
                  >
                    {trendlist[4]}
                  </Trendbtn>
                  <Trendbtn
                    len={trendlist[5].length}
                    id={5}
                    onClick={() => {
                      onClick(trendlist[5]);
                    }}
                  >
                    {trendlist[5]}
                  </Trendbtn>
                  <Trendbtn
                    len={trendlist[6].length}
                    id={6}
                    onClick={() => {
                      onClick(trendlist[6]);
                    }}
                  >
                    {trendlist[6]}
                  </Trendbtn>
                </Trenddiv2>
              </Div3>
            ) : (
              <Div3>
                <Trenddiv>
                  <Trendbtn
                    len={1}
                    id={0}
                    onClick={() => {
                      onClick(trendlist[0]);
                    }}
                  ></Trendbtn>
                  <Trendbtn
                    len={1}
                    id={1}
                    onClick={() => {
                      onClick(trendlist[1]);
                    }}
                  ></Trendbtn>
                  <Trendbtn
                    len={1}
                    id={2}
                    onClick={() => {
                      onClick(trendlist[2]);
                    }}
                  ></Trendbtn>
                  <Trendbtn
                    len={1}
                    id={3}
                    onClick={() => {
                      onClick(trendlist[3]);
                    }}
                  ></Trendbtn>
                </Trenddiv>
                <Trenddiv2>
                  <Trendbtn
                    len={1}
                    id={4}
                    onClick={() => {
                      onClick(trendlist[4]);
                    }}
                  ></Trendbtn>
                  <Trendbtn
                    len={1}
                    id={5}
                    onClick={() => {
                      onClick(trendlist[5]);
                    }}
                  ></Trendbtn>
                  <Trendbtn
                    len={1}
                    id={6}
                    onClick={() => {
                      onClick(trendlist[6]);
                    }}
                  ></Trendbtn>
                </Trenddiv2>
              </Div3>
            )}
            <div
              style={{
                display: "flex",
                height: "56%",
                flexDirection: "column",
                justifyContent: "flex-end",
              }}
            >
              <Img src={search_insert} alt="search_insert.jpg"></Img>
            </div>
          </Wrapper>
        </motion.div>
      </div>
      <Footer></Footer>
    </>
  );
};
const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  height: 90vh;
  width: 100vw;
  align-items: center;
`;
//로고 들어갈거
const Div1 = styled.div`
  margin-top: 3%;
  display: flex;
  margin-bottom: 2%;
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
  // background-color: #d94925;
  background-color: white;
  border-radius: 20px;
  box-shadow: 2px 5px 5px 1px gray;
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
  color: #ce3909;
  letter-spacing: 0.2vw;
  box-shadow: 1px 3px 5px 1px gray;
`;
const Recommend = styled.div`
  display: flex;
  width: 50%;
  height: 2%;
  align-items: flex-end;
`;
//trend 보여줄 Div
const Div3 = styled.div`
  display: flex;
  width: 50%;
  height: 10%;
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
//trend button
const color_array = [
  "#FAECC8",
  "#F4CC7E",
  "#FFE193",
  "#FAECC8",
  "#FFE193",
  "#FAECC8",
  "#F4CC7E",
];
const Trendbtn = styled.button`
  cursor: pointer;
  width: 20%;
  height: 80%;
  border-radius: 30px;
  font-size: ${(props) => (props.len < 8 ? "1vw" : "0.7vw")};
  background-color: #e8e8e8;
  color: black;
  font-family: Roboto;
  letter-spacing: 0.1vw;
  font-weight: bold;
  border: 0px solid;
  box-shadow: 2px 3px 5px 1px gray;
`;
//이미지
const Img = styled.img`
  width: 70vw;
  border: 0px solid;
`;
const RecomImg = styled.img`
  height: 90%;
  border: 0px solid;
`;
export default SearchInput;
