import React, { useState } from 'react';
import { Navbar, Nav, NavDropdown, Container, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './MainPageStyles.css'; 

const MainPage = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleAuthButtonClick = () => {
    setIsAuthenticated(!isAuthenticated);
  };

  return (
    <div className="main-page">
      <Navbar>
        <Container>
          <Navbar.Brand href="#home">API Tools</Navbar.Brand>
          <Nav className="me-auto">
              <NavDropdown title="Dropdown" id="nav-dropdown">
                <NavDropdown.Item href="#action1">Action</NavDropdown.Item>
                <NavDropdown.Item href="#action2">Another action</NavDropdown.Item>
                <NavDropdown.Item href="#action3">Something else here</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item href="#separated">Separated link</NavDropdown.Item>
              </NavDropdown>
            </Nav>

          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              <Button
                variant="outline-light"
                onClick={handleAuthButtonClick}
                className="auth-button"
              >
                {isAuthenticated ? 'Logout' : 'Login'}
              </Button>
            </Nav>
          </Navbar.Collapse>

        </Container>
      </Navbar>
    </div>
  );
};

export default MainPage;
