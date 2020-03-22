import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import cn from 'classnames';
import styles from './styles.module.scss';

class Tag extends PureComponent {
  static propTypes = {
    text: PropTypes.string,
    theme: PropTypes.oneOf(['red', 'green', 'orange']),
    className: PropTypes.string,
  }

  static defaultProps = {
    text: '',
    theme: 'green',
  }

  // Themes signify level of confidence in answer
  static themes = {
    RED: 'red',
    GREEN: 'green',
    ORANGE: 'orange'
  }

  render() {
    const { text, theme, className } = this.props;
    return (
      <div className={cn(
        styles.tag,
        styles[theme],
        className
      )}>
        {text}
      </div>
    );
  }
}

export default Tag;
