import React from "react";
import { Container, Row, Col, Navbar } from "react-bootstrap";
import "../styles/MainFooterStyles.css";


const MainFooter = () => {
  return (
    <Navbar className="footer mt-auto py-3">
      <Container>
        <Row className="w-100">
          <Col md={4} className="text-center text-md-left">
            <p className="mb-0">© 2024 Your Company</p>
          </Col>
          <Col md={4} className="text-center">
            <p className="mb-0">Privacy Policy</p>
          </Col>
          <Col md={4} className="text-center text-md-right">
            <p className="mb-0">Follow us on: <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">Twitter</a></p>
          </Col>
        </Row>
      </Container>
    </Navbar>
  );
};

export default MainFooter;
