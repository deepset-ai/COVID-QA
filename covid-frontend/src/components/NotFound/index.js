import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Result, Button } from 'antd';
import links from 'routes/links';
import { withTranslation } from 'react-i18next';

class NotFound extends PureComponent {

  static propTypes = {
    history: PropTypes.object
  }

  handleBackHome = () => {
    this.props.history.push(links.home);
  }

  render() {
    const { t } = this.props;

    return (
      <Result
        status="404"
        title="404"
        subTitle={t('404.subtitle')}
        extra={
          <Button onClick={this.handleBackHome}>
            {t('404.button-text')}
          </Button>
        }
      />
    );
  }
}

export default connect()(withTranslation()(NotFound));
