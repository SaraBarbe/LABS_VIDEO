
FROM python:3.9


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update && apt-get install -y ffmpeg


COPY ./__init__.py /code/
COPY ./main.py /code/
COPY ./index.html /code/
RUN mkdir -p /code/uploads

RUN mkdir -p /code/static
RUN mkdir -p /code/static/images
COPY ./images/*.jpg /code/static/images/

CMD ["fastapi", "run", "main.py", "--port", "80"]