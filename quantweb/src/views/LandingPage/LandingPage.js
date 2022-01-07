import React from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";

// @material-ui/icons

// core components
import Header from "components/Header/Header.js";
import Footer from "components/Footer/Footer.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
//import Button from "components/CustomButtons/Button.js";
import HeaderLinks from "components/Header/HeaderLinks.js";
import Parallax from "components/Parallax/Parallax.js";

import styles from "assets/jss/material-kit-react/views/landingPage.js";

// Sections for this page
import ProductSection from "./Sections/ProductSection.js";
import UseCaseSection from "./Sections/UseCaseSection.js";
import TeamSection from "./Sections/TeamSection.js";
import WorkSection from "./Sections/WorkSection.js";

import logo1 from "assets/img/400PngdpiLogoCropped_BW.png";
import logo2 from "assets/img/openQKD.png";
import logo3 from "assets/img/ec-logo.png";

const dashboardRoutes = [];

const useStyles = makeStyles(styles);

export default function LandingPage(props) {
  const classes = useStyles();
  const { ...rest } = props;
  return (
    <div>
      <Header
        color="transparent"
        routes={dashboardRoutes}
        brand="Quantumacy"
        rightLinks={<HeaderLinks />}
        fixed
        changeColorOnScroll={{
          height: 400,
          color: "white",
        }}
        {...rest}
      />
      <Parallax filter image={require("assets/img/landing-q.jpg").default}>
        <div className={classes.container}>
          <GridContainer>
            <GridItem xs={12} sm={12} md={6}>
              <h1 className={classes.title}>Quantum.Privacy</h1>
              <h4>
                Quantumacy is a privacy-preserving data analytics platform
                combining the security of QKD protocols and links with
                state-of-the-art homomorphic encryption capabilities to execute
                machine-learning and deep-learning workloads across a
                distributed federated-learning infrastructure.
              </h4>
              <br />
              <img src={logo1} alt="quantumacy" width={150} />
              &nbsp;&nbsp;&nbsp;
              <img src={logo2} alt="openQKD" width={150} />
              &nbsp;&nbsp;&nbsp;
              <img src={logo3} alt="EC" width={100} />
            </GridItem>
          </GridContainer>
        </div>
      </Parallax>
      <div className={classNames(classes.main, classes.mainRaised)}>
        <div className={classes.container}>
          <ProductSection />
          <UseCaseSection />
          <TeamSection />
          <WorkSection />
        </div>
      </div>
      <Footer />
    </div>
  );
}
