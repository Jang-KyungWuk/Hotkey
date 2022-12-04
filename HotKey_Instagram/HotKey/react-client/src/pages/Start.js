import React from "react";
import HotKey_Logo from "../images/HotKey_Logo.jpg";
import Ripple from "../components/Ripple";

const Start = () => {
  return (
    <div className="App">
      <img src={HotKey_Logo} style={styles.image} alt="hotkey_logo.."></img>
      <h1 style={styles.h1}>Is your Keyword Hot ?</h1>
      <button
        style={styles.button}
        onClick={() => {
          console.log("키워드 검색 페이지로 이동");
          window.location.href = "/search_input";
        }}
      >
        SEARCH YOUR KEYWORD
        <Ripple color={"#FF6D28"} duration={1500} />
      </button>
    </div>
  );
};
const styles = {
  button: {
    position: "relative",
    cursor: "pointer",
    backgroundColor: "#CE3909",
    width: 800,
    height: 125,
    borderWidth: 4,
    borderRadius: 8,
    fontFamily: "Roboto",
    fontSize: 50,
    color: "white",
    letterSpacing: 3,
    marginTop: 200,
    display: "block",
    marginLeft: "auto",
    marginRight: "auto",
  },
  h1: {
    fontFamily: "Roboto",
    fontSize: 120,
    fontWeight: "bold",
    textAlign: "center",
  },
  image: {
    display: "block",
    marginTop: 150,
    marginLeft: "auto",
    marginRight: "auto",
    marginBottom: 150,
    width: 300,
    height: 100,
  },
};
export default Start;
