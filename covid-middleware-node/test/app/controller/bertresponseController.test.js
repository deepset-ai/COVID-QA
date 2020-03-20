// const SeedFactory = require('../../setting/seedFactory');
const { app, assert } = require('egg-mock/bootstrap');

describe('app/controller/userController', () => {


  before(async () => {
  });

  describe('POST /api/questions/autocomplete', () => {
    let user;
    let token;
    let contracts;

    it('should find an autocomplete response', async () => {

      const { status, body } = await app.httpRequest()
        .get('/api/questions/autocomplete')
        .query({ search: 'hello' })

      ;
      console.log({ body });
      assert.equal(status, 200);
    });
    // it('should respond with 422', async () => {
    //   const {status, body} = await app.httpRequest()
    //     .get('/api/questions/autocomplete')
    //   ;
    //   assert.equal(status, 422);
    // });
  });
});
