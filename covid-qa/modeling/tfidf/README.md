## Train and Evaluate TF-IDF Model

### 1. Train sentencepiece model

Preprocessing takes max 1 argument (= vocab size for sentencepiece) which defaults to 24000 if not set.

`cat my_large_text | python3 ./preprocess.py 16000`

### 2. Train TF-IDF Vectors

TF-IDF Vectors are trained with 1- and 2-bigrams, with otherwise default settings

`cat my_questions | python3 ./tfidf_train.py`

### 3. Score and submit

Each pair in the eval set is scored with cosine similarity and then results are posted to mflow

`python3 ./tfidf_client.py`
