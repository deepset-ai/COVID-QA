import React, { Component, Fragment } from 'react';

class App extends Component {

  render () {
    return (
      <Fragment>
        { this.props.children }
      </Fragment>
    );
  }
}

export default App;
