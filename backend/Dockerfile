FROM python:3.9
COPY . ./app
COPY ../data ./app/data
WORKDIR /app/footgram
RUN pip3 install -r ../requirements.txt --no-cache-dir
