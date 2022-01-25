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

import profile from "public/img/demos/MRI_classification.png";

const useStyles = makeStyles(styles);

export default function UseCaseMRIPage(props) {
  const classes = useStyles();
  const { ...rest } = props;
  const imageClasses = classNames(
    classes.imgRaised,
    classes.imgRoundedCircle,
    classes.imgFluid
  );
  const navImageClasses = classNames(classes.imgRounded, classes.imgGallery);

  const urlImageList = "http://olvm-livinglab-02:7000/images";
  const [imageListAvailable, setImageListAvailable] = React.useState(false);
  const [imageListHTML, setImageListHTML] = React.useState("");

  const url = "/demos/mri-client";
  const [executed, setExecuted] = React.useState(false);
  const [qkdHTML, setHTML] = React.useState("");

  const showImages = () => {
    var parser = new DOMParser();

    fetch(urlImageList)
    .then(function (response) {
      return response.text();
    })
    .then(function (data) {
      var htmlDoc = parser.parseFromString(data, 'text/html');
      setImageListHTML( htmlDoc.getElementById("result").innerHTML );
      //setHTML( data );
      }.bind(this))
    .catch(function (err) {
      setImageListHTML( err.stack );
    });

    setImageListAvailable(true);

  };

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
      setHTML( err.stack );
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
      <Parallax small filter image="/img/research-bg.jpg" />
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
                    <h3 className={classes.title}>Chest MRI Classification</h3>
                    <h6>Medical Research</h6>
                  </div>
                </div>
              </GridItem>
            </GridContainer>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={8}>
                <h4>
                  This demo explains how medical image classification can be done
                  securely across a distributed infrastructure by using QKD keys
                  to encrypt the communication and homomorphic encryption to
                  encrypt the tranferred images and perform the classification without
                  decrypting them on the remote server. For more information on
                  homomorphic encryption read the <a href="/fhe">Homomorphic Encryption</a> page.
                </h4>
                <p>&nbsp;</p>
              </GridItem>
              <GridItem xs={12} sm={12} md={8}>
                <center>
                  <Button color="primary" round onClick={showImages}>
                    Run demo
                  </Button>
                </center>
              </GridItem>
            </GridContainer>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={8}>
                <Collapse in={imageListAvailable}>
                  <Card>
                    <CardBody >
                      <div dangerouslySetInnerHTML={ { __html: setImageListHTML} } />
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
