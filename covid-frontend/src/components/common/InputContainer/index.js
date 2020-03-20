import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import cn from 'classnames';
import styles from './styles.module.scss';

class InputContainer extends PureComponent {
  static propTypes = {
    label: PropTypes.string,
    error: PropTypes.oneOfType([
      PropTypes.bool,
      PropTypes.string
    ]),
    info: PropTypes.oneOfType([
      PropTypes.bool,
      PropTypes.string
    ]),
    fluid: PropTypes.bool,
    className: PropTypes.string,
  }

  static defaultProps = {
    label: '',
    info: '',
    error: '',
    fluid: false,

    className: ''
  }

  render() {
    const { label, info, error, fluid, className, children } = this.props;

    const classes = cn(
      styles.container,
      { [styles.fluid]: fluid },
      { [styles.withError]: error },
      className
    );

    return (
      <div className={classes}>
        { label && <label>{label}</label> }
        { children }
        { (error && (typeof error === 'string')) && <span className={styles.error}>{error}</span> }
        { info && <span className={styles.info}>{info}</span> }
      </div>
    );
  }
}

export default InputContainer;
