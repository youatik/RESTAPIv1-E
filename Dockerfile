FROM python:3-alpine3.15
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt && apk add --no-cache supervisor
COPY ./supervisord.conf /etc/supervisord.conf
EXPOSE 5001 5002
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
LABEL authors="youatik"

