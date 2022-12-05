import React, { useState } from "react";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import Footer from "../components/Footer";
import { useNavigate } from "react-router-dom";

const SearchInput = () => {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();
  return (
    <div>
      <div style={{ height: "700px" }}>
        <img src={HotKey_Logo} style={styles.image} alt="hotkey_logo.."></img>
        <div>
          {/*여기서 검색창기능 구현!! (검색라인, 버튼, 트렌드 워드, 백그라운드 컬러..)*/}
          <input
            placeholder="검색할 해시태그를 입력하세요"
            type="search"
            maxLength="20"
            onChange={(e) => {
              setQuery(e.target.value);
            }}
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                navigate("/search_result", { state: { keyword: query } });
              }
            }}
            style={styles.input}
          ></input>
          {query.length === 0 ? (
            <button
              style={styles.button}
              onClick={() => {
                alert("검색어를 한 글자 이상 입력하세요");
              }}
            >
              검색
            </button>
          ) : (
            <button
              style={styles.button}
              onClick={() => {
                console.log("검색결과 페이지로 이동");
                navigate("/search_result", { state: { keyword: query } });
              }}
            >
              검색
            </button>
          )}
          <h1 style={{ textAlign: "center" }}>
            검색칸 밑에서 트렌드키워드 추천!{"\n"}trend1, trend2, trend3, ...
          </h1>
        </div>
      </div>
      <Footer />
    </div>
  );
};
const styles = {
  image: {
    display: "block",
    marginTop: 100,
    marginLeft: "auto",
    marginRight: "auto",
    marginBottom: 150,
    width: 300,
    height: 100,
  },
  input: {
    height: 70,
    width: "50%",
    fontSize: 30,
    textAlign: "left",
    marginLeft: 450,
    borderWidth: 3,
    borderRadius: 8,
  },
  button: {
    backgroundColor: "ivory",
    cursor: "pointer",
    height: 60,
    width: 90,
    fontSize: 30,
    borderWidth: 3,
    borderRadius: 8,
    marginLeft: 20,
  },
};
export default SearchInput;
