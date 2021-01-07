FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends build-essential r-base python3.7 python3-pip python3-setuptools python3-dev

WORKDIR /src

COPY requirements.txt /src/requirements.txt

COPY . /src

RUN pip3 install -r requirements.txt

RUN Rscript -e "install.packages('vroom','LaF','dplyr','fs','DataExplorer','janitor','jsonlite','dplyr')"

EXPOSE 8080

CMD [ "python", "./main.py" ]