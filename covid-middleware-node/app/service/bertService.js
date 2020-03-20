const Service = require('./baseService');
const axios = require('axios');
const objecthash = require('object-hash');

class BertService extends Service {
  constructor(ctx) {
    super(ctx);
    this.Bertresponse = ctx.model ? ctx.model.Bertresponse : null;
    this.ctx = ctx;
    const config = this.config.bert;
    this.bertURL = config.url;
    this.enableCache = false;

  }


  async requestQuestion(question, filter) {
    question = question.trim();
    const cacheHash = objecthash({ question, filter });
    const cached = await this.getCache(cacheHash);
    if (this.enableCache && cached) {
      return { response: cached, filter };
    }

    const response = await this._fetchBertQuestion(question, filter);
    if (!response) {
      this.ctx.throw(500, 'invalid response from Bert');
    }
    if (!cached) { // avoid saving duplicates
      await this.saveBertquestion(cacheHash, response);
    }
    return { response, filter };

  }

  async _fetchBertQuestion(question, filter) {

    const bertUrl = this.bertURL;
    const params = {
      questions: [ question ],
      filter,
      top_k_retriever: 5,
    };
    let bertResponse = null;

    try {
      this.ctx.logger.info(`requesting uncached question to ${bertUrl} with :` + JSON.stringify(params));
      const result = await axios.post(bertUrl, params);
      bertResponse = result.data.results[0];
    } catch (e) {
      const status = e.response ? e.response.status : 500;
      if (status === 503) {
        this.ctx.throw(422, 'Bert is busy at the moment, please try again in a few seconds');
        return;
      }
      this.ctx.logger.error('request failed to ', bertUrl);
      this.ctx.throw(status, 'Bert failed to answer');
    }
    return bertResponse;
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }


  // database cache

  async getCache(requesthash) {
    const response = await this.Bertresponse.findOne({ where: { requesthash } });
    if (response) {
      response.hits++;
      await response.save();
    }
    return response;
  }

  async saveBertquestion(requesthash, finalData) {
    const newResponse = new this.Bertresponse({ requesthash, hits: 0, ...finalData });
    await newResponse.save();
  }


}

module
  .exports = BertService;
