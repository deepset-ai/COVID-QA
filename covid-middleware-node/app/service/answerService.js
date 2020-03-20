const Service = require('./baseService');


class AnswerService extends Service {
  constructor(ctx) {
    super(ctx);
    this.model = ctx.model.Answer;
  }

  async findByDocument(document_id) {
    return this.model.findAll({ where: { document_id } });
  }

  async findByDocumentAndLabler(document_id, labeler_id) {
    return this.model.findAll({ where: { document_id, labeler_id } });
  }

  async getAnswersToExport() {
    const query = `SELECT answers.id,
                          questions.text as question,
                          answers.selected_text,
                          answers.document_id,
                          question_id,
                          labeler_id,
                          start_offset,
                          end_offset
                   FROM answers
                          JOIN questions ON question_id = questions.id`;
    const sequelize = this.model.sequelize;
    const result = await sequelize.query(query, { type: sequelize.QueryTypes.RAW });
    return result[0];

  }

  async getAnswersByUserid(id) {
    const query = `SELECT answers.id,
                          questions.text as question,
                          answers.selected_text,
                          answers.document_id,
                          question_id,
                          labeler_id,
                          start_offset,
                          end_offset
                   FROM answers
                          JOIN questions ON question_id = questions.id
              WHERE answers.labeler_id = ${id}
    `;
    const sequelize = this.model.sequelize;
    const result = await sequelize.query(query, { type: sequelize.QueryTypes.RAW });
    return result[0];

  }
}

module.exports = AnswerService;
