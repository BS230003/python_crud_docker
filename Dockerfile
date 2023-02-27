FROM python:3.8-slim-buster

WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /src
COPY templates/*.* /src/templates/*.*
COPY uploads /src/uploads
COPY static /src/static
COPY static/images /src/static/images
COPY static/images/*.* /src/static/images/*.*


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
