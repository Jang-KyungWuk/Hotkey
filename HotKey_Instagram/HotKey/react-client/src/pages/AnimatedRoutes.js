import React from "react";
import { Route, Routes, useLocation } from "react-router-dom";
import Home from "./Home.js";
import SearchFetch from "./SearchFetch.js";
import SearchResult from "./SearchResult.js";
import Info from "./Info.js";
import { AnimatePresence } from "framer-motion";
import { TransitionGroup, CSSTransition } from "react-transition-group";

const AnimatedRoutes = () => {
  const location = useLocation();
  const timeout = { enter: 800, exit: 400 }; //for CSS Transition
  return (
    <AnimatePresence>
      <TransitionGroup component="div" className="App">
        <CSSTransition
          timeout={timeout}
          classNames="pageSlider"
          mountOnEnter={false}
          unmountOnExit={true}
        >
          <Routes location={location} key={location.pathname}>
            {/*검색 페이지 (홈 화면)*/}
            <Route exact path="/" element={<Home />}></Route>
            {/*키워드 입력 후 서버 요청 페이지 (로딩 페이지)*/}
            <Route exact path="/fetch" element={<SearchFetch />}></Route>
            {/*분석 결과 보여주는 페이지 */}
            <Route
              exact
              path="/search_result"
              element={<SearchResult />}
            ></Route>
            {/*핫키 사용법 클릭시 이동할 페이지*/}
            <Route exact path="/info" element={<Info />}></Route>
          </Routes>
        </CSSTransition>
      </TransitionGroup>
    </AnimatePresence>
  );
};

export default AnimatedRoutes;
