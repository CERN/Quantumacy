import React from "react";
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
//import Button from "components/CustomButtons/Button.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import HeaderLinks from "components/Header/HeaderLinks.js";
//import NavPills from "components/NavPills/NavPills.js";
import Parallax from "components/Parallax/Parallax.js";

import profile from "assets/img/examples/qkd.jpg";

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

export default function TechnologyQKD(props) {
  const classes = useStyles();
  const { ...rest } = props;
  const imageClasses = classNames(
    classes.imgRaised,
    classes.imgRounded,
    classes.imgFluid
  );
  //const navImageClasses = classNames(classes.imgRounded, classes.imgGallery);
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
                    <h3 className={classes.title}>Quantum Key Distribution</h3>
                    <h6>Technology</h6>
                  </div>
                </div>
              </GridItem>
            </GridContainer>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={8}>
                <h4>
                  Quantum key distribution (QKD) is a secure communication
                  method which implements a cryptographic protocol involving
                  components of quantum mechanics. It enables two parties to
                  produce a shared random secret key known only to them, which
                  can then be used to encrypt and decrypt messages. An important
                  and unique property of quantum key distribution is the ability
                  of the two communicating users to detect the presence of any
                  third party trying to gain knowledge of the key. This results
                  from a fundamental aspect of quantum mechanics: the process of
                  measuring a quantum system in general disturbs the system. A
                  third party trying to eavesdrop on the key must in some way
                  measure it, thus introducing detectable anomalies. By using
                  quantum superpositions or quantum entanglement and
                  transmitting information in quantum states, a communication
                  system can be implemented that detects eavesdropping. If the
                  level of eavesdropping is below a certain threshold, a key can
                  be produced that is guaranteed to be secure (that is the
                  eavesdropper has no information about it), otherwise no secure
                  key is possible and communication is aborted.
                </h4>
                <h4>
                  The main drawback of quantum key distribution is that it
                  usually relies on having an authenticated classical channel of
                  communications. In modern cryptography, having an
                  authenticated classical channel means that one has either
                  already exchanged a symmetric key of sufficient length or
                  public keys of sufficient security level. With such
                  information already available, one can achieve authenticated
                  and secure communications without using QKD, such as by using
                  the Galois/Counter Mode of the Advanced Encryption Standard.
                  Thus QKD does the work of a Stream Cipher at many times the
                  cost.
                </h4>
                <h4>
                  Quantum key distribution is only used to produce and
                  distribute a key, not to transmit any message data. This key
                  can then be used with any chosen encryption algorithm to
                  encrypt (and decrypt) a message, which can then be transmitted
                  over a standard communication channel. The algorithm most
                  commonly associated with QKD is the one-time pad, as it is
                  provably secure when used with a secret, random key.
                </h4>
                <h4>
                  As QKD is today mainly implemented as point-to-point link
                  involving two endpoints connected by a quantum channel, it is
                  usually implemented as a combination of a QKD link with a link
                  encryptor to form a QKD Link Encryptor, anetwork-transparent
                  cryptographic system. A QKD link encryptor is a Quantum
                  Cryptography appliance for point-to-point link encryption
                  similar to a Virtual Private Network VPN tunnel. The link
                  encryptor usually uses the keys supplied by QKD as keys for a
                  symmetrical block cipher (for example the Advanced Encryption
                  Standard AES) or steam cipher (One Time Pad for highest
                  security) and can be used for example to encrypt traffic on an
                  Ethernet of Fiber Channel link. The QKD Link encryptor may be
                  used to support communications between two adjacent network
                  nodes employing QKD or it may provide protection for
                  communications end-to-end across a network of nodes as a VPN
                  tunnel.
                </h4>
                <h4>
                  Since physical QKD links are not commodity yet and will only
                  be available for a limited time during the lifetime of the
                  project, the initial implementation of the QUANTUMACY platform
                  is based on simulated links.
                </h4>
                <p>&nbsp;</p>
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
