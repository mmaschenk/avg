FROM python:3.7

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY manage.py /app/
COPY avgregister /app/avgregister
COPY core /app/core
COPY templates /app/templates
COPY runapp.sh /app/

EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/app/runapp.sh"]