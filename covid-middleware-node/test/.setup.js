
const exec = require('child_process').exec;
const { app } = require('egg-mock/bootstrap');
const { promisify } = require('util');

before(async () => {
  await app.ready();
  // await promisify(app.mongooseDB.db.dropDatabase.bind(app.mongooseDB.db))();
  // await promisify(exec)('NODE_ENV=test npm run migrate:up');
});
