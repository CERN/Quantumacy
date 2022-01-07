import React from "react";
//import express from "components/express/index.js";
// nodejs library that concatenates classes
import classNames from "classnames";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
//import Camera from "@material-ui/icons/Camera";
//import Palette from "@material-ui/icons/Palette";
//import Favorite from "@material-ui/icons/Favorite";
// core components
import Header from "components/Header/Header.js";
import Footer from "components/Footer/Footer.js";
import Button from "components/CustomButtons/Button.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import HeaderLinks from "components/Header/HeaderLinks.js";
import Parallax from "components/Parallax/Parallax.js";
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import profile from "assets/img/examples/MRI_classification.png";

import { Collapse } from "@material-ui/core";

//import studio1 from "assets/img/examples/studio-1.jpg";
//import studio2 from "assets/img/examples/studio-2.jpg";
//import studio3 from "assets/img/examples/studio-3.jpg";
//import studio4 from "assets/img/examples/studio-4.jpg";
//import studio5 from "assets/img/examples/studio-5.jpg";
//import work1 from "assets/img/examples/olu-eletu.jpg";
//import work2 from "assets/img/examples/clem-onojeghuo.jpg";
//import work3 from "assets/img/examples/cynthia-del-rio.jpg";
//import work4 from "assets/img/examples/mariya-georgieva.jpg";
//import work5 from "assets/img/examples/clem-onojegaw.jpg";

import styles from "assets/jss/material-kit-react/views/profilePage.js";

const useStyles = makeStyles(styles);

export default function UseCaseMRI(props) {
  const classes = useStyles();
  const { ...rest } = props;
  const imageClasses = classNames(
    classes.imgRaised,
    classes.imgRounded,
    classes.imgFluid
  );
  //const navImageClasses = classNames(classes.imgRounded, classes.imgGallery);
  const [executed, setExecuted] = React.useState(false);
  var qkdResponse = "";

  const executeTask = () => {
    //const express = require("express");
    //const app = express();

    setExecuted(true);

    //const spawn = require("child_process").spawn;
    //const { pipeline } = require("stream");
    //app.get("/qkd-client", (request, response) => {
    //  const qkdClient = spawn("ls", ["-l"]);
    //  // pipe the process stream into the response stream
    //  pipeline(qkdClient, response, (err) => err && console.warn(err));
    //  request = null;
    //});
  };

  return (
    <div>
      <Header
        color="transparent"
        brand="Quantumacy"
        rightLinks={<HeaderLinks />}
        fixed
        changeColorOnScroll={{
          height: 200,
          color: "white",
        }}
        {...rest}
      />
      <Parallax
        small
        filter
        image={require("assets/img/profile-bg.jpg").default}
      />
      <div className={classNames(classes.main, classes.mainRaised)}>
        <div>
          <div className={classes.container}>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={6}>
                <div className={classes.profile}>
                  <div>
                    <img src={profile} alt="..." className={imageClasses} />
                  </div>
                  <div className={classes.name}>
                    <h3 className={classes.title}>Check MRI Classification</h3>
                    <h6>Healthcare</h6>
                  </div>
                </div>
              </GridItem>
            </GridContainer>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={8}>
                <h4>
                  This demo shows an example of transfer of personal data to a
                  central processing server to generate a health check score
                  based on pre-trained risk analysis models. The data is
                  provided by the patient and transferred to a hospital for
                  analysis across a QKD-secured link (please note that this is a
                  simulation, no hospital is involved, do not enter real
                  personal information). For more information on the Health
                  Check Score model read the <a href="/hcs">Health Check</a>
                  &nbsp;page.
                </h4>
                <p>&nbsp;</p>
              </GridItem>
              <GridItem xs={12} sm={12} md={8}>
                <center>
                  <Button color="primary" round onClick={executeTask}>
                    Run demo
                  </Button>
                </center>
              </GridItem>
            </GridContainer>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={8}>
                <Collapse in={executed}>
                  <Card>
                    <CardBody>{qkdResponse}</CardBody>
                  </Card>
                </Collapse>
                <p>&nbsp;</p>
              </GridItem>
            </GridContainer>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
