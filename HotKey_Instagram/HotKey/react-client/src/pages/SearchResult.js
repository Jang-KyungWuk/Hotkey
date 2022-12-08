import React, { useState, useEffect } from "react";
import Footer from "../components/Footer";
import Header from "../components/Header";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import Loading from "../images/Loading.jpg";
import Loading1 from "../components/Loading1";
import Loading2 from "../components/Loading2";
import Loading3 from "../components/Loading3";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import styled from "styled-components";

const SearchResult = () => {
  // *****매우 중요: 대소문자 구분없이, 띄어쓰기 되어서 들어오면 붙여서 백엔드로 보내야함!!!*********
  //키워드 잘 들어오는지 확인용
  const location = useLocation();
  const keyword = location.state?.keyword;

  const [loading, setLoading] = useState(true); //로딩중인경우 true
  const [lstate, setLstate] = useState(0); //로딩중 단계 => lstate가 2에서 다 끝나면 setLoading(false) & setLstate(0)
  //분기 : keyword가 존재하는 경우 => loading이 있는가? -> lstate에 따라 분기. (3항 연산자 중첩 사용하거나? 어떻게 할지 생각..ㅇㅇ 최대한 state안꼬이게)

  console.log("검색결과 페이지=> keyword : " + keyword);
  //keyword와 enforce에 맞게 적절하게 실행

  useEffect(() => {
    console.log("useeffect실행");
    if (keyword) {
      setLstate(0); //react-router-dom 이슈인지,, 위의  useState가 검색어가 바뀌어도 따로 바뀌지 않아서 ㅇㅇ, 검색어가바뀔떄 useeffect가 실행
      setLoading(true);
      console.log("/keyword_search/" + keyword + "(으)로 request");
      fetch("/keyword_search/" + keyword)
        .then((res) => res.json())
        .then((data) => {
          console.log("keyword_search API 서버 응답");
          console.log(data.status, data.tid);
          if (data.status) {
            //키워드 corpus가 정상적으로 생성된 경우! (서버 응답 True)
            setLstate(1);
            //이후에 서버 API로 분석요청!! => data.tid사용!!
            console.log("analyze/" + data.tid + "(으)로 request");
            fetch("/analyze/" + data.tid)
              .then((res) => res.json())
              .then((data) => {
                console.log("analyze API 서버 응답");
                console.log(data.status, data.result);
                if (data.status) {
                  // 분석 결고 ㅏ데이터도 잘 받아온 경우
                  setLstate(2);
                  setTimeout(() => {
                    setLoading(false); //로딩 풀기
                    setLstate(0);
                  }, 2000);
                } else {
                  //분석 결과 데이터를 잘 못받아 온경우 (서버 으답이 False인경우)
                  alert(
                    "서버로부터의 응답이 원활하지 않습니다..\n다른 키워드를 검색해보거나 잠시 후에 다시 시도해주세요"
                  );
                }
              });
            //이후에도 분석이 완료된경우 분석결과를 받아서 보여주는 컴포넌트에 전달해주기(구현 예정)
          } else {
            //서버 응답이 False인경우 => crawling 데이터를 잘 못받아 온경우
            alert(
              "서버로부터의 응답이 원활하지 않습니다..\n다른 키워드를 검색해보거나 잠시 후에 다시 시도해주세요"
            );
            //lState가 3인경우 만들어서 서버로부터 왜 제대로 못받아왔는지 보여주는 컴포넌트? (구현 예정)
          }
        })
        .catch((err) => {
          console.log(err);
          alert(err);
        });
    }
  }, [keyword]); //한번만 실행되네요~

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
  //분기 : keyword가 존재하는 경우 => loading이 있는가? -> lstate에 따라 분기. (3항 연산자 중첩 사용하거나? 어떻게 할지 생각..ㅇㅇ 최대한 state안꼬이게)
  else if (loading) {
    //여기서 로딩중/ 검색결과로 나누기!! (로딩중인 경우 Header에 loading == True 넘겨줘야함!!)
    if (lstate === 0)
      return (
        <div>
          <Header />
          <Wrapper>
            <Loadingdiv>
              <Loading1 />
              <Load2>
                <Img src={Loading}></Img>
              </Load2>
            </Loadingdiv>
          </Wrapper>
          <Footer />
        </div>
      );
    else if (lstate === 1)
      return (
        <div>
          <Header />
          <Wrapper>
            <Loadingdiv>
              <Loading2 />
              <Load2>
                <Img src={Loading}></Img>
              </Load2>
            </Loadingdiv>
          </Wrapper>
          <Footer />
        </div>
      );
    //lstate가 2인경우
    else
      return (
        <div>
          <Header />
          <Wrapper>
            <Loadingdiv>
              <Loading3 />
              <Load2>
                <Img src={Loading}></Img>
              </Load2>
            </Loadingdiv>
          </Wrapper>
          <Footer />
        </div>
      );
  } else {
    //넘어온 keyword가 있고 loading중도 아닌경우 => result보여주기
    return (
      <div>
        <Header loading={false}></Header>
        <Wrapper2>
          <Resultdiv>
            <h5>결과는 여기서 구현...</h5>
          </Resultdiv>
        </Wrapper2>
      </div>
    );
  }
};
//로딩인경우 wrapper
const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 6vh; //헤더크기(+0.5vh)만큼 margin주기
`;
//실제 결과가 들어갈 Wrapper
const Wrapper2 = styled.div`
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
  background-color: maroon;
`;
// fetch되지 않은 경우, 로딩 Div => 반응형
const Loadingdiv = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 2vh;
  width: 100vw;
  height: 80vh;
`;
//loading div2 => 분석중 이미지가 들어갈 div
const Load2 = styled.div`
  display: flex;
  margin-left: 20%;
  align-items: center;
  width: 100%;
  height: 60%;
`;
//이미지
const Img = styled.img`
  height: 70%;
  border: 0px solid;
`;

export default SearchResult;
