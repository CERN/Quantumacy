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

export default function TeamSection() {
  const classes = useStyles();
  const imageClasses = classNames(
    classes.imgRaised,
    classes.imgRoundedCircle,
    classes.imgFluid
  );
  return (
    <div className={classes.section}>
      <h2 className={classes.title}>The Quantumacy Team</h2>
      <div>
        <GridContainer>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <img
                  src="/img/faces/alberto.png"
                  alt="..."
                  className={imageClasses}
                />
              </GridItem>
              <h4 className={classes.cardTitle}>
                Alberto Di Meglio
                <br />
                <small className={classes.smallTitle}>Project Manager - CERN</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  Alberto is the Head of the CERN openlab team in the CERN IT DEpartment
                  and Coordinator of the CERN Quantum Technology Initiative. He has more than
                  twenty years of experience in coordinating joint R&amp;D projects between
                  Research and Industry.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
                <Button
                  justIcon
                  color="transparent"
                  className={classes.margin5}
                  href="https://twitter.com/AlbertoDiMeglio?ref=cernopenlab"
                  target="_blank"
                      >
                  <i className={classes.socials + " fab fa-twitter"} />
                </Button>
                <Button
                  justIcon
                  color="transparent"
                  className={classes.margin5}
                  href="https://www.linkedin.com/in/albertodimeglio/"
                  target="_blank"
                >
                  <i className={classes.socials + " fab fa-linkedin"} />
                </Button>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <img
                  src="/img/faces/avatar-male.png"
                  alt="..."
                  className={imageClasses}
                />
              </GridItem>
              <h4 className={classes.cardTitle}>
                Jose Cabrero Holgueras
                <br />
                <small className={classes.smallTitle}>Privacy-Preseving Technologies - CERN</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  You can write here details about one of your team members. You
                  can give more details about what they do. Feel free to add
                  some <a href="#pablo">links</a> for people to be able to
                  follow them outside the site.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
                <Button
                  justIcon
                  color="transparent"
                  className={classes.margin5}
                >
                  <i className={classes.socials + " fab fa-twitter"} />
                </Button>
                <Button
                  justIcon
                  color="transparent"
                  className={classes.margin5}
                >
                  <i className={classes.socials + " fab fa-linkedin"} />
                </Button>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <img
                  src="/img/faces/gm.jpg"
                  alt="..."
                  className={imageClasses}
                />
              </GridItem>
              <h4 className={classes.cardTitle}>
                Gabriele Morello
                <br />
                <small className={classes.smallTitle}>Software Engineering - CERN</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  Gabriele is a Computing Engineering student at Politecnico di Torino
                  and Technical Student at CERN. As part of the Quantumacy project, Gabriele
                  developed the QLKD simulator used in the test platform and ported
                  the openFL federated learning platform to use the QKD libraries instead
                  of the standard certificate-based security framework.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              <Button
                  justIcon
                  color="transparent"
                  className={classes.margin5}
                  href="https://www.linkedin.com/in/gabriele-morello"
                  target="_blank"
                >
                  <i className={classes.socials + " fab fa-linkedin"} />
                </Button>
              </CardFooter>
            </Card>
          </GridItem>
        </GridContainer>
        <GridContainer>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <img
                  src="/img/faces/dm.jpg"
                  alt="..."
                  className={imageClasses}
                />
              </GridItem>
              <h4 className={classes.cardTitle}>
                David Manset
                <br />
                <small className={classes.smallTitle}>CEO - Be-ys Research</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  David is the CEO of Be ys Research. Specialised in deeptechs and personal data protection, Dr. David Manset holds
                  a Habilitation thesis to conduct research (HDR) from Paris 1 Pantheon Sorbonne and a D.Phil. in Model Driven
                  Engineering of Distributed Computing Systems, from the University of the West of England in Bristol.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <img
                  src="/img/faces/mk.jpg"
                  alt="..."
                  className={imageClasses}
                />
              </GridItem>
              <h4 className={classes.cardTitle}>
                Mirko Koscina
                <br />
                <small className={classes.smallTitle}>Cryptography and Blocchain - Be-ys Pay</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  Dr Mirko Koscina currently occupies the CEO position at Be ys Pay. Mirkoholds a PhD from ENS-Paris,
                  he is a researcher in cryptography and blockchain and a believer in sharing knowledge.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <img
                  src="/img/faces/ok.jpg"
                  alt="..."
                  className={imageClasses}
                />
              </GridItem>
              <h4 className={classes.cardTitle}>
                Octavio Perez-Kempner
                <br />
                <small className={classes.smallTitle}>Research Engineer - Be-ys Research</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  Octavio is a Research Engineer at Be ys Research and PhD student at ENS-Paris working at the Information Security Group,
                  Computer Science Department. Octavio Perez-Kempner specialises in partial credentials sharing, blockchain and the use
                  of Zero Knowledge Proof.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              <Button
                  justIcon
                  color="transparent"
                  className={classes.margin5}
                  href="https://www.linkedin.com/in/gabriele-morello"
                  target="_blank"
                >
                  <i className={classes.socials + " fab fa-linkedin"} />
                </Button>
              </CardFooter>
            </Card>
          </GridItem>
        </GridContainer>
        <GridContainer>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <img
                  src="/img/faces/avatar-male.png"
                  alt="..."
                  className={imageClasses}
                />
              </GridItem>
              <h4 className={classes.cardTitle}>
                Hanyul Ryu
                <br />
                <small className={classes.smallTitle}>Software Engineering - SNUBH</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  Hanyul is a machine learning and privacy data expert at the Seoul National University Bundang Hospital.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <img
                  src="/img/faces/avatar-female.png"
                  alt="..."
                  className={imageClasses}
                />
              </GridItem>
              <h4 className={classes.cardTitle}>
                Sofia Vallecorsa
                <br />
                <small className={classes.smallTitle}>AI and Quantum Technologies - CERN</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  Sofia is the AI and Quantum Computing Lead in the CERN IT Innovation unit. She holds a PhDin Particle Physics and
                  a is an international expert in ML/DL/QML for physics applications.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card plain>
              <GridItem xs={12} sm={12} md={6} className={classes.itemGrid}>
                <img
                  src="/img/faces/michele.jpg"
                  alt="..."
                  className={imageClasses}
                />
              </GridItem>
              <h4 className={classes.cardTitle}>
                Michele Grossi
                <br />
                <small className={classes.smallTitle}>Quantum Technologies</small>
              </h4>
              <CardBody>
                <p className={classes.description}>
                  Michele is a senior fellow in quantum computing at CERN.
                  Michele has been working as Quantum Technical Ambassador at IBM and
                  Hybrid Cloud solution Architect. His focus is the development
                  of QML pipelines for HEP problems and their usage in different fields.
                </p>
              </CardBody>
              <CardFooter className={classes.justifyCenter}>
                <Button
                  justIcon
                  color="transparent"
                  className={classes.margin5}
                >
                  <i className={classes.socials + " fab fa-twitter"} />
                </Button>
                <Button
                  justIcon
                  color="transparent"
                  className={classes.margin5}
                >
                  <i className={classes.socials + " fab fa-instagram"} />
                </Button>
                <Button
                  justIcon
                  color="transparent"
                  className={classes.margin5}
                >
                  <i className={classes.socials + " fab fa-facebook"} />
                </Button>
              </CardFooter>
            </Card>
          </GridItem>
        </GridContainer>
      </div>
    </div>
  );
}
