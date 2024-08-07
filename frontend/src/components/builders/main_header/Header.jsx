import React from "react";
import { Button } from "react-bootstrap";
import "./common_styles/CommonStyles.css";


const Header = ({ headerText }) => {
    return (
      <>
      <Button className="logout-button" as="input" type="button" value="Log Out"/>{' '}
      <div className="main-header-block">
        <h2 className="header-text">
          {headerText}
        </h2>
      </div>
      </>
    )  
};

export default Header;