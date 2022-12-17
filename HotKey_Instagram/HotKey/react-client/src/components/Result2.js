import React from "react";
import styled from "styled-components";
import Page21 from "../images/Page21.png";
import Page22 from "../images/Page22.png";

const Result2 = ({ keyword, topic_num, topic_list }) => {
  return (
    <Wrapper>
      <Left>
        <Left1 url={require("../images/Page21.png")}>
          <H1>{keyword}</H1>
        </Left1>
        <Left2>
          <P1>
            <span style={{ fontSize: "calc(0.7vw + 0.7vh)" }}>
              #사람들의 #생각이 #궁금할 때
            </span>
            <br />
            핫키는 sns의 이야기로
            <br /> 세상을 이해합니다
          </P1>
          <img src={Page22} style={{ width: "90%" }} alt={"마이크"}></img>
        </Left2>
      </Left>
      <Mid>
        <Mid1>
          <p>
            지금 이 시간,
            <br />
            사람들이 같이 주목하는
            <br />
            키워드 리스트
          </p>
        </Mid1>
        <Mid2>
          <BarImg
            src={require("../visualization/barplot/" + keyword + ".png")}
            onClick={() => {
              window.open(
                require("../visualization/barplot/" + keyword + ".png")
              );
            }}
          />
        </Mid2>
      </Mid>
      <Right>
        <Right1>
          <p>
            지금 이 시간,
            <br />
            핫키 에디터가 나눈 토픽 분류별 모음
            <br />
            <span style={{ fontSize: "calc(0.65vw + 0.65vh)" }}>
              *키워드를 기반으로 숨겨진 주제를 찾아놓았습니다.
            </span>
          </p>
        </Right1>
        <Right2>
          {" "}
          <Page2232>
            {topic_num === 2 ? (
              <>
                <Grid style={{ border: "0px outset" }}>
                  <GridImg
                    style={{ height: "45%", width: "55%" }}
                    src={process.env.PUBLIC_URL + "/searching.png"}
                  ></GridImg>
                </Grid>
                <Grid style={{ border: "0px outset" }}>
                  "두 개의 토픽으로 최적화 됩니다"
                </Grid>
                <Grid>
                  <GridImg
                    src={require("../visualization/lda_results/" +
                      topic_list[0] +
                      ".png")}
                    onClick={() => {
                      window.open(
                        require("../visualization/lda_results/" +
                          topic_list[0] +
                          ".png")
                      );
                    }}
                  ></GridImg>
                </Grid>
                <Grid>
                  <GridImg
                    src={require("../visualization/lda_results/" +
                      topic_list[1] +
                      ".png")}
                    onClick={() => {
                      window.open(
                        require("../visualization/lda_results/" +
                          topic_list[1] +
                          ".png")
                      );
                    }}
                  ></GridImg>
                </Grid>
              </>
            ) : (
              <>
                <Grid>
                  <GridImg
                    src={require("../visualization/lda_results/" +
                      topic_list[0] +
                      ".png")}
                    onClick={() => {
                      window.open(
                        require("../visualization/lda_results/" +
                          topic_list[0] +
                          ".png")
                      );
                    }}
                  ></GridImg>
                </Grid>
                <Grid>
                  <GridImg
                    src={require("../visualization/lda_results/" +
                      topic_list[1] +
                      ".png")}
                    onClick={() => {
                      window.open(
                        require("../visualization/lda_results/" +
                          topic_list[1] +
                          ".png")
                      );
                    }}
                  ></GridImg>
                </Grid>
                <Grid>
                  <GridImg
                    src={require("../visualization/lda_results/" +
                      topic_list[2] +
                      ".png")}
                    onClick={() => {
                      window.open(
                        require("../visualization/lda_results/" +
                          topic_list[2] +
                          ".png")
                      );
                    }}
                  ></GridImg>
                </Grid>
                <Grid>
                  <GridImg
                    src={require("../visualization/lda_results/" +
                      topic_list[3] +
                      ".png")}
                    onClick={() => {
                      window.open(
                        require("../visualization/lda_results/" +
                          topic_list[3] +
                          ".png")
                      );
                    }}
                  ></GridImg>
                </Grid>
              </>
            )}
          </Page2232>
        </Right2>
      </Right>
    </Wrapper>
  );
};

const Wrapper = styled.div`
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 92%;
  height: 97%;
`;
const Left = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  height: 100%;
  width: 25%;
`;
const Left1 = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80%;
  height: 60%;
  background-image: url(${(prop) => prop.url});
  background-size: cover;
`;
const H1 = styled.p`
  margin-top: 15%;
  font-family: chosun;
  font-size: calc(2.3vw + 2.3vh);
  writing-mode: vertical-rl;
  letter-spacing: 1vh;
`;
//텍스트+이미지
const Left2 = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 95%;
  height: 40%;
`;
const P1 = styled.div`
  margin-top: 2%;
  font-size: calc(1vw + 1vh);
  font-family: chosun;
  line-height: 100%;
  text-align: center;
`;

const Mid = styled.div`
  display: flex;
  flex-direction: column;
  justify-contents: space-around;
  height: 92%;
  width: 22%;
`;
const Mid1 = styled.div`
  display: flex;
  margin-top: 5%;
  margin-left: 5%;
  width: 95%;
  height: 20%;
  font-size: calc(0.8vw + 0.8vh);
  font-family: chosun;
  line-height: 130%;
`;
const Mid2 = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80%;
  border: 1px outset;
  border-radius: 20px;
  &:hover {
    border: 0px outset;
    border-radius: 20px;
  }
`;
//barplot전용 이미지
const BarImg = styled.img`
  display: block;
  height: 100%;
  cursor: pointer;
  &:hover {
    transform: scale(1.15);
    border: 1px outset;
    border-radius: 20px;
  }
  transition: all 0.2s ease-out;
`;
const Right = styled.div`
  height: 90%;
  width: 45%;
`;
const Right1 = styled.div`
  margin-right: 5%;
  margin-top: 5%;
  height: 15%;
  text-align: right;
  font-family: chosun;
  font-size: calc(0.95vw + 0.95vh);
  line-height: 130%;
`;
const Right2 = styled.div`
  height: 80%;
  width: 100%;
`;
//Page223의 아래 (토픽모델링 워드클라우드)
const Page2232 = styled.div`
  margin: auto;
  height: 100%;
  width: 95%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  grid-row-gap: 2%;
  grid-column-gap: 2%;
  padding: 1%;
`;
//그리드 자식 컴포넌트
const Grid = styled.div`
  height: 100%;
  width: 100%;
  border: 1px outset;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: chosun;
  font-size: 1.2vw;
  text-align: center;
  &:hover {
    transform: scale(1.2);
  }
  transition: all 0.2s ease-out;
`;
const GridImg = styled.img`
  width: 100%;
  cursor: pointer;
`;
export default Result2;
