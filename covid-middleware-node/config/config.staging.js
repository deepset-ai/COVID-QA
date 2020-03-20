
module.exports = appInfo => {
  const config = exports = {};
  config.keys = appInfo.name + '_1539102769744_2629';
  config.env = 'staging';

  config.security = {
    csrf: {
      enable: false,
    },
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

  return config;
};
