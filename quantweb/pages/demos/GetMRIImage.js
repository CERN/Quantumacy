import React from "react";
import Image from "next/image";

import { makeStyles } from "@material-ui/core/styles";

import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Radio from "@material-ui/core/Radio";
import FiberManualRecord from "@material-ui/icons/FiberManualRecord";

import styles from "styles/jss/nextjs-material-kit/pages/componentsSections/basicsStyle.js";

//export default function GetMRIImage({ data }) {
  const GetMRIImage = ( data ) => {
    // Render data...

    const useStyles = makeStyles(styles);
    const classes = useStyles();

    const [selectedEnabled, setSelectedEnabled] = React.useState("F0");
  
    var imageDynamicF0 = "/data/images/frontal_0.png"; // + data.split('","')[0];
    var imageDynamicF1 = "/data/images/frontal_1.png"; // + data.split('","')[0];
    var imageDynamicF2 = "/data/images/frontal_2.png"; // + data.split('","')[0];
    var imageDynamicF3 = "/data/images/frontal_30.png"; // + data.split('","')[0];
    var imageDynamicL0 = "/data/images/lateral_17.png"; // + data.split('","')[0];
    var imageDynamicL1 = "/data/images/lateral_19.png"; // + data.split('","')[0];
    var imageDynamicL2 = "/data/images/lateral_21.png"; // + data.split('","')[0];
    var imageDynamicL3 = "/data/images/lateral_3.png"; // + data.split('","')[0];

  return (
          <div style={{width:600}}>
            <GridContainer >
              <GridItem xs={12} sm={6} md={3} lg={3} align="center">
                <Image src={imageDynamicF0}
                  alt="MRI Image"
                  width={150}
                  height={150}/>
                <br></br>
                <FormControlLabel
                  control={
                    <Radio
                      checked={selectedEnabled === "F0"}
                      onChange={() => setSelectedEnabled("F0")}
                      value="F0"
                      name="Frontal 0"
                      aria-label="F0"
                      icon={
                        <FiberManualRecord className={classes.radioUnchecked} />
                      }
                      checkedIcon={
                        <FiberManualRecord className={classes.radioChecked} />
                      }
                      classes={{
                        checked: classes.radio,
                        root: classes.radioRoot,
                      }}
                    />
                  }
                  classes={{
                    label: classes.label,
                    root: classes.labelRoot,
                  }}
                  label="F0"
                />
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3} align="center">
                <Image src={imageDynamicF1}
                    alt="MRI Image"
                    width={150}
                    height={150}/>
                <br></br>
                <FormControlLabel
                  control={
                    <Radio
                      checked={selectedEnabled === "F1"}
                      onChange={() => setSelectedEnabled("F1")}
                      value="F1"
                      name="Frontal 1"
                      aria-label="F1"
                      icon={
                        <FiberManualRecord className={classes.radioUnchecked} />
                      }
                      checkedIcon={
                        <FiberManualRecord className={classes.radioChecked} />
                      }
                      classes={{
                        checked: classes.radio,
                        root: classes.radioRoot,
                      }}
                    />
                  }
                  classes={{
                    label: classes.label,
                    root: classes.labelRoot,
                  }}
                  label="F1"
                />
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3} align="center">
                <Image src={imageDynamicF2}
                  alt="MRI Image"
                  width={150}
                  height={150}/>
                <br></br>
                <FormControlLabel
                  control={
                    <Radio
                      checked={selectedEnabled === "F2"}
                      onChange={() => setSelectedEnabled("F2")}
                      value="F2"
                      name="Frontal 2"
                      aria-label="F2"
                      icon={
                        <FiberManualRecord className={classes.radioUnchecked} />
                      }
                      checkedIcon={
                        <FiberManualRecord className={classes.radioChecked} />
                      }
                      classes={{
                        checked: classes.radio,
                        root: classes.radioRoot,
                      }}
                    />
                  }
                  classes={{
                    label: classes.label,
                    root: classes.labelRoot,
                  }}
                  label="F2"
                />
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3} align="center">
                <Image src={imageDynamicF3}
                  alt="MRI Image"
                  width={150}
                  height={150}/>
                <br></br>
                <FormControlLabel
                  control={
                    <Radio
                      checked={selectedEnabled === "F3"}
                      onChange={() => setSelectedEnabled("F3")}
                      value="F3"
                      name="Frontal 3"
                      aria-label="F3"
                      icon={
                        <FiberManualRecord className={classes.radioUnchecked} />
                      }
                      checkedIcon={
                        <FiberManualRecord className={classes.radioChecked} />
                      }
                      classes={{
                        checked: classes.radio,
                        root: classes.radioRoot,
                      }}
                    />
                  }
                  classes={{
                    label: classes.label,
                    root: classes.labelRoot,
                  }}
                  label="F3"
                />
              </GridItem>
            </GridContainer>

            <GridContainer>
              <GridItem xs={12} sm={6} md={3} lg={3} align="center">
                <Image src={imageDynamicL0}
                  alt="MRI Image"
                  width={150}
                  height={150}/>
                <br></br>
                <FormControlLabel
                  control={
                    <Radio
                      checked={selectedEnabled === "L0"}
                      onChange={() => setSelectedEnabled("L0")}
                      value="L0"
                      name="Lateral 0"
                      aria-label="L0"
                      icon={
                        <FiberManualRecord className={classes.radioUnchecked} />
                      }
                      checkedIcon={
                        <FiberManualRecord className={classes.radioChecked} />
                      }
                      classes={{
                        checked: classes.radio,
                        root: classes.radioRoot,
                      }}
                    />
                  }
                  classes={{
                    label: classes.label,
                    root: classes.labelRoot,
                  }}
                  label="L0"
                />
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3} align="center">
                <Image src={imageDynamicL1}
                  alt="MRI Image"
                  width={150}
                  height={150}/>
                <br></br>
                <FormControlLabel
                  control={
                    <Radio
                      checked={selectedEnabled === "L1"}
                      onChange={() => setSelectedEnabled("L1")}
                      value="L1"
                      name="Lateral 1"
                      aria-label="L1"
                      icon={
                        <FiberManualRecord className={classes.radioUnchecked} />
                      }
                      checkedIcon={
                        <FiberManualRecord className={classes.radioChecked} />
                      }
                      classes={{
                        checked: classes.radio,
                        root: classes.radioRoot,
                      }}
                    />
                  }
                  classes={{
                    label: classes.label,
                    root: classes.labelRoot,
                  }}
                  label="L1"
                />
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3} align="center">
                <Image src={imageDynamicL2}
                  alt="MRI Image"
                  width={150}
                  height={150}/>
                <br></br>
                <FormControlLabel
                  control={
                    <Radio
                      checked={selectedEnabled === "L2"}
                      onChange={() => setSelectedEnabled("L2")}
                      value="L2"
                      name="Lateral 2"
                      aria-label="L2"
                      icon={
                        <FiberManualRecord className={classes.radioUnchecked} />
                      }
                      checkedIcon={
                        <FiberManualRecord className={classes.radioChecked} />
                      }
                      classes={{
                        checked: classes.radio,
                        root: classes.radioRoot,
                      }}
                    />
                  }
                  classes={{
                    label: classes.label,
                    root: classes.labelRoot,
                  }}
                  label="L2"
                />
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3} align="center">
                <Image src={imageDynamicL3}
                  alt="MRI Image"
                  width={150}
                  height={150}/>
                <br></br>
                <FormControlLabel
                  control={
                    <Radio
                      checked={selectedEnabled === "L3"}
                      onChange={() => setSelectedEnabled("L3")}
                      value="L3"
                      name="Lateral 3"
                      aria-label="L3"
                      icon={
                        <FiberManualRecord className={classes.radioUnchecked} />
                      }
                      checkedIcon={
                        <FiberManualRecord className={classes.radioChecked} />
                      }
                      classes={{
                        checked: classes.radio,
                        root: classes.radioRoot,
                      }}
                    />
                  }
                  classes={{
                    label: classes.label,
                    root: classes.labelRoot,
                  }}
                  label="L3"
                />
              </GridItem>
            </GridContainer>
          </div>
  );
}

// This gets called on every request
//const args = ["client", "188.184.195.170:5002", "188.184.195.170:5000"];
//const args = ["client", "188.184.195.118:5002", "188.184.195.118:5000"];
//const args = ["client", "188.184.195.58:5002", "188.184.195.58:5000"];
export async function getServerSideProps() {
  var data = "";
  return { props: { data } }
}
 
export default GetMRIImage;
