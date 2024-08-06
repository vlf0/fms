import React from "react";
import Header from "../Header";
import ParserService from "./services/FirstService";
import { Container, Row, Col } from "react-bootstrap";


const ServicesSection = () => {
  return (
    <>
    <header className="main-page-header">
      <Header headerText={"Welcome to fastapi service"}/>
    </header>
    <div className="main-page">

      <Container className="services-panel">

        <Row>
          <Col>
            <ParserService />
          </Col>
          <Col>
            <ParserService />
          </Col>
        </Row>

        <Row>
          <Col>
            <ParserService />
          </Col>
          <Col>
            <ParserService />
          </Col>
        </Row>

      </Container>

    {/* <div class="container text-center">
      <div class="row">
        <div class="col">
          Column
        </div>
        <div class="col">
          Column
        </div>
      </div>
      <div class="row">
        <div class="col">
          Column
        </div>
        <div class="col">
          Column
        </div>
      </div>
    </div> */}

    </div>
    </>
  );
};

export default ServicesSection;
