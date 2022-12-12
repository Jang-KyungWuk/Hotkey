import React from "react";
import styled from "styled-components";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import Footer from "../components/Footer";
import Header from "../components/Header";
import Imagegrid from "../components/Imagegrid";

const SearchResult = () => {
  const location = useLocation();
  //   const navigate = useNavigate();
  const key_word = location.state?.key_word;
  const image_num = location.state?.image_num;
  let image_list = [
    "dddefault0",
    "dddefault1",
    "dddefault2",
    "dddefault3",
    "dddefault4",
    "dddefault5",
    "dddefault6",
    "dddefault7",
    "dddefault8",
  ];
  for (let i = 0; i < image_num; i++) {
    image_list[i] = key_word + i + ".jpg";
  }

  console.log("분석 결과 페이지 렌더링...");
  console.log("image_list :", image_list);
  console.log("key_word :", key_word);
  return (
    <Div>
      {location.state ? (
        <div>
          <Header loading={false} />
          <Wrapper>
            <Resultdiv>
              <ResultWrapper>
                <Page1>
                  <Page11>
                    <Page111>
                      <h3>{"< 이미지1, 이미지2 >"}</h3>
                    </Page111>
                    <Page112>
                      {image_list.map((file) => (
                        <Imagegrid key={file} image={file} />
                      ))}
                    </Page112>
                  </Page11>
                  <Page12>
                    <Page121>
                      <h3>{"< 워드클라우드 >"}</h3>
                    </Page121>
                    <Page122>
                      <h3>{"< 토픽별 워드클라우드 >"}</h3>
                    </Page122>
                  </Page12>
                </Page1>
                <Page2>
                  <Page21></Page21>
                  <Page22></Page22>
                </Page2>
              </ResultWrapper>
            </Resultdiv>
          </Wrapper>
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
    </Div>
  );
};
const Div = styled.div`
  height: 1700px;
  width: 1900px;
  display: flex;
  justify-content: center;
  background-color: #edf0f5;
`;
const Wrapper = styled.div`
  display: flex;
  margin-top: 8vh; //헤더크기(+0.1vh)만큼 margin주기
  justify-content: center;
`;
// fetch된 경우 결과 보여줄 Result Div => fixed-height // Wrapper
const Resultdiv = styled.div`
  display: flex;
  margin-left: 2%;
  height: 100%; //고정 픽셀값 (결과값은 크기가 작아지면 안될듯)
  width: 90%; //유동 픽셀값 (추후 테스트 거쳐서 레이아웃 수정)
  justify-content: center;
`;
const ResultWrapper = styled.div`
  display: flex;
  flex-direction: column;
  height: 1600px;
  width: 1800px;
  margin-right: 25px; //시각적으로 센터에 맞게 수정
  align-items: center;
  //background-color: grey;
`;
//1페이지
const Page1 = styled.div`
  display: flex;
  height: 50%;
  width: 100%;
  //background-color: tomato;
  justify-content: space-around;
  align-items: center;
`;
//1페이지의 왼쪽
const Page11 = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  height: 100%;
  width: 46%;
  //background-color: maroon;
  align-items: center;
`;
//1페이지 왼쪽의 위
const Page111 = styled.div`
  margin-top: 35px;
  display: flex;
  width: 630px;
  height: 180px;
  background-color: #edf0f5;
  justify-content: center;
  align-items: center;
`;
//1페이지 왼쪽의 아래
const Page112 = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr 1fr;
  margin-top: 1px;
  width: 550px;
  height: 550px;
  background-color: white;
  border-radius: 25px;
  padding: 1px;
`;
//1페이지의 오른쪽
const Page12 = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 94%;
  width: 50%;
  //background-color: red;
`;
//1페이지의 오른쪽 위
const Page121 = styled.div`
  display: flex;
  height: 49%;
  width: 100%;
  background-color: white;
  border-radius: 15px;
  justify-content: center;
  align-items: center;
`;
//1페이지의 오른쪽 아래
const Page122 = styled.div`
  display: flex;
  margin-top: 2%;
  height: 47%;
  width: 100%;
  background-color: white;
  border-radius: 15px;
  justify-content: center;
  align-items: center;
`;
//2페이지
const Page2 = styled.div`
  display: flex;
  height: 50%;
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
