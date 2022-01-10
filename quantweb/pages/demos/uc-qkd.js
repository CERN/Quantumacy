import React from "react";

// nodejs library that concatenates classes
import classNames from "classnames";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
import Camera from "@material-ui/icons/Camera";
import Palette from "@material-ui/icons/Palette";
import Favorite from "@material-ui/icons/Favorite";

import { Collapse } from "@material-ui/core";

// core components
import Header from "components/Header/Header.js";
import Footer from "components/Footer/Footer.js";
import Button from "components/CustomButtons/Button.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import HeaderLinks from "components/Header/HeaderLinks.js";
import NavPills from "components/NavPills/NavPills.js";
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import Parallax from "components/Parallax/Parallax.js";

import styles from "styles/jss/nextjs-material-kit/pages/profilePage.js";

import profile from "public/img/demos/qkd.jpg";

const useStyles = makeStyles(styles);

export default function UseCaseQKDPage(props) {
  const classes = useStyles();
  const { ...rest } = props;
  const imageClasses = classNames(
    classes.imgRaised,
    classes.imgRoundedCircle,
    classes.imgFluid
  );
  const navImageClasses = classNames(classes.imgRounded, classes.imgGallery);

  const url = "/qkd-client";
  const [executed, setExecuted] = React.useState(false);
  const [qkdHTML, setHTML] = React.useState("");

  const executeTask = () => {
    var parser = new DOMParser();

    setExecuted(true);

    fetch(url)
    .then(function (response) {
      return response.text();
    })
    .then(function (data) {
      var htmlDoc = parser.parseFromString(data, 'text/html');
      setHTML( htmlDoc.getElementById("result").innerHTML );
      //setHTML( data );
      }.bind(this))
    .catch(function (err) {
      setResponse( err.stack );
    });

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
      <Parallax small filter image="/img/technology-bg.jpg" />
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
                    <h3 className={classes.title}>Quantum Key Distribution</h3>
                    <h6>Technology</h6>
                  </div>
                </div>
              </GridItem>
            </GridContainer>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={8}>
                <h4>
                  This demo explains how QKD works and shows how to use the
                  Quantumacy QKD simulator to generate secure symmetric keys
                  using the BB84 protocol. For more information on Quantum Key
                  Distribution (QKD) read the <a href="/qkd">QKD</a> page.
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
                    <CardBody >
                      <div dangerouslySetInnerHTML={ { __html: qkdHTML} } />
                    </CardBody>
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
