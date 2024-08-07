import React from "react";
import { Container, Row, Col, Navbar } from "react-bootstrap";
import "../styles/MainFooterStyles.css";


const MainFooter = () => {
  return (
    <Navbar className="footer mt-auto py-3">
      <Container>
        <Row className="w-100">
          <Col sm={6} className="text-center">
            <p className="mb-0">© 2024 Your Company</p>
          </Col>
          <Col sm={6} className="text-center">
            <p className="mb-0">Privacy Policy</p>
          </Col>
          <Col sm={12} className="text-center">
            <p className="mb-0">Follow us on:</p>
              <a className="subscribe-links" href="https://x.com/dr_dnb2" target="_blank" rel="noopener noreferrer">
                X
              </a>
              <a className="subscribe-links" href="https://github.com/vlf0" target="_blank" rel="noopener noreferrer">
                GitHub
              </a> 
          </Col>
        </Row>
      </Container>
    </Navbar>
  );
};

export default MainFooter;
