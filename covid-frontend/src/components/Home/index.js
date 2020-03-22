import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Row, Col } from 'antd';
import links from 'routes/links';
import * as actions from 'store/actions/globalSearch';
import { WrappedSearchForm as SearchForm } from './SearchForm';
import logo from 'assets/images/logo.png';
import styles from './styles.module.scss';

class Home extends PureComponent {

  static propTypes = {
    history: PropTypes.object,
    globalSearch: PropTypes.object,
    actions: PropTypes.object
  }

  handleSubmit = (value) => {
    this.props.actions.setSelectedValue(value);
    this.props.history.push(links.answers);
  }

  render() {
    const { currentString, options, filters } = this.props.globalSearch.search;
    return (
      <div className={styles.wrapper}>
        <Row>
          <Col sm={{ span: 20, offset: 2 }} md={{ span: 16, offset: 4 }} lg={{ span: 8, offset: 8 }}>
            <div className={styles.content}>

              <div className={styles.logoWrapper}>
                <div className={styles.logo}>
                  <img src={logo} alt="logo"/>
                </div>
              </div>

              <SearchForm
                value={currentString}
                options={options}
                filters={filters}
                onSearch={this.props.actions.updateSearchValue}
                onSubmit={this.handleSubmit}
              />
            </div>
          </Col>
        </Row>
      </div>
    );
  }
}

export default connect(
  state => ({
    globalSearch: state.globalSearch
  }),
  dispatch => ({
    actions: bindActionCreators(actions, dispatch)
  })
)(Home);
