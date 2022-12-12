import React from "react";
import { Route, Routes, useLocation } from "react-router-dom";
import Start from "./Start.js";
import SearchInput from "./SearchInput.js";
import SearchFetch from "./SearchFetch.js";
import SearchResult from "./SearchResult.js";
import Test from "./Test.js";
import Test2 from "./Test2.js";
import Info from "./Info.js";
import { AnimatePresence } from "framer-motion";

const AnimatedRoutes = () => {
  const location = useLocation();
  return (
    <AnimatePresence>
      <Routes location={location} key={location.pathname}>
        <Route exact path="/" element={<Start />}></Route>
        {/*키워드 입력하는 페이지*/}
        <Route exact path="/search" element={<SearchInput />}></Route>
        {/*키워드 입력 후 서버 요청 페이지*/}
        <Route exact path="/search_fetch" element={<SearchFetch />}></Route>
        {/*분석 결과 보여주는 페이지 */}
        <Route exact path="/search_result" element={<SearchResult />}></Route>
        {/*핫키 사용법 클릭시 이동*/}
        <Route exact path="/info" element={<Info />}></Route>
        {/*테스트용 페이지, 개발 완료 시 삭제 */}
        <Route exact path="/test" element={<Test />}></Route>
        {/*테스트용 페이지, 개발 완료 시 삭제 */}
        <Route exact path="/test2" element={<Test2 />}></Route>
      </Routes>
    </AnimatePresence>
  );
};

export default AnimatedRoutes;
