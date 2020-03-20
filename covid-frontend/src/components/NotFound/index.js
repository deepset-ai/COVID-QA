import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Result, Button } from 'antd';
import links from 'routes/links';

class NotFound extends PureComponent {

  static propTypes = {
    history: PropTypes.object
  }

  handleBackHome = () => {
    this.props.history.push(links.home);
  }

  render() {
    return (
      <Result
        status="404"
        title="404"
        subTitle="Sorry, the page you visited does not exist."
        extra={
          <Button onClick={this.handleBackHome}>
            Back to Home
          </Button>
        }
      />
    );
  }
}

export default connect()(NotFound);
