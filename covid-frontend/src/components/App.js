import React, { Component, Fragment } from 'react';
import { ConfigProvider } from 'antd';
import deDE from 'antd/es/locale/de_DE';

class App extends Component {

  render () {
    return (
      <Fragment>
        <ConfigProvider locale={deDE}>
          { this.props.children }
        </ConfigProvider>
      </Fragment>
    );
  }
}

export default App;
