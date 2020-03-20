const BaseController = require('./baseController');

class ApiController extends BaseController {
  async index() {
    const { service } = this;
    const { criteria, options } = this.checkAndBuildQuery(this.ctx.query);
    const page = await service.paginationService.findAll(this.model, criteria, options);
    this.validation = null;
    return this.success(page);
  }

  checkAndBuildQuery(query) {
    const options = {
      limit: query.limit ? query.limit : undefined,
      offset: query.offset ? query.offset : undefined,
    };
    const criteria = {};
    if (this.order) {
      options.order = this.order;
    }
    // hack
    if (query.globalquestions) {
      criteria.document_id = null;
    }

    return { options, criteria };
  }

  async show() {
    const record = await this.model.findByPk(this.ctx.params.id);
    if (!record) {
      return this.notFound(this.name);
    }

    return this.success(record.get({ plain: true }));
  }

  async create() {

    // get post parameter

    if (this.validation && this.validation.create) {
      this.validate(this.validation.create);
    }

    const record = await this.model.create(this.ctx.request.body);
    this.success({ data: record });

  }

  async update() {
    const { model } = this;
    // First try to find the record
    const id = this.ctx.params.id;
    const record = await model.findByPk(id);
    if (!record) {
      return this.notFound(this.name);
    }

    if (this.validation && this.validation.update) {
      this.validate(this.validation.update);
    }
    const body = this.ctx.request.body;

    await this.model.update(
      body,
      { where: { id } }
    );
    const item = await model.findByPk(id);

    this.success({ message: 'ok', item: item.get({ plain: true }) });
  }

  async _updateOrCreate(where, newItem) {
    const { model } = this;
    // First try to find the record
    const foundItem = await model.findOne({ where });
    if (!foundItem) {
      // Item not found, create a new one
      const item = await model.create(newItem);
      return { item, created: true };
    }
    // Found an item, update it
    let item = await model.update(newItem, { where });
    item = await model.findOne({ where });
    return { item, created: false };
  }

  async destroy() {
    const { ctx } = this;
    const { id } = ctx.params;

    const record = await this.model.findByPk(this.ctx.params.id);
    if (!record) {
      this.notFound();
      return;
    }
    await record.destroy();

    this.success({ id });
  }

  async transformPage(page) {
    return page;
  }

  async transformEntry(entry) {
    return entry.toObject();
  }

}

module.exports = ApiController;
