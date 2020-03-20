import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { Spin, Icon } from 'antd';
import cn from 'classnames';

import styles from './styles.module.scss';

class Loader extends PureComponent {
  static propTypes = {
    size: PropTypes.number,
    loading: PropTypes.bool, // works only when loader has children
    selfContained: PropTypes.bool, // works only when loader has no children
    fullSized: PropTypes.bool, // works only when loader has no children
    className: PropTypes.string, // works only when loader has no children
  }

  static defaultProps = {
    size: 24,
    selfContained: true,
    fullSized: false,
    className: '',
    loading: false
  }

  render() {
    const { children, loading, size, selfContained, fullSized, className } = this.props;

    const classNames = cn({
      [styles.selfContained]: selfContained,
      [styles.fullSized]: fullSized,
      className
    });

    if (children) {
      return (
        <Spin
          indicator={<Icon type="loading" style={{ fontSize: size }} spin />}
          spinning={loading}
        >
          { children }
        </Spin>
      );
    }

    return (
      <div className={classNames}>
        <Spin indicator={<Icon type="loading" style={{ fontSize: size }} spin />} />
      </div>
    );
  }
}

export default Loader;
