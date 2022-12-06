import React, { useState, useEffect } from "react";
import Footer from "../components/Footer";
import Header from "../components/Header";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import HotKey_Logo from "../images/HotKey_Logo.jpg";

const SearchResult = () => {
  // *****매우 중요: 대소문자 구분없이, 띄어쓰기 되어서 들어오면 붙여서 백엔드로 보내야함!!!*********
  //키워드 잘 들어오는지 확인용
  const location = useLocation();
  const keyword = location.state?.keyword;
  const [result, setResult] = useState("");

  console.log("keyword : " + keyword);
  //keyword와 enforce에 맞게 적절하게 실행

  useEffect(() => {
    if (keyword) {
      // fetch("/manage/test/keyword_search/" + keyword) //without enforcing... for test
      // .then((res) => res.json())
      // .then((data) => {
      //   setResult(data);
      //   console.log("받아온 stringify된 corpus", data);
      // });
      console.log("/manage/test/keyword_search/" + keyword);
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
        <Link to="/search">검색페이지로 이동</Link>
      </div>
    );
  else {
    //여기서 로딩중/ 검색결과로 나누기!!
    return (
      <div>
        <Header />
        <div style={{ height: "1500px" }}>
          <h1 style={{ textAlign: "center" }}>검색결과 여기서 구현...</h1>
          <h6>{result}</h6>
        </div>
        <Footer />
      </div>
    );
  }
};
export default SearchResult;
