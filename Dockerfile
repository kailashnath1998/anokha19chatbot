FROM python:3.6.8-alpine3.8

COPY . /app

WORKDIR /app

RUN pip install -r requirments.txt

EXPOSE 6789

CMD ["python" ,"bottel.py", "&"]

CMD ["python" ,"telebot.py", "&"]
