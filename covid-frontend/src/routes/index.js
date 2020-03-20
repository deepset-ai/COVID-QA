import React, { PureComponent } from 'react';
import { Route, Switch, Redirect, withRouter } from 'react-router-dom';
import App from 'components/App';
import Provider from 'components/Provider';
import links from 'routes/links';
import { MainTemplate } from 'components/themes';
import Home from 'components/Home';
import Answers from 'components/Answers';
import NotFound from 'components/NotFound';

class Routes extends PureComponent {
  render () {
    return (
      <App>

        <Provider>
          <Switch>
            <Redirect exact from='/' to={links.home} />
            {/* <Redirect exact from='/index.html' to={links.home} /> */}

            <Route path={links.home} component={Home} />

            <MainTemplate>
              <Switch>
                <Route exact path={links.answers} component={Answers} />

                <Route component={NotFound} />
              </Switch>

            </MainTemplate>

            <Route component={NotFound} />
          </Switch>
        </Provider>

      </App>
    );
  }
}

export default withRouter(Routes);
