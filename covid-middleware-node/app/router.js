/**
 * @param {Egg.Application} app - egg application
 */
module.exports = app => {
  const { router, controller } = app;
  router.get('/', controller.healthController.home);

  router.get('/alive', controller.healthController.alive);
  router.get('/api/alive', controller.healthController.alive);
  // router.get('/api/documentation', controller.documentationController.index);


  router.post('/api/bert/question', controller.bertController.question);

  router.get('/api/questions/autocomplete', controller.bertresponseController.autocomplete);


};
