<img alt="cover-photo" src="https://github.com/deepset-ai/COVID-QA/blob/master/docs/img/covid-bert.png?raw=true" width="130" height="298" />

This open source project serves two purposes. 
1. Collection and evaluation of a Question Answering dataset to improve existing QA/search methods - **COVID-QA**
2. Question matching capabilities: Provide trustworthy answers to questions about COVID-19 via NLP - **outdated**

# COVID-QA
- Link to [COVID-QA Dataset](https://github.com/deepset-ai/COVID-QA/tree/master/data/question-answering/COVID-QA.json) 
- Accompanying paper on [OpenReview](https://openreview.net/forum?id=JENSKEEzsoU)
- Annotation guidelines as [pdf](https://drive.google.com/file/d/1Wv3OIC0Z7ibHIzOm9Xw_r0gjTFmpl-33/view?usp=sharing) or [videos](https://www.youtube.com/playlist?list=PL0pJupneBHx4rkCtNmaXUs1q7SV7EjLED)
- [deepset/roberta-base-squad2-covid](https://huggingface.co/deepset/roberta-base-squad2-covid) a QA model trained on COVID-QA 

**Update 14th April, 2020:** We are open sourcing the first batch of 
[SQuAD style question answering annotations](https://github.com/deepset-ai/COVID-QA/tree/master/data/question-answering).
Thanks to [Tony Reina](https://www.linkedin.com/in/skysurgery/) for managing the process and the 
many professional annotators who spend valuable time looking through Covid related research papers.


# FAQ matching
**Update 17th June, 2020**: As the pandemic is thankfully slowing down and other information sources have catched up, we decided to take our hosted API and UI offline. We will keep the repository here as an inspiration for other projects and to share the COVID-QA dataset.

### :zap: Problem
- People have many questions about COVID-19
- Answers are scattered on different websites 
- Finding the right answers takes a lot of time
- Trustworthiness of answers is hard to judge
- Many answers get outdated soon

### :bulb: Idea
- Aggregate FAQs and texts from trustworthy data sources (WHO, CDC ...)
- Provide a UI where people can ask questions
- Use NLP to match incoming questions of users with meaningful answers
- Users can provide feedback about answers to improve the NLP model and flag outdated or wrong answers
- Display most common queries without good answers to guide data collection and model improvements

### :gear:	Tech 
- Scrapers to collect data
- Elasticsearch to store texts, FAQs, embeddings
- NLP Models implemented via [Haystack](https://github.com/deepset-ai/haystack/) to find answers via a) detecting similar question in FAQs b) detect answers in free texts (extractive QA)
- React Frontend

