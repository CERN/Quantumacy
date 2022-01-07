import React from "react";
import ReactDOM from "react-dom";
import { createBrowserHistory } from "history";
import { Router, Route, Switch } from "react-router-dom";

import "assets/scss/material-kit-react.scss?v=1.10.0";

// pages for this product
import Components from "views/Components/Components.js";
import LandingPage from "views/LandingPage/LandingPage.js";
import ProfilePage from "views/ProfilePage/ProfilePage.js";
import TechnologyQKD from "views/Technologies/QKD.js";
import UseCaseQKD from "views/UseCases/UseCaseQKD.js";
import UseCaseHCS from "views/UseCases/UseCaseHCS.js";
import UseCaseMRI from "views/UseCases/UseCaseMRI.js";
import LoginPage from "views/LoginPage/LoginPage.js";

var hist = createBrowserHistory();

ReactDOM.render(
  <Router history={hist}>
    <Switch>
      <Route path="/profile-page" component={ProfilePage} />
      <Route path="/login-page" component={LoginPage} />
      <Route path="/components" component={Components} />
      <Route path="/qkd" component={TechnologyQKD} />
      <Route path="/uc-qkd" component={UseCaseQKD} />
      <Route path="/uc-hcs" component={UseCaseHCS} />
      <Route path="/uc-mri" component={UseCaseMRI} />
      <Route path="/" component={LandingPage} />
    </Switch>
  </Router>,
  document.getElementById("root")
);
