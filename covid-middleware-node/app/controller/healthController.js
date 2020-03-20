const Controller = require('egg').Controller;
const bootTime = new Date();
const packageJson = require('../../package');

class HomeController extends Controller {
  async alive() {
    this.ctx.body = {
      name: packageJson.name,
      uptime: this.getTimeDiff(new Date(), bootTime),
      build: packageJson.build,
      version: packageJson.version,
      NODE_ENV: process.env.NODE_ENV,
      EGG_SERVER_ENV: process.env.EGG_SERVER_ENV,
    };
  }

  home() {
    this.ctx.body = {
      status: 200,
      message: 'covid bert ready',
    };
  }
  getTimeDiff(d1, d2) {

    const diff = new Date(d1.getTime() - d2.getTime());
    return (diff.getUTCFullYear() - 1970) + ' yrs '
      + diff.getUTCMonth() + ' month '
      + (diff.getUTCDate() - 1) + ' days '
      + (diff.getHours() - 1) + ':'
      + diff.getMinutes() + ':'
      + diff.getSeconds();

  }
}

module.exports = HomeController;
