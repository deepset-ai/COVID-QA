const { ApiController } = require('./base');
const { Op } = require('sequelize');

class BertresponseController extends ApiController {
  constructor(ctx) {
    super(ctx);
    this.model = ctx.model.Bertresponse;
    this.name = 'Bertresponse';
  }

  async autocomplete() {

    const { search } = this.ctx.query;
    if (!search) {
      this.ctx.throw(422, 'search parameter is required');
      return;
    }
    const searchTrimmed = search.trim();

    const responses = await this.ctx.model.Bertresponse.findAll({
      attributes: [ 'question', 'hits', 'id' ],
      raw: true,
      where: { question: { [Op.iLike]: `${searchTrimmed}%` } },
      order: [
        [ 'hits', 'DESC' ],
      ],
      limit: 10,
    });
    this.ctx.body = responses;
  }

}

module.exports = BertresponseController;
