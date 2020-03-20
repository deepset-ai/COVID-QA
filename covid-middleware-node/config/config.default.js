require('dotenv').config();


module.exports = appInfo => {
  const config = exports = {};
  config.env = 'default';
  config.keys = appInfo.name + '_1539102769744_2629';
  config.mailDir = '../app/mail/';


  const logDir = process.env.LOG_DIR || '/tmp/';

  config.rundir = '/tmp/run';

  const { CI_DB_HOSTNAME, CI_DB_NAME, CI_DB_USERNAME, CI_DB_PASSWORD } = process.env;

  exports.sequelize = {
    dialect: 'postgres',
    database: CI_DB_NAME,
    host: CI_DB_HOSTNAME,
    port: 5432,
    username: CI_DB_USERNAME,
    password: CI_DB_PASSWORD,
  };


  config.bert = {
    url: 'http://3.121.62.187/models/1/faq-qa',
    cacheSleepTime: 0,
  };
  // disable sequlize;

  config.security = {
    domainWhiteList: [ '*' ],
    csrf: {
      enable: false,
    },
  };

  config.jwt = {
    secret: 'OUmCS609ZZaRbBY4H5MvLQ2hNKP1873U',
  };
  config.onerror = {
    all(err, ctx) {
      if (err.code === 'invalid_param') {
        const error = {
          statusCode: ctx.status,
          message: err.message,
          errors: err.errors,
        };
        ctx.body = JSON.stringify(error);
        return;
      }
      if (err.type === 'http' || err.status) {
        ctx.status = err.status;
        ctx.body = JSON.stringify({ message: err.message });
        return;
      }
      ctx.body = JSON.stringify({ message: 'Internal server error' });
    },
  };


  exports.logger = {
    consoleLevel: 'INFO',
    disableConsoleAfterReady: false,
    dir: logDir,
    coreLogger: {},
  };

  return config;
};

