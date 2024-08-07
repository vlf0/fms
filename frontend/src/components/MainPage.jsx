import React from "react";
import MainHeader from "./builders/main_header/MainHeader";
import GreedSection from "./builders/greed_section/GreedSection";
import MainFooter from "./builders/footer/MainFooter";


const MainPage = () => {
  return (
    <div className="main-page">
      <MainHeader />
      <GreedSection />
      <MainFooter />
    </div>
  );
};

export default MainPage;
