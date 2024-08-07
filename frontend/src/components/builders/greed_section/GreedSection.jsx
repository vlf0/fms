import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import ParserService from "../services/ParserService";


const GreedSection = () => {

  return (
    <Container className="mt-4">
        <Row style={{textAlign: 'center' }}>
          <Col>
            <ParserService />
          </Col>
          <Col>
            Not Awailable
          </Col>
        </Row>
    </Container>
  )
};

export default GreedSection;
