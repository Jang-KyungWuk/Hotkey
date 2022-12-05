import React, { useState, useEffect } from "react";
import Footer from "../components/Footer";
import Header from "../components/Header";
import { useLocation } from "react-router-dom";

const SearchResult = () => {
  //키워드 잘 들어오는지 확인용
  const location = useLocation();
  const { keyword } = location.state;
  useEffect(() => {
    console.log(keyword);
  }, []);
  return (
    <div>
      <Header />
      <div>
        <h1 style={{ textAlign: "center" }}>검색결과 여기서 구현...</h1>
      </div>
      <Footer />
    </div>
  );
};
export default SearchResult;
