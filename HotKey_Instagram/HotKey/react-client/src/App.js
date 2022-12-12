import React from "react";
import { BrowserRouter } from "react-router-dom";
import AnimatedRoutes from "./pages/AnimatedRoutes";
// import Start from "./pages/Start.js";
// import SearchInput from "./pages/SearchInput.js";
// import SearchFetch from "./pages/SearchFetch.js";
// import SearchResult from "./pages/SearchResult.js";
// import Test from "./pages/Test.js";
// import Test2 from "./pages/Test2.js";
// import Info from "./pages/Info.js";

function App() {
  return (
    <BrowserRouter>
      <AnimatedRoutes />
    </BrowserRouter>
  );
}

export default App;
