import React from "react";
import { BrowserRouter } from "react-router-dom";
import AnimatedRoutes from "./pages/AnimatedRoutes";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <AnimatedRoutes />
    </BrowserRouter>
  );
}

export default App;
