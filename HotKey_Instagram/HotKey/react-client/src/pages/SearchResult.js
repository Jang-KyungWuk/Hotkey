import React from "react";
import styled from "styled-components";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import Footer from "../components/Footer";
import Header from "../components/Header";

const SearchResult = () => {
  const location = useLocation();
  //   const navigate = useNavigate();
  const image_list = location.state?.image_list;
  const key_word = location.state?.key_word;
  console.log("분석 결과 페이지 렌더링...");
  console.log("image_list :", image_list);
  console.log("key_word :", key_word);
  return (
    <>
      {location.state ? (
        <div>
          <Header loading={false} />
          <Resultdiv>
            <ResultWrapper>
              <Page1>
                <Page11>
                  <Page111></Page111>
                  <Page112>
                    {/* {image_list.map((file) => (
                    <img
                      key={file}
                      src={require("../top_imgs/" + file)}
                      style={{ height: "10%", width: "20%" }}
                      alt="임시"
                    ></img>
                  ))} */}
                  </Page112>
                </Page11>
                <Page12></Page12>
              </Page1>
              <Page2>
                <Page21></Page21>
                <Page22></Page22>
              </Page2>
            </ResultWrapper>
          </Resultdiv>
          <Footer />
        </div>
      ) : (
        <div>
          <Link to="/">
            <img
              src={HotKey_Logo}
              style={{ width: 300, height: 100 }}
              alt="hotkey_logo.."
            ></img>
          </Link>
          <h1>페이지가 존재하지 않습니다.</h1>
          <Link to="/search">검색페이지로 돌아가기</Link>
        </div>
      )}
    </>
  );
};

// fetch된 경우 결과 보여줄 Result Div => fixed-height // Wrapper
const Resultdiv = styled.div`
  display: flex;
  margin-top: 9.5vh; //헤더크기(+0.5vh)만큼 margin주기
  height: 2500px; //고정 픽셀값 (결과값은 크기가 작아지면 안될듯)
  width: 100vw; //유동 픽셀값 (추후 테스트 거쳐서 레이아웃 수정)
  justify-content: center;
`;
const ResultWrapper = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 90%;
  margin-right: 2%; //시각적으로 센터에 맞게 수정
  align-items: center;
  justify-content: space-around;
  background-color: grey;
`;
//1페이지
const Page1 = styled.div`
  display: flex;
  height: 48%;
  width: 100%;
  background-color: tomato;
  justify-content: space-around;
  align-items: center;
`;
//1페이지의 왼쪽
const Page11 = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 95%;
  width: 42%;
  background-color: maroon;
  align-items: center;
`;
//1페이지 왼쪽의 위
const Page111 = styled.div`
  display: flex;
  width: 90%;
  height: 35%;
  background-color: black;
`;
//1페이지 왼쪽의 아래
const Page112 = styled.div`
  display: flex;
  width: 90%;
  height: 57%;
  background-color: ivory;
`;
//1페이지의 오른쪽
const Page12 = styled.div`
  display: flex;
  flex-direction: column;
  height: 95%;
  width: 53%;
  background-color: red;
`;
//2페이지
const Page2 = styled.div`
  display: flex;
  height: 48%;
  width: 100%;
  background-color: tomato;
  justify-content: space-around;
  align-items: center;
`;
//2페이지의 왼쪽
const Page21 = styled.div`
  display: flex;
  flex-direction: column;
  height: 95%;
  width: 50%;
  background-color: red;
`;
//2페이지의 오른쪽
const Page22 = styled.div`
  display: flex;
  flex-direction: column;
  height: 95%;
  width: 45%;
  background-color: maroon;
`;
//1페

export default SearchResult;
