import React, { Component } from 'react';
import { Header } from '../common';
import styles from './styles.module.scss';

class MainTemplate extends Component {

  static propTypes = {}

  render() {
    return (
      <div className={styles.wrapper}>
        <Header />

        <div className={styles.content}>
          { this.props.children }
        </div>

      </div>

    );
  }
}

export default MainTemplate;
