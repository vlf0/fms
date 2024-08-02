import React from "react";
import Header from "../Header";
import ParserService from "./services/FirstService";
// import '../styles/mainpage_styles.css'; 

const MainPage = () => {
  return (
    <div className="main-page">
      <header className="main-page-header">
        <Header headerText={"Welcome to fastapi service"}/>
      </header>
      <div className="parser">
        <ParserService />
      </div>

      {/* <main className="main-page-content">

        <section className="component-container">

          <div className="small-component">Component 1</div>
          <div className="small-component">Component 2</div>

        </section>
      </main> */}

    </div>
  );
};

export default MainPage;
