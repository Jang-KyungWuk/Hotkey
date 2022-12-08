import React, { useState, useEffect } from "react";
import Footer from "../components/Footer";

const Test = () => {
  //서버 fetch 테스트용...
  const [data, setData] = useState([{}]);
  useEffect(() => {
    fetch("/manage/accounts")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log("받아온 Account 객체", data);
      });

    fetch("/manage/test/test")
      .then((res) => res.blob())
      .then((blob) => {
        let blobUrl = URL.createObjectURL(blob);
        console.log(blobUrl);
        //URL.revokeObjectURL(blobUrl);
      });
  }, []);

  return (
    <div>
      <div style={{ height: 900 }}>
        <h1>테스트용 페이지...</h1>
        {/*밑에는 서버 fetch 테스트용...*/}
        <h2>네트워크 test</h2>
        <button
          onClick={() => {
            console.log("네트워크 팝업 구현");
            //중요 : json에서 proxy설정한 것은 리액트 자체에서 request할때만 작용하는 것으로보임, 아래처럼 서버에 직접 접근하려면 서버의 주소를 적어줘야한다.
            //팝업창 옵션 (창 크기 조절 등 조정)
            const popupOption = "width=1000, height=640, status=no;";
            window.open(
              "http://localhost:5000/manage/test/network/월드컵1203.html",
              "",
              popupOption
            );
          }}
          style={{ height: 100, width: 500, fontSize: 30, fontWeight: "bold" }}
        >
          네트워크 페이지로 이동! (팝업구현)
        </button>
        {typeof data.all_blocked === "undefined" ? (
          <h1>Loading...</h1>
        ) : (
          <span>
            <br />
            <h1>
              Account Data successfully fetched from server... (port:5000)
            </h1>
            <br />
            <h3>Account Data fetched : </h3>
            <h4>{JSON.stringify(data.total_acc_info)}</h4>
          </span>
        )}
      </div>
      <Footer />
    </div>
  );
};
export default Test;
