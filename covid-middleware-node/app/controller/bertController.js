const { ApiController } = require('./base');

class DocumentController extends ApiController {
  constructor(ctx) {
    super(ctx);
    this.model = ctx.model ? ctx.model.Answer : null;
    this.name = 'Answer';
  }

  async question() {

    const { question } = this.ctx.request.body;
    const { bertService } = this.ctx.service;

    if (!question) {
      this.ctx.throw(422, 'question is required');
    }

    const { response } = await bertService.requestQuestion(question);

    this.ctx.body = response;
  }


}

module.exports = DocumentController;
