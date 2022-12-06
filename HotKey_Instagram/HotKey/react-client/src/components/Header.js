import React from "react";

const Header = () => {
  return (
    <div
      style={{
        backgroundColor: "beige",
        height: "100px",
        width: "100%",
        borderBottom: "2px solid teal",
        textAlign: "center",
        // 수직정렬하는법 ㅠㅠ
      }}
    >
      <h1 style={{ textAlign: "center", lineHeight: "100px" }}>
        Header입니다. 구현 예정...
      </h1>
    </div>
  );
};

export default Header;
