## Train and Evaluate TF-IDF Model

### 1. Train sentencepiece model

`cat my_large_text | python3 ./preprocess.py`

### 2. Train TF-IDF Vectors

`cat my_questions | python3 ./tfidf_train.py`
