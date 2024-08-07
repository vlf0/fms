import React from "react";
import { Navbar, Nav, NavDropdown, Container} from "react-bootstrap";
import AuthButton from "./AuthButton";
import "../styles/MainPageStyles.css";


const MainHeader = () => {

  return (
    <Navbar className="main-navbar">
      <Container>
        <Navbar.Brand>API Tools</Navbar.Brand>
        <Nav className="me-auto">
          <NavDropdown title="Dropdown" id="nav-dropdown">
            <NavDropdown.Item href="#action1">Action</NavDropdown.Item>
            <NavDropdown.Item href="#action2">Another action</NavDropdown.Item>
            <NavDropdown.Item href="#action3">Something else here</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item href="#separated">Separated link</NavDropdown.Item>
          </NavDropdown>
        </Nav>
        <AuthButton />
      </Container>
    </Navbar>
  );
};

export default MainHeader;
