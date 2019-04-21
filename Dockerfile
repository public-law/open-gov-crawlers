FROM python:3.7

COPY oar /app/oar
COPY scrapy.cfg /app
COPY requirements.txt /app

WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["scrapy", "crawl", "secure.sos.state.or.us"]
