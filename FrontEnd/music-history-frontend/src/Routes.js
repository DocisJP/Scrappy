import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Timeline from "./Components/Timeline"; // Adjust the path as necessary
import Era from "./Components/Era"; // Adjust the path as necessary
import MusicStyle from "./Components/MusicStyle"; // Adjust the path as necessary
import Song from "./Components/Song"; // Adjust the path as necessary

function Routes() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Timeline} />
        <Route path="/era" component={Era} />
        <Route path="/musicstyle" component={MusicStyle} />
        <Route path="/song" component={Song} />
      </Switch>
    </Router>
  );
}

export default Routes;
