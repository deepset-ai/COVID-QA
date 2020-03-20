module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('bertresponses', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER,
      },
      requesthash: {
        type: Sequelize.STRING,
      },
      question: {
        type: Sequelize.STRING,
      },
      answers: {
        type: Sequelize.JSONB,
      },
      document_id: {
        type: Sequelize.INTEGER,
        allowNull: true,
      },
      hits: {
        type: Sequelize.INTEGER,
        allowNull: true,
      },
      created_at: {
        allowNull: false,
        type: Sequelize.DATE,
      },
      updated_at: {
        allowNull: false,
        type: Sequelize.DATE,
      },
    });
  },

  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('bertresponse');
  },
};
