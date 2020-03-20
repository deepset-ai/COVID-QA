import React, { PureComponent, Fragment } from 'react';
// import PropTypes from 'prop-types';
import { connect } from 'react-redux';
// import { bindActionCreators } from 'redux';
// import { Loader } from 'components/common/presentational';

class Provider extends PureComponent {

  static propTypes = {
    // companies: PropTypes.object,
    // userActions: PropTypes.object,
    // companiesActions: PropTypes.object
  }

  render () {

    // next will be removed later
    // if (!companies.isReady) {
    //   return <Loader fullSized size={30} />;
    // }

    return (
      <Fragment>
        { this.props.children }
      </Fragment>

    );
  }
}

export default connect(
  // state => ({
  //   companies: state.companies
  // }),
  // dispatch => ({
  //   companiesActions: bindActionCreators(companiesActions, dispatch),
  // })
)(Provider);
