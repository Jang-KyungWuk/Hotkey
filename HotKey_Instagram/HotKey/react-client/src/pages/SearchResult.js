import React, { useState, useEffect } from "react";
import Footer from "../components/Footer";
import Header from "../components/Header";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";

const SearchResult = () => {
  //키워드 잘 들어오는지 확인용
  const location = useLocation();
  const keyword = location.state?.keyword;
  // useEffect(() => {
  //   console.log(keyword);
  // }, []);
  console.log(keyword);
  return (
    <div>
      {keyword ? (
        <div>
          <div>
            <Header />
            <h1 style={{ textAlign: "center" }}>검색결과 여기서 구현...</h1>
          </div>
          <Footer />
        </div>
      ) : (
        <div>
          <h1>페이지가 존재하지 않습니다.</h1>
          <Link to="/search_input">검색페이지로 이동</Link>
        </div>
      )}
    </div>
  );
};
export default SearchResult;
