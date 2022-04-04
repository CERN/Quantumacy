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
              <GridItem xs={12} sm={6} md={3} lg={3}>
                <Image src={imageDynamicF0}
                      alt="MRI Image"
                      width={150}
                      height={150}/>
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3}>
                <Image src={imageDynamicF1}
                      alt="MRI Image"
                      width={150}
                      height={150}/>
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3}>
                <Image src={imageDynamicF2}
                      alt="MRI Image"
                      width={150}
                      height={150}/>
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3}>
                <Image src={imageDynamicF3}
                      alt="MRI Image"
                      width={150}
                      height={150}/>
              </GridItem>
            </GridContainer>

            <GridContainer >
              <GridItem xs={12} sm={6} md={3} lg={3}>
              <FormControlLabel
                  control={
                    <Radio
                      //checked={selectedEnabled === "F0"}
                      //onChange={() => setSelectedEnabled("F0")}
                      value="F0"
                      name="Frontal 01"
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
                  label=""
                />
            </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3}>
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3}>
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3}>
              </GridItem>
            </GridContainer>

            <GridContainer>
            <GridItem xs={12} sm={6} md={3} lg={3}>
                  <Image src={imageDynamicL0}
                    alt="MRI Image"
                    width={150}
                    height={150}/>
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3}>
                  <Image src={imageDynamicL1}
                    alt="MRI Image"
                    width={150}
                    height={150}/>
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3}>
                  <Image src={imageDynamicL2}
                    alt="MRI Image"
                    width={150}
                    height={150}/>
              </GridItem>
              <GridItem xs={12} sm={6} md={3} lg={3}>
                  <Image src={imageDynamicL3}
                    alt="MRI Image"
                    width={150}
                    height={150}/>
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
