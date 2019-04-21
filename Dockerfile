FROM ubuntu
RUN apt-get update
RUN apt-get install -y wget

CMD ["scrapy crawl secure.sos.state.or.us"]
