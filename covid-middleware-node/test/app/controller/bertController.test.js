// const SeedFactory = require('../../setting/seedFactory');
const { app, assert } = require('egg-mock/bootstrap');

describe('app/controller/userController', () => {


  before(async () => {
  });

  describe('POST /api/bert/question', () => {
    it('should return answer', async () => {

      const { status, body } = await app.httpRequest()
        .post('/api/bert/question')
        .send({
          question: 'Why did this happen?',
        });

      assert.equal(status, 200);
    });
    it('should return answer uncached', async () => {

      const random  = Math.round(Math.random() * 1000);
      const { status, body } = await app.httpRequest()
        .post('/api/bert/question')
        .send({
          question: 'Why did this happen in ' + random +' ?',
        });

      console.log({
        question: 'Why did this happen in ' + random +' ?',
      });
      assert.equal(status, 200);
    });
  });
});
