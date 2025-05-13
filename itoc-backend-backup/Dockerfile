FROM python:3.9@sha256:6f468ed026185ad7f1a13d1dde8f307449fce3777695bfacf91da8f7987b5fd5
RUN pip install pipenv

WORKDIR /api/
COPY Pipfile /api/Pipfile
COPY Pipfile.lock /api/Pipfile.lock
RUN pipenv install
COPY ./api/ /api/

# CMD ["pipenv", "run", "uvicorn", "--port", "9000", "--host", "0.0.0.0", "main:app"]
CMD ["pipenv", "run", "uvicorn", "--port", "9000", "--host", "0.0.0.0", "main:app"]
