import React from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
import Camera from "@material-ui/icons/Camera";
import Palette from "@material-ui/icons/Palette";
import Favorite from "@material-ui/icons/Favorite";
// core components
import Header from "components/Header/Header.js";
import Footer from "components/Footer/Footer.js";
import Button from "components/CustomButtons/Button.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import HeaderLinks from "components/Header/HeaderLinks.js";
import NavPills from "components/NavPills/NavPills.js";
import Parallax from "components/Parallax/Parallax.js";

import styles from "styles/jss/nextjs-material-kit/pages/profilePage.js";

const useStyles = makeStyles(styles);

export default function AboutPage(props) {
  const classes = useStyles();
  const { ...rest } = props;
  const imageClasses = classNames(
    classes.imgRaised,
    classes.imgRoundedCircle,
    classes.imgFluid
  );
  const navImageClasses = classNames(classes.imgRounded, classes.imgGallery);
  return (
    <div>
      <Header
        color="transparent"
        brand="NextJS Material Kit"
        rightLinks={<HeaderLinks />}
        fixed
        changeColorOnScroll={{
          height: 200,
          color: "white",
        }}
        {...rest}
      />
      <Parallax small filter image="/img/bg2.jpg" />
      <div className={classNames(classes.main, classes.mainRaised)}>
        <div>
          <div className={classes.container}>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={6}>
                <div className={classes.profile}>
                  <div>
                    <img
                      src="/img/400JpgdpiLogo.jpg"
                      alt="..."
                      className={imageClasses}
                    />
                  </div>
                  <div className={classes.name}>
                    <h3 className={classes.title}><br/>What is Quantumacy?</h3>
                  </div>
                </div>
              </GridItem>
            </GridContainer>
            <div className={classes.description}>
              <p>
                The Quantumacy project is a proof-of-concept of integration and application
                of several provacy-preserving technologies to data analysis with
                sensitive data.{" "}<br/><br/>
                Quantumacy was funded as an open call of the EC-funded project openQKD in
                February 2021 for one year.<br/><br/>
                Between 2021 and 2022, Quantumacy partners CERN and Be-ys Research with
                the collaboration of the Seoul National University Hospital in Bundang 
                (South Korea) have developed a test platform integrating Quantum Key
                Distribution techniques (both simulated and on real links), homomorphic
                encryption, federated learning, and block chain.<br/><br/>
                Use cases exemplifying typical medical research and healthcare activities
                have been developed to experiment with the different techniques and
                assess how they would apply to differebt scenarios<br/><br/>
                Using standard QKD APIs implemented in a simple, but effective simulator
                proof-of-concept version of the popular openFL federated learning framework
                and the Be-ys patented block-chain framework usong QKD-based security
                have been developed and tested.<br/><br/>
                The software and use cases are available under the MIT open source license
                from the project Github <a href="https://github.com/CERN/Quantumacy">{" "}repository</a>.<br/><br/>
                The project is run at CERN under the framework of the
                <a href="https://quantum.cern">{" "}CERN Quantum Technology Initiative{" "}</a>
                For more information and collaboration contact
                <a href="mailto:QTI-info@cern.ch">{" "}the team</a>.

              </p>
            </div>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={8} className={classes.navWrapper}>
              </GridItem>
            </GridContainer>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
