const fs = require('fs');
const Controller = require('egg').Controller;

class BaseController extends Controller {
  constructor(ctx) {
    super(ctx);

    this.model = null;
    this.name = 'Resource';
    this.allowedQuery = null;
    this.forceDbUsage = this.config.useDb;
  }

  get user() {
    return this.ctx.session.user;
  }

  success(data) {
    this.ctx.body = data || { success: true };
  }

  validate(rule, data) {
    const actualData = data || this.ctx.request.body;

    return this.ctx.validate(rule, actualData);
  }

  notFound(instanceName) {
    this.ctx.throw(404, `${instanceName} not found`);
  }

  badRequest(message = 'Invalid request') {
    this.ctx.throw(400, message);
  }

  forbidden(message = 'Forbidden') {
    this.ctx.throw(403, message);
  }


  async getCurrentUser() {
    const { ctx, app } = this;
    if (ctx.currentUser) {
      return ctx.currentUser;
    }
    const token = ctx.request.header.accesstoken;

    if (!token) {
      ctx.throw(403, 'Access token required');
    }

    const currentUser = app.jwt.verify(token, app.config.jwt.secret);

    console.log('currentUser', currentUser);

    const user = await ctx.service.userService.getUserByEmail(currentUser.email);
    ctx.currentUser = user;

    if (!user) {
      ctx.throw(403, 'Invalid Access token');
    }

    return user;
  }

  async index() {
    // const { service } = this;
    // // const { criteria, options } = this.checkAndBuildMongoQuery(this.ctx.query);
    // // const page = await service.paginationService.findAll(this.model, criteria, options);
    // const page = {}; // @todo
    // const transformedPage = await this.transformPage(page);
    // return this.success(transformedPage);
    // moved to api controller
  }

  async show() {
    // const { ctx } = this;
    // const record = {} ; // await this.model.findOne({ _id: ctx.params.id });
    // if (!record) {
    //   return this.notFound(this.name);
    // }
    //
    // this.success(await this.transformEntry(record));
    // moved to api controller
  }


  async cachedRequest(identifier) {

    const cacheDir = this.config.cacheDir;
    const file = `${cacheDir}/${identifier}.json`;
    if (this.forceDbUsage) {
      this.ctx.logger.info('Did not use cache, because we forced db usage');
      return false;
    }
    if (fs.existsSync(file)) {
      const data = fs.readFileSync(file, 'utf8');
      try {
        return JSON.parse(data);
      } catch (e) {
        console.error('error on parsing', file);
      }
    } else {
      this.ctx.logger.info(`cache file ${file} does not exists`);
    }
    return false;
  }

  async cacheRequest(identifier, data) {

    const cacheDir = this.config.cacheDir;
    const file = `${cacheDir}/${identifier}.json`;

    try {
      const json = JSON.stringify(data);
      fs.writeFileSync(file, json);
    } catch (e) {
      console.error('error on saving cache file: ' + file);
    }

  }

  async wrapCache(identifier, callback, delay) {
    const cachedResult = await this.cachedRequest(identifier);
    if (cachedResult) {
      if (delay) {
        await this.sleep(delay);
      }
      return cachedResult;
    }
    const data = await callback();
    await this.cacheRequest(identifier, data);
    return data;
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }


}

module.exports = BaseController;
