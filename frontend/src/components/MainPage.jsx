import React from "react";
import Header from "../Header";
import ServicesSection from "./s_menu/ServicesSection";


const MainPage = () => {
  return (
    <>
      <header className="main-page-header">
        <Header headerText={"Welcome to fastapi service"}/>
      </header>
      <ServicesSection />
    </>
  );
};

export default MainPage;
