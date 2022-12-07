import React, { useState, useEffect } from "react";
import Footer from "../components/Footer";
import Header from "../components/Header";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import loading from "../images/loading.jpg";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import styled from "styled-components";

const SearchResult = () => {
  // *****매우 중요: 대소문자 구분없이, 띄어쓰기 되어서 들어오면 붙여서 백엔드로 보내야함!!!*********
  //키워드 잘 들어오는지 확인용
  const location = useLocation();
  const keyword = location.state?.keyword;
  const [result, setResult] = useState("");

  const [loading, setLoading] = useState(true); //로딩중인경우 true
  const [lstate, setLstate] = useState(0); //로딩중 단계 => lstate가 2에서 다 끝나면 setLoading(false) & setLstate(0)
  //분기 : keyword가 존재하는 경우 => loading이 있는가? -> lstate에 따라 분기. (3항 연산자 중첩 사용하거나? 어떻게 할지 생각..ㅇㅇ 최대한 state안꼬이게)

  console.log("keyword : " + keyword);
  //keyword와 enforce에 맞게 적절하게 실행

  useEffect(() => {
    if (keyword) {
      //여기서 fetch 실행 (keyword가 전달된 경우)
      // fetch("/manage/test/keyword_search/" + keyword) //without enforcing... for test
      // .then((res) => res.json())
      // .then((data) => {
      //   setResult(data);
      //   console.log("받아온 stringify된 corpus", data);
      // });
      console.log("/manage/test/keyword_search/" + keyword);
      console.log("result : ", result);
    }
  }, []); //한번만 실행되네요~

  if (!keyword)
    return (
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
    );
  else {
    //여기서 로딩중/ 검색결과로 나누기!! (로딩중인 경우 Header에 loading == True 넘겨줘야함!!)
    return (
      <div>
        <Header loading={true} />
        <Wrapper>
          {result.length === 0 ? ( //result가 아직 로딩중인 경우 => 로딩 중 구현
            <Loadingdiv></Loadingdiv>
          ) : (
            //result가 fetch (update)된 경우 => 결과 구현
            <Resultdiv></Resultdiv>
          )}
        </Wrapper>
        <Footer />
      </div>
    );
  }
};
//실제 결과가 들어갈 div
const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 9.5vh; //헤더크기(+0.5vh)만큼 margin주기
`;
// fetch된 경우 결과 보여줄 Result Div => min-height 속성
const Resultdiv = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 800px; //고정 픽셀값 (결과값은 크기가 작아지면 안될듯)
  width: 100vw; //유동 픽셀값 (추후 테스트 거쳐서 레이아웃 수정)
  align-items: center;
  background-color: ivory;
`;
// fetch되지 않은 경우, 로딩 Div => 반응형
const Loadingdiv = styled.div``;

export default SearchResult;
