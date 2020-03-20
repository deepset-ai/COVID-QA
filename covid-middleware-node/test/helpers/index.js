module.exports = {
  async loginAndGetToken(app, credentials) {
    const { body } = await app.httpRequest()
      .post('/user/login')
      .send({
        email: credentials.email,
        password: credentials.password,
      });

    return body.token;
  },
  getBasicAuthToken(name, pass) {
    return 'Basic ' + new Buffer(name + ':' + pass).toString('base64');
  },
};
