import React from "react";

// nodejs library that concatenates classes
import classNames from "classnames";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
import Camera from "@material-ui/icons/Camera";
import Palette from "@material-ui/icons/Palette";
import Favorite from "@material-ui/icons/Favorite";

import { Collapse, TextField } from "@material-ui/core";

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
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Radio from "@material-ui/core/Radio";
import CustomInput from "components/CustomInput/CustomInput.js";
import FiberManualRecord from "@material-ui/icons/FiberManualRecord";
import InputAdornment from "@material-ui/core/InputAdornment";

import styles from "styles/jss/nextjs-material-kit/pages/profilePage.js";

import profile from "public/img/demos/health-check.jpg";

const useStyles = makeStyles(styles);

export default function UseCaseHCPage(props) {
  const classes = useStyles();
  const { ...rest } = props;
  const imageClasses = classNames(
    classes.imgRaised,
    classes.imgRoundedCircle,
    classes.imgFluid
  );
  const navImageClasses = classNames(classes.imgRounded, classes.imgGallery);

  const url = "/demos/hc-client";

  const [formOpened, setFormOpened] = React.useState(false);
  const [executed, setExecuted] = React.useState(false);
  const [hcHTML, setHTML] = React.useState("");

  const [selectedEnabledEthnicity, setSelectedEnabledEthnicity] = React.useState("");
  const [selectedEnabledSex, setSelectedEnabledSex] = React.useState("");
  const [age, setAge] = React.useState(-1);
  const [ageError, setAgeError] = React.useState(false);
  const [errorAgeText, setAgeErrorText] = React.useState("");
  const [totalChol, setTotalChol] = React.useState(-1);
  const [totalCholError, setTotalCholError] = React.useState(false);
  const [errorTotalCholText, setTotalCholErrorText] = React.useState("");
  const [hdlChol, setHDLChol] = React.useState(-1);
  const [hdlCholError, setHDLCholError] = React.useState(false);
  const [errorHDLCholText, setHDLCholErrorText] = React.useState("");
  const [systolic, setSystolic] = React.useState(-1);
  const [systolicError, setSystolicError] = React.useState(false);
  const [errorSystolicText, setSystolicErrorText] = React.useState("");
  const [selectedEnabledPressure, setSelectedEnabledPressure] = React.useState(-1);
  const [selectedEnabledSmoker, setSelectedEnabledSmoker] = React.useState(-1);
  const [selectedEnabledDiabetes, setSelectedEnabledDiabetes] = React.useState(-1);

  const formUpdate = {
    ethnicity: selectedEnabledEthnicity,
    sex: selectedEnabledSex,
    age: parseInt(age),
    totalChol: parseInt(totalChol),
    hdlChol: parseInt(hdlChol),
    systolic: parseInt(systolic),
    pressure: selectedEnabledPressure,
    smoker: selectedEnabledSmoker,
    diabetes: selectedEnabledDiabetes,
  };

  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(formUpdate),
  };

  const prepareForm = () => {

    setFormOpened(true);

  };

  const handleInputChange = (e) => {
    if (e.target.id === "Age") {
      if (e.target.value < 40 || e.target.value > 79) {
        setAgeError(true)
        setAgeErrorText("Invalid")
        }
    else {
        setAgeError(false)
        setAgeErrorText("")
      };
      setAge(e.target.value);
    }
    else if (e.target.id === "TotalCholesterol") {
      if (e.target.value < 130 || e.target.value > 320) {
        setTotalCholError(true)
        setTotalCholErrorText("Invalid")
      }
      else {
        setTotalCholError(false)
        setTotalCholErrorText("")
      };
      setTotalChol(e.target.value);
    }
    else if (e.target.id === "HDLCholesterol") {
      if (e.target.value < 20 || e.target.value > 100) {
        setHDLCholError(true)
        setHDLCholErrorText("Invalid")
      }
      else {
        setHDLCholError(false)
        setHDLCholErrorText("")
      };
      setHDLChol(e.target.value);
    }
    else if (e.target.id === "SystolicBloodPressure") {
      if (e.target.value < 90 || e.target.value > 200) {
        setSystolicError(true)
        setSystolicErrorText("Invalid")
      }
      else {
        setSystolicError(false)
        setSystolicErrorText("")
      };
      setSystolic(e.target.value);
    }
  };

  const submitInput = () => {

    if (errorAgeText != "" || errorTotalCholText != "" || errorHDLCholText != "" || errorSystolicText != "") {
      alert("Please check your values");
      return;
    }

    if (selectedEnabledEthnicity == "") {
      alert("Please check the category options");
      return;
    }
    if (selectedEnabledSex == "") {
      alert("Please check the Sex options");
      return;
    }
    if (age == -1) {
      setAgeError(true)
      setAgeErrorText("Invalid")
      alert("Please check the age value");
      return;
    }
    if (totalChol == -1) {
      setTotalCholError(true)
      setTotalCholErrorText("Invalid")
      alert("Please check the Total Cholesterol value");
      return;
    }
    if (hdlChol == -1) {
      setHDLCholError(true)
      setHDLCholErrorText("Invalid")
      alert("Please check the HDL Cholesterol value");
      return;
    }
    if (systolic == -1) {
      setSystolicError(true)
      setSystolicErrorText("Invalid")
      alert("Please check the Systolic Blood Pressure value");
      return;
    }
    if (selectedEnabledPressure == -1) {
      alert("Please check the Pressure Medications options");
      return;
    }
    if (selectedEnabledSmoker == -1) {
      alert("Please check the Smoking options");
      return;
    }
    if (selectedEnabledDiabetes == -1) {
      alert("Please check the Diabetes options");
      return;
    }

    var parser = new DOMParser();

    setExecuted(true);

    fetch(url, options)
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
      <Parallax small filter image="/img/healthcare-bg.jpg" />
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
                    <h3 className={classes.title}>Health Check</h3>
                    <h6>Healthcare</h6>
                  </div>
                </div>
              </GridItem>
            </GridContainer>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={8}>
                <h4>
                  This demo exemplifies a scenario in which a doctor or patient
                  need to submit data for further processing to a public facility.
                  The data collected in the form is encrypted using a homomorphic
                  encryption technique, the encrypted data is sent for processing,
                  and encrypted results are sent back. The results are finally
                  decrypted locally. The data is processed in its encrypted form
                  and personal information is never disclosed. This example uses the
                  <a href="https://www.microsoft.com/en-us/research/project/microsoft-seal/"> Microsoft SEAL HE libraries</a>. The use case is a simple cardiovascular
                  risk assessment using the <a href="https://www.ahajournals.org/doi/10.1161/01.cir.0000437741.48606.98">2013 ACC/AHA guidelines</a>.
                  <br/><br/><strong>PLEASE NOTE: this is a demo, not a medical tool, no identifiable personal information is collected and the data is not kept anywhere after the demo has run,
                  the results must not be taken as a valid medical check.</strong>
                </h4>
                <p>&nbsp;</p>
              </GridItem>
              <GridItem xs={12} sm={12} md={8}>
                <center>
                  <Button color="primary" round onClick={prepareForm}>
                    Run demo
                  </Button>
                </center>
              </GridItem>
            </GridContainer>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={8}>
                <Collapse in={formOpened}>
                  <Card>
                    <CardBody >
                      <div id="ethnicRadio">
                        <GridContainer>
                          <GridItem xs={12} sm={12} md={12}>
                            <center><strong>Input your values</strong></center>
                          </GridItem>
                          <GridItem xs={12} sm={12} md={6}>
                            <br/>
                            <p style={{textAlign:'right'}}><strong>Which category best describes yourself?</strong></p>
                          </GridItem>
                          <GridItem xs={12} sm={12} md={6}>
                            <br/>
                            <FormControlLabel
                              control={
                                <Radio
                                  checked={selectedEnabledEthnicity === "African-American"}
                                  onChange={() => setSelectedEnabledEthnicity("African-American")}
                                  value="African-American"
                                  name="Ethnicity"
                                  aria-label="Black or African-American"
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
                              label="Black or African-American"
                            />
                            <br/>
                            <FormControlLabel
                              control={
                                <Radio
                                  checked={selectedEnabledEthnicity === "White"}
                                  onChange={() => setSelectedEnabledEthnicity("White")}
                                  value="White"
                                  name="Ethnicity"
                                  aria-label="White"
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
                              label="White"
                            />
                            <br/>
                            <FormControlLabel
                              control={
                                <Radio
                                  checked={selectedEnabledEthnicity === "Other"}
                                  onChange={() => setSelectedEnabledEthnicity("Other")}
                                  value="Other"
                                  name="Ethnicity"
                                  aria-label="Other"
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
                              label="Other"
                            />
                          </GridItem>
                        </GridContainer>
                      </div>
                      <div id="sexRadio">
                        <GridContainer>
                          <GridItem xs={12} sm={12} md={6}>
                            <p style={{textAlign:'right'}}><strong>Sex</strong></p>
                          </GridItem>
                          <GridItem xs={12} sm={12} md={6}>
                            <FormControlLabel
                              control={
                                <Radio
                                  checked={selectedEnabledSex === "Female"}
                                  onChange={() => setSelectedEnabledSex("Female")}
                                  value="Female"
                                  name="Sex"
                                  aria-label="Female"
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
                              label="Female"
                            />
                            <br/>
                            <FormControlLabel
                              control={
                                <Radio
                                  checked={selectedEnabledSex === "Male"}
                                  onChange={() => setSelectedEnabledSex("Male")}
                                  value="Male"
                                  name="Sex"
                                  aria-label="Male"
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
                              label="Male"
                            />
                          </GridItem>
                        </GridContainer>
                      </div>
                      <div id="ageForm">
                        <GridContainer>
                          <GridItem xs={12} sm={12} md={6}>
                              <br/>
                              <p style={{textAlign:'right'}}><strong>Age</strong></p>
                          </GridItem>
                          <GridItem xs={12} sm={12} md={6}>
                            <br/>
                            <p style={{textAlign:'left'}}>
                              <TextField
                                error={ageError}
                                helperText={errorAgeText}
                                id="Age"
                                type="number"
                                onChange={handleInputChange}
                                inputProps={{
                                  placeholder: "Years",
                                }}
                                formControlProps={{
                                  fullWidth: true,
                                }}
                              />
                            </p>
                        </GridItem>
                        </GridContainer>
                      </div>
                      <div id="TotalCholForm">
                        <GridContainer>
                          <GridItem xs={12} sm={12} md={6}>
                              <br/>
                              <p style={{textAlign:'right'}}><strong>Total cholesterol</strong></p>
                          </GridItem>
                          <GridItem xs={12} sm={12} md={6}>
                            <br/>
                            <p style={{textAlign:'left'}}>
                              <TextField
                                error={totalCholError}
                                helperText={errorTotalCholText}
                                id="TotalCholesterol"
                                type="number"
                                onChange={handleInputChange}
                                inputProps={{
                                  placeholder: "mg/dl",
                                }}
                                formControlProps={{
                                  fullWidth: true,
                                }}
                              />
                            </p>
                          </GridItem>
                        </GridContainer>
                      </div>
                      <div id="hdlChol">
                        <GridContainer>
                          <GridItem xs={12} sm={12} md={6}>
                              <br/>
                              <p style={{textAlign:'right'}}><strong>HDL cholesterol</strong></p>
                          </GridItem>
                          <GridItem xs={12} sm={12} md={6}>
                            <br/>
                            <p style={{textAlign:'left'}}>
                              <TextField
                                error={hdlCholError}
                                helperText={errorHDLCholText}
                                id="HDLCholesterol"
                                type="number"
                                onChange={handleInputChange}
                                inputProps={{
                                  placeholder: "mg/dl",
                                }}
                                formControlProps={{
                                  fullWidth: true,
                                }}
                              />
                            </p>
                          </GridItem>
                        </GridContainer>
                      </div>
                      <div id="systeolicForm">
                        <GridContainer>
                          <GridItem xs={12} sm={12} md={6}>
                              <br/>
                              <p style={{textAlign:'right'}}><strong>Systolic blood pressure</strong></p>
                          </GridItem>
                          <GridItem xs={12} sm={12} md={6}>
                            <br/>
                            <p style={{textAlign:'left'}}>
                              <TextField
                                error={systolicError}
                                helperText={errorSystolicText}
                                id="SystolicBloodPressure"
                                type="number"
                                onChange={handleInputChange}
                                inputProps={{
                                  placeholder: "mmHg",
                                }}
                                formControlProps={{
                                  fullWidth: true,
                                }}
                              />
                            </p>
                          </GridItem>
                        </GridContainer>
                      </div>
                      <div id="pressureRadio">
                        <GridContainer>
                          <GridItem xs={12} sm={12} md={6}>
                            <p style={{textAlign:'right'}}><strong>Do you take blood pressure medications?</strong></p>
                          </GridItem>
                          <GridItem xs={12} sm={12} md={6}>
                            <FormControlLabel
                              control={
                                <Radio
                                  checked={selectedEnabledPressure === 1}
                                  onChange={() => setSelectedEnabledPressure(1)}
                                  value="1"
                                  name="Pressure"
                                  aria-label="Yes"
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
                              label="Yes"
                            />
                            <br/>
                            <FormControlLabel
                              control={
                                <Radio
                                  checked={selectedEnabledPressure === 0}
                                  onChange={() => setSelectedEnabledPressure(0)}
                                  value="0"
                                  name="Pressure"
                                  aria-label="No"
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
                              label="No"
                            />
                          </GridItem>
                        </GridContainer>
                      </div>
                      <div id="smokeForm">
                        <GridContainer>
                          <GridItem xs={12} sm={12} md={6}>
                            <p style={{textAlign:'right'}}><strong>Do you smoke cigarettes?</strong></p>
                          </GridItem>
                          <GridItem xs={12} sm={12} md={6}>
                            <FormControlLabel
                              control={
                                <Radio
                                  checked={selectedEnabledSmoker === 1}
                                  onChange={() => setSelectedEnabledSmoker(1)}
                                  value="1"
                                  name="Smoker"
                                  aria-label="Yes"
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
                              label="Yes"
                            />
                            <br/>
                            <FormControlLabel
                              control={
                                <Radio
                                  checked={selectedEnabledSmoker === 0}
                                  onChange={() => setSelectedEnabledSmoker(0)}
                                  value="0"
                                  name="Smoker"
                                  aria-label="No"
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
                              label="No"
                            />
                          </GridItem>
                        </GridContainer>
                      </div>
                      <div id="diabetesForm">
                        <GridContainer>
                          <GridItem xs={12} sm={12} md={6}>
                            <p style={{textAlign:'right'}}><strong>Do you have diabetes?</strong></p>
                          </GridItem>
                          <GridItem xs={12} sm={12} md={6}>
                            <FormControlLabel
                              control={
                                <Radio
                                  checked={selectedEnabledDiabetes === 1}
                                  onChange={() => setSelectedEnabledDiabetes(1)}
                                  value="1"
                                  name="Diabetes"
                                  aria-label="Yes"
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
                              label="Yes"
                            />
                            <br/>
                            <FormControlLabel
                              control={
                                <Radio
                                  checked={selectedEnabledDiabetes === 0}
                                  onChange={() => setSelectedEnabledDiabetes(0)}
                                  value="0"
                                  name="Diabetes"
                                  aria-label="No"
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
                              label="No"
                            />
                          </GridItem>
                        </GridContainer>
                      </div>
                      <GridContainer>
                        <GridItem xs={12} sm={12} md={12}>
                          <div id="InputForm">
                            <center>
                              <br></br>
                              <Button color="primary" round onClick={submitInput}>
                                Submit
                              </Button>
                            </center>
                          </div>
                        </GridItem>
                      </GridContainer>
                      <Collapse in={executed}>
                        <Card>
                          <CardBody >
                            <GridContainer>
                              <GridItem xs={12} sm={12} md={12}>
                                <div dangerouslySetInnerHTML={ { __html: hcHTML} } />
                              </GridItem>
                            </GridContainer>
                          </CardBody>
                        </Card>
                      </Collapse>
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
