import React, { useState, useEffect } from "react";
import Footer from "../components/Footer";
import Header from "../components/Header";
import { useLocation, useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import Loading from "../images/Loading.gif";
import Loading1 from "../components/Loading1";
import Loading2 from "../components/Loading2";
import Loading3 from "../components/Loading3";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import styled from "styled-components";

const SearchFetch = () => {
  const location = useLocation();
  const keyword = location.state?.keyword;

  const [lstate, setLstate] = useState(0); //로딩중 단계
  const navigate = useNavigate();
  useEffect(() => {
    if (keyword) {
      setLstate(0);
      // fetch(
      //   "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/keyword_search/" +
      //     keyword.toLowerCase()
      // )
      fetch(
        "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/manage/t_search/" +
          keyword.toLowerCase()
      )
        .then((res) => res.json())
        .then((data) => {
          console.log("keyword_search response : ", data);
          if (data.status) {
            //키워드 corpus가 정상적으로 생성된 경우
            setLstate(1);
            fetch(
              "http://ec2-13-209-21-117.ap-northeast-2.compute.amazonaws.com:5000/analyze/" +
                data.tid
            )
              .then((res2) => res2.json())
              .then((data2) => {
                console.log("analyze response : ", data2);
                if (data2.get_image) {
                  setLstate(2);
                  setTimeout(() => {
                    setLstate(0);
                    navigate("/search_result", {
                      state: {
                        key_word: keyword,
                        image_num: data2.imagenum,
                        topic_num: data2.topic_num,
                        sent_result: data2.sent_result,
                        status: data2.status,
                      },
                    });
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
  }, [keyword]);

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
        <Link to="/">검색페이지로 돌아가기</Link>
      </div>
    );
  //분기 : keyword가 존재하는 경우 => loading이 있는가? -> lstate에 따라 분기. (3항 연산자 중첩 사용하거나? 어떻게 할지 생각..ㅇㅇ 최대한 state안꼬이게)
  else {
    return (
      <>
        <Header loading={true} />
        <Wrapper>
          <Loadingdiv>
            <Load1>
              {lstate === 0 ? (
                <Loading1 />
              ) : (
                <>{lstate === 1 ? <Loading2 /> : <Loading3 />}</>
              )}
            </Load1>
            <Load2>
              <Img src={Loading} />
            </Load2>
          </Loadingdiv>
        </Wrapper>
        <Footer />
      </>
    );
  }
};
//로딩인경우 wrapper
const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 7vh; //헤더크기(+0.5vh)만큼 margin주기
`;

// fetch되지 않은 경우, 로딩 Div => 반응형
const Loadingdiv = styled.div`
  display: flex;
  justify-content: space-around;
  width: 100vw;
  height: 85.5vh;
`;
//progress bar가 들어갈 div
const Load1 = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 90%;
  width: 50%;
`;
//loading div2 => 분석중 이미지가 들어갈 div
const Load2 = styled.div`
  height: 100%;
  width: 40%;
  display: flex;
  justify-content: center;
  align-items: center;
`;
//이미지
const Img = styled.img`
  height: 70%;
`;

export default SearchFetch;
