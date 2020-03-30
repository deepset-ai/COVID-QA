FROM python:3.7.4-stretch

WORKDIR /home/user

# install haystack and dependencies
COPY requirements.txt /home/user/
RUN pip install -r requirements.txt

COPY backend /home/user/backend
COPY covid_nlp /home/user/covid_nlp

EXPOSE 8000

# cmd for running the API
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]