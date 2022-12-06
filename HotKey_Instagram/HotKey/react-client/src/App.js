import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Start from "./pages/Start.js";
import SearchInput from "./pages/SearchInput.js";
import SearchResult from "./pages/SearchResult.js";
import Test from "./pages/Test.js";
import Test2 from "./pages/Test2.js";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<Start />}></Route>
        {/*키워드 입력하는 페이지*/}
        <Route exact path="/search" element={<SearchInput />}></Route>
        {/*키워드 입력 후 결과 페이지*/}
        <Route exact path="/search_result" element={<SearchResult />}></Route>
        {/*테스트용 페이지, 개발 완료 시 삭제 */}
        <Route exact path="/test" element={<Test />}></Route>
        {/*테스트용 페이지, 개발 완료 시 삭제 */}
        <Route exact path="/test2" element={<Test2 />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
