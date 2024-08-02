import React from "react";
import "./common_styles/CommonStyles.css";


const Header = ({ headerText }) => {
    return (
      <div className="main-header-block">
        <h2 className="header-text">
          {headerText}
        </h2>
      </div>
    )  
};

export default Header;