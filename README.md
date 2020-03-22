# COVID-QA

<img src="https://github.com/deepset-ai/COVID-QA/blob/master/docs/img/covid-bert.png?raw=true" width="130" height="298" />

Provide trustworthy questions to COVID-19 via NLP

Staging: https://covid-staging.deepset.ai/

Prod: https://covid.deepset.ai/

## :zap: Problem
- People have many questions about COVID-19
- Answers are scattered on different websites 
- Finding the right answers takes a lot of time
- Trustworthiness of answers is hard to judge
- Many answers get outdated soon

## :bulb: Idea
- Aggregate FAQs and texts from trustworty data sources (WHO, CDC ...)
- Provide an UI where people can ask questions
- Use NLP to match incoming questions of users with meaningful answers
- Users can provide feedback about answers to improve the NLP model and flag outdated or wrong answers
- Display most common queries without good answers to guide data collection and model improvements

## :gear:	Tech 
- Scrapers to collect data
- Elasticsearch to store texts, FAQs, embeddings
- NLP Models implented via [Haystack](https://github.com/deepset-ai/haystack/) to find answers via a) detecting similar question in FAQs b) detect answers in free texts (extractive QA)
- NodeJS / koa / eggjs middleware
- React Frontend

## Quick overview of current status 

1. Check out the [demo app](https://covid.deepset.ai/) to get a basic idea 
2. Data: At the moment we are using [scrapers](https://github.com/deepset-ai/COVID-QA/tree/master/data/scrapers) to create a CSV that get's ingested into elasticsearch
3. Model: The NLP model to find answers is build via haystack. It's configured and exposed via this [API](https://github.com/deepset-ai/COVID-QA/tree/master/backend).
4. Frontend/middleware: TODO

## :heart: How you can help
This project is build by the community for the community. We are really appreciating every kind of support! There's plenty of work on UX, Design, ML, Backend, Frontend, Middlewware, Data collection ... 

We are also happy if you just report bugs, add documentation or flag useful/inappropriate answers returned by the model.

Some next TODOs we see:
### Data / Backend
- [ ] Integrate more data sources via scrapers that return a csv with fields: [question,	answer, answer_html, 
link, name, source, category, country, region, city, lang, last_update](https://github.com/deepset-ai/COVID-QA/blob/master/docs/img/example-data-format.png)
- [ ] Handling of special non-FAQ questions via other APIs (e.g. “How many infections in Berlin?”)
- [ ] Improve API to foster external integrations (e.g. Chatsystems) 
- [ ] Logging & storage to foster analysis of common queries with bad results  
- [ ] Support other languages (data collection)

### Machine learning / NLP / IR
- [x] English evaluation dataset & pipeline to benchmark models
- [ ] Benchmark baseline models
- [ ] Improve NLP models for FAQ matching (better embeddings, e.g. sentence-bert trained on Quora duplicate questions dataset)
- [ ] Add extractive QA Models
- [ ] Support other languages (models)
- [ ] Tune Elasticsearch + Embedding models

### UI/UX/Design
- [ ] Integrate user feedback mechanism for answers (flag as "correct", "not matching my question", "outdated", "fake news")
- [ ] Tab to explore common queries and those with bad answers
- [ ] Logos / icons
- [ ] Intuitive displaying of search results
- [ ] UX for adding/reviewing data sources by the crowd
