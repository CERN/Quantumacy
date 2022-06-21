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

import YoutubeEmbed from "components/YouTubeEmbed/YouTubeEmbed.js";

import styles from "styles/jss/nextjs-material-kit/pages/profilePage.js";

import profile from "public/img/demos/qkd.jpg";

const useStyles = makeStyles(styles);

export default function UseCaseBlockchainPage(props) {
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
                    <h3 className={classes.title}>Blockchain for secure data sharing and storage</h3>
                    <h6>Technology</h6>
                  </div>
                </div>
              </GridItem>
            </GridContainer>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={8}>
                <h4>
                  Implementation of the GDPM patent (ie., General Data Protection Method for distributed storage and sharing of personal data -
                  European Patent EP 3 410 630 A1) integrating Quantum Key Distribution (QKD) and the ProRegister private blockchain.
                  This demonstration shows a new data sharing and storage patented protocol data carries its own processing purpose thanks
                  to a combination of QKD and homomorphic encryption, demonstrating a possible shift in the way data is professionally
                  processed everyday and gearing toward informational self-determination and Web 3.0.
                </h4>
                <p>&nbsp;</p>
              </GridItem>
              <GridItem xs={12} sm={12} md={8}>
                <center>
                  <div className="App">
                    <YoutubeEmbed embedId="j6FsUA7LSPk" />
                  </div>
                  <br/><br/>
                </center>
              </GridItem>
            </GridContainer>
            <GridContainer justify="center">
            </GridContainer>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
