module.exports = () => {
  const config = exports = {};
  config.env = 'test';

  config.NODE_ENV = 'test';

  config.logger = {
    consoleLevel: 'DEBUG',
    disableConsoleAfterReady: true,
  };


  return config;
};

