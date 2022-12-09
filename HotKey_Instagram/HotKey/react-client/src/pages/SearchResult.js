import React, { useState, useEffect } from "react";
import Footer from "../components/Footer";
import Header from "../components/Header";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import loading from "../images/loading.jpg";
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
  // const [keyword, setKeyword] = useState(location.state?.keyword);

  const [load, setLoad] = useState(true); //로딩중인경우 true
  const [lstate, setLstate] = useState(0); //로딩중 단계 => lstate가 2에서 다 끝나면 setLoading(false) & setLstate(0)
  const [images, setImages] = useState([]);
  //분기 : keyword가 존재하는 경우 => loading이 있는가? -> lstate에 따라 분기. (3항 연산자 중첩 사용하거나? 어떻게 할지 생각..ㅇㅇ 최대한 state안꼬이게)
  console.log("렌더링, keyword : " + keyword);

  useEffect(() => {
    console.log("useeffect실행");
    if (keyword) {
      // setLstate(0); //react-router-dom 이슈인지,, 위의  useState가 검색어가 바뀌어도 따로 바뀌지 않아서 ㅇㅇ, 검색어가바뀔떄 useeffect가 실행
      // setLoad(true);
      // console.log("/keyword_search/" + keyword + "(으)로 request");
      fetch("/keyword_search/" + keyword)
        .then((res) => res.json())
        .then((data) => {
          console.log("keyword_search 응답 : ", data);
          if (data.status) {
            //키워드 corpus가 정상적으로 생성된 경우! (서버 응답 True)
            setLstate(1);
            //   //이후에 서버 API로 분석요청!! => data.tid사용!!
            // console.log("analyze/" + data.tid + "(으)로 request");
            fetch("/analyze/" + data.tid)
              .then((res2) => res2.json())
              .then((data2) => {
                console.log("analyze 응답 : ", data2);
                if (data2.status) {
                  setLstate(2);
                  setImages(data2.images);
                  setTimeout(() => {
                    setLoad(false); //로딩 풀기 -> 결과창이동
                    setLstate(0);
                  }, 2000);
                } else
                  alert(
                    "분석결과를 서버로부터 받아오는 중 에러가 발생했습니다.\n다른 키워드를 검색해보거나 잠시 후에 다시 시도해주세요"
                  );
              })
              .catch((err) => {
                alert("analyze API 에러 :", err);
              });
          }
        })
        .catch((err) => {
          alert("keyword search 에러 :", err);
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
  else if (load) {
    //여기서 로딩중/ 검색결과로 나누기!! (로딩중인 경우 Header에 loading == True 넘겨줘야함!!)
    if (lstate === 0)
      return (
        <div>
          <Header loading={true} />
          <Wrapper>
            <Loadingdiv>
              <Loading1 />
              <Load2>
                <Img src={loading}></Img>
              </Load2>
            </Loadingdiv>
          </Wrapper>
          <Footer />
        </div>
      );
    else if (lstate === 1)
      return (
        <div>
          <Header loading={true} />
          <Wrapper>
            <Loadingdiv>
              <Loading2 />
              <Load2>
                <Img src={loading}></Img>
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
          <Header loading={true} />
          <Wrapper>
            <Loadingdiv>
              <Loading3 />
              <Load2>
                <Img src={loading}></Img>
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
            <h5>결과창 구현예정</h5>
            {images.map((file) => (
              <img
                src={require("../top_imgs/" + file)}
                style={{ height: "300px" }}
                alt="임시"
              ></img>
            ))}
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
  margin-left: 20vw;
  align-items: center;
  width: 100vw;
  height: 60%;
`;
//이미지
const Img = styled.img`
  height: 70%;
  border: 0px solid;
`;

export default SearchResult;
