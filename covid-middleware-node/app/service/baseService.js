const Service = require('egg').Service;
const HttpError = require('../errors/httpError');
class BaseService extends Service {
  constructor(ctx) {
    super(ctx);

    this.model = null;
    this.name = '';
  }

  create(entity) {
    return this.model.create(entity);
  }

  find(query, projection) {
    return this.model.find(query, projection);
  }

  async findOne(query, projection) {
    return this.model.findOne(query, projection);
  }

  async findById(id, projection) {
    return this.model.findByPk(id, projection);
  }

  async checkAndFindById(id, projection) {
    const entity = await this.findById(id, projection);
    if (!entity) {
      throw new HttpError(404, `Record with ${id} in collection ${this.name} not found`);
    }

    return entity;
  }

  async checkAndFindOne(query, projection) {
    const entity = await this.findOne(query, projection);
    if (!entity) {
      throw new HttpError(404, `Record in collection ${this.name} not found`);
    }

    return entity;
  }

  async updateById(id, record) {
    return this.model.findOneAndUpdate({ _id: id }, record, { new: true });
  }

  async updateMany(query, updateSet) {
    return this.model.updateMany(query, updateSet);
  }

  async updateOne(query, updateSet, options) {
    return this.model.updateOne(query, updateSet, options);
  }
}

module.exports = BaseService;
