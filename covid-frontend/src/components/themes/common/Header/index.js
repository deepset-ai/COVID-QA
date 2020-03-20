import React, { PureComponent } from 'react';
import { Link } from 'react-router-dom';
import links from 'routes/links';
import logo from 'assets/images/logo.png';
import styles from './styles.module.scss';

class Header extends PureComponent {

  render() {

    return (
      <div className={styles.wrapper}>
        <header className={styles.header}>
          <Link to={links.home} className={styles.homeLink}>
            <div className={styles.logo}>
              <img src={logo} alt="corona-scholar logo" />
            </div>
          </Link>
        </header>
      </div>
    );
  }
}


export default Header;
