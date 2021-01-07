FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends build-essential r-base python3.7 python3-pip python3-setuptools libffi-dev openssl-dev python3-dev

WORKDIR /app

COPY /src/requirements.txt /app/requirements.txt

COPY . /app

RUN pip3 install -r requirements.txt

RUN Rscript -e "install.packages('vroom','LaF','dplyr','fs','DataExplorer','janitor','jsonlite','dplyr')"

EXPOSE 8080

CMD [ "python", "./main.py" ]