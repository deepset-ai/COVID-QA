const { app, assert } = require('egg-mock/bootstrap');
const sinon = require('sinon');

describe('app/service/bertService', () => {
  describe('saveSubscription()', () => {
    let bertService;

    before(() => {
      const ctx = app.mockContext();
      bertService = ctx.service.bertService;
    });


  });


})
;
