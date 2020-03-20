
module.exports = app => {
  const { STRING, INTEGER, JSONB, DATE } = app.Sequelize;

  const Schema = app.model.define('bertresponse', {
    question: STRING,
    answers: JSONB,
    // filter
    hits: INTEGER,
    requesthash: STRING,
    // creatd udpated
    created_at: DATE,
    updated_at: DATE,
  }, { table_name: 'bertresponses' });

  return Schema;
};

