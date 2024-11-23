
FROM python:3.9


WORKDIR /code/service2


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update && apt-get install -y ffmpeg


COPY ./__init__.py /code/service2/
COPY ./main.py /code/service2/
RUN mkdir -p /code/service2/uploads


CMD ["fastapi", "run", "main.py", "--port", "80"]