FROM python:alpine
LABEL Maintainer='KaruleanDEV'
LABEL Version='0.1 Alpha'
LABEL Description='ScrapingFoxholeAPI'

WORKDIR /home/
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY main.py ./
EXPOSE 8500

RUN apk --update --no-cache add curl
HEALTHCHECK CMD curl --fail http://localhost:8500/ || exit 1
CMD ["python", "-u", "./main.py"]
