import React from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";

// @material-ui/icons

// core components
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import Button from "components/CustomButtons/Button.js";
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import CardFooter from "components/Card/CardFooter.js";

import styles from "styles/jss/nextjs-material-kit/pages/landingPageSections/teamStyle.js";

const useStyles = makeStyles(styles);

import case1 from "public/img/demos/qkd.jpg";
import case2 from "public/img/demos/health-check.jpg";
import case3 from "public/img/demos/MRI_classification.png";
import case4 from "public/img/demos/FL.png";
import case5 from "public/img/demos/Parkinson.png";
import case6 from "public/img/demos/BlockChain.png";

export default function UseCaseSection() {
  const classes = useStyles();
  const imageClasses = classNames(
    classes.imgRaised,
    classes.imgRounded,
    classes.imgFluid
  );
  return (
    <div className={classes.section}>
      <h2 className={classes.title}>Demo Use Cases</h2>
      <div>
        <GridContainer>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <a
                  href="/demos/uc-qkd">
                  <img
                    src={case1}
                    alt="QKD"
                    className={imageClasses}
                />
              </a>
              </GridItem>
              <h4 className={classes.cardTitle}>
              Key Generation
                <br />
                <small className={classes.smallTitle}>Technology</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  This demo explains how QKD works and shows how to use the
                  Quantumacy QKD simulator to generate secure symmetric keys
                  using the BB84 protocol.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
          <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <a href="/demos/uc-hcs">
                  <img src={case2} alt="..." className={imageClasses} />
                </a>
              </GridItem>
              <h4 className={classes.cardTitle}>
                Health Check Score
                <br />
                <small className={classes.smallTitle}>Healthcare</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  This demo shows how to protect the privacy of personal
                  information transmitted through Internet connections using
                  homomorphic encryption.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
          <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <a href="/demos/uc-mri">
                  <img src={case3} alt="Chest MRI Classification" className={imageClasses} />
                </a>
              </GridItem>
              <h4 className={classes.cardTitle}>
                Chest MRI Classification
                <br />
                <small className={classes.smallTitle}>Medical Research</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  This demo shows how to implement a simple image classification
                  pipeline over QKD-secured networks using
                  homomorphically-encrypted images.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              </CardFooter>
            </Card>
          </GridItem>
        </GridContainer>
        <GridContainer>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <a href="/uc-hcs">
                  <img src={case4} alt="..." className={imageClasses} />
                </a>
              </GridItem>
              <h4 className={classes.cardTitle}>
                Secure Federated Learning
                <br />
                <small className={classes.smallTitle}>Technology</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  This demo explains how to extend Federated Learning frameworks to
                  use symmetric keys generated by QKD to secure the communication
                  between the computing nodes.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <a href="/uc-fl">
                  <img src={case5} alt="Parkinson" className={imageClasses} />
                </a>
              </GridItem>
              <h4 className={classes.cardTitle}>
                Parkinson&apos;s Symptoms Classification
                <br />
                <small className={classes.smallTitle}>Healthcare</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  This demo shows an application of secure federated learning to classify
                  Parkinson's tremor symptoms from wearable and portable sensor devices.
                  The links between the analysis nodes are all secured using QKD keys.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <a href="/uc-mri">
                  <img src={case6} alt="..." className={imageClasses} />
                </a>
              </GridItem>
              <h4 className={classes.cardTitle}>
                Secure Block Chains
                <br />
                <small className={classes.smallTitle}>Technology</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  This demo shows an example of a block chain framework to
                  record and validate transactions across a distributed
                  data analysis pipeline using keys generated by the QKD
                  infrastructure.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              </CardFooter>
            </Card>
          </GridItem>
        </GridContainer>
      </div>
    </div>
  );
}
